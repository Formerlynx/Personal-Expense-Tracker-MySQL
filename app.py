from flask import Flask, render_template, request, redirect, url_for, session, flash
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import textwrap
import os
import sys
import pyodbc
import shutil
import base64
import secrets
import threading
import webbrowser
import logging
import textwrap
from flask_bcrypt import Bcrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# Import system tray dependencies
try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
    import tkinter as tk
    from tkinter import messagebox
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

# Configure paths for PyInstaller
def get_base_path():
    """Get the base path for resources (works for both dev and frozen)"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_user_data_path():
    """Get path for user data (persistent storage)"""
    if sys.platform == 'win32':
        base = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'ExpenseTracker')
    else:
        base = os.path.join(os.path.expanduser('~'), '.expensetracker')
    
    if not os.path.exists(base):
        os.makedirs(base)
    return base

def get_settings_file():
    """Get path to settings file"""
    return os.path.join(get_user_data_path(), 'settings.txt')

def is_first_run():
    """Check if this is the first time running the app"""
    settings_file = get_settings_file()
    return not os.path.exists(settings_file)

def save_autostart_preference(enable):
    """Save user's autostart preference"""
    settings_file = get_settings_file()
    with open(settings_file, 'w') as f:
        f.write(f"autostart={'yes' if enable else 'no'}\n")
        f.write(f"first_run_done=yes\n")

def should_autostart():
    """Check if app should start in background"""
    settings_file = get_settings_file()
    if not os.path.exists(settings_file):
        return True  # Default to yes
    
    try:
        with open(settings_file, 'r') as f:
            for line in f:
                if line.startswith('autostart='):
                    return line.strip().split('=')[1] == 'yes'
    except:
        pass
    return True

def show_first_run_dialog():
    """Show dialog on first run asking about background running"""
    if not TRAY_AVAILABLE:
        return True
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    result = messagebox.askyesno(
        "Expense Tracker - First Run",
        "Welcome to Expense Tracker!\n\n"
        "Would you like this app to run in the background?\n\n"
        "• YES: App runs in system tray, access anytime via http://127.0.0.1:5000\n"
        "• NO: App closes when you close the browser\n\n"
        "You can change this later in settings.",
        icon='question'
    )
    
    root.destroy()
    return result

def initialize_database():
    """
    Initialize the database for the application.
    If running as executable, copy template database to user data folder.
    """
    if getattr(sys, 'frozen', False):
        user_data_path = get_user_data_path()
        db_path = os.path.join(user_data_path, 'expenses.accdb')
        
        if not os.path.exists(db_path):
            template_db = os.path.join(sys._MEIPASS, 'Database', 'expenses.accdb')
            if os.path.exists(template_db):
                shutil.copy2(template_db, db_path)
            else:
                raise FileNotFoundError("Template database not found in executable!")
        
        return db_path
    else:
        return os.path.join(os.getcwd(), 'Database', 'expenses.accdb')

# Encryption utilities
class EncryptionManager:
    """Manages encryption and decryption of expense data using AES-256"""
    
    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    @staticmethod
    def encrypt(data: str, key: bytes) -> str:
        """Encrypt data using Fernet (AES-256)"""
        f = Fernet(key)
        encrypted = f.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    @staticmethod
    def decrypt(encrypted_data: str, key: bytes) -> str:
        """Decrypt data using Fernet (AES-256)"""
        try:
            f = Fernet(key)
            decrypted = f.decrypt(base64.b64decode(encrypted_data))
            return decrypted.decode()
        except Exception:
            return "[Decryption Failed]"

base_path = get_base_path()
template_folder = os.path.join(base_path, 'templates')
static_folder = os.path.join(base_path, 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# when frozen, serve dynamic static files (charts) from user data directory
if getattr(sys, 'frozen', False):
    user_static_dir = os.path.join(get_user_data_path(), 'static')
    if not os.path.exists(user_static_dir):
        os.makedirs(user_static_dir)
    # override flask's static folder so url_for('static') points here
    app.static_folder = user_static_dir

app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))
bcrypt = Bcrypt(app)

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Error handler for debugging
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return f"Error: {str(e)}", 500

# Initialize database path
DB_PATH = initialize_database()

# Global variable for system tray icon
tray_icon = None

def get_db_connection():
    db_password = 'password'
    
    # Try different connection methods
    conn_str_options = [
        # Try without password first
        r"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH}",
        # Try with password
        r"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH};PWD={db_password}",
        # Try alternative driver name
        r"Provider=Microsoft.ACE.OLEDB.12.0;Data Source={DB_PATH}",
        # Try with password for OLEDB
        r"Provider=Microsoft.ACE.OLEDB.12.0;Data Source={DB_PATH};Jet OLEDB:Database Password={db_password}",
    ]
    
    for conn_str_template in conn_str_options:
        try:
            conn_str = conn_str_template.format(DB_PATH=DB_PATH, db_password=db_password)
            logger.debug(f"Trying connection: {conn_str}")
            conn = pyodbc.connect(conn_str)
            logger.info("Database connection successful")
            return conn
        except pyodbc.Error as e:
            logger.warning(f"Connection failed: {conn_str} - {str(e)}")
            continue
    
    # If all fail, raise the last error
    raise pyodbc.Error("Failed to connect to database. Please ensure Microsoft Access Database Engine is installed.")

def is_logged_in():
    return 'user_id' in session and 'encryption_key' in session

@app.before_request
def restrict_access():
    allowed_routes = ['login', 'signup', 'static']
    if not is_logged_in() and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        salt = secrets.token_bytes(32)
        salt_b64 = base64.b64encode(salt).decode()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", 
                          (username, hashed_password, salt_b64))
            conn.commit()
            conn.close()

            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        except pyodbc.IntegrityError:
            flash("Username already exists, please choose another one.", "danger")
            conn.close()
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, password, salt FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            
            salt = base64.b64decode(user[2])
            encryption_key = EncryptionManager.derive_key(password, salt)
            session['encryption_key'] = base64.b64encode(encryption_key).decode()
            
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if not is_logged_in():
        flash("Please log in to add expenses.", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    encryption_key = base64.b64decode(session['encryption_key'])

    cursor.execute("SELECT DISTINCT category FROM expenses WHERE user_id = ?", (session['user_id'],))
    encrypted_categories = [row[0] for row in cursor.fetchall()]
    categories = list(set([EncryptionManager.decrypt(cat, encryption_key) for cat in encrypted_categories]))
    categories.sort()

    if request.method == 'POST':
        raw_date = request.form['date']
        try:
            date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
            date = date_obj.strftime("%d-%m-%Y")
        except ValueError:
            date = raw_date

        selected_category = request.form['category']
        new_category = request.form.get('new_category', '').strip()
        amount = request.form['amount']
        rounded_amount = round(float(amount), 3)

        category = new_category if selected_category == 'add_new' else selected_category
        
        if not category:
            flash("Category cannot be empty.", "danger")
            conn.close()
            return redirect(url_for('add_expense'))
        
        if rounded_amount <= 0:
            flash("Amount must be greater than zero.", "danger")
            conn.close()
            return redirect(url_for('add_expense'))

        encrypted_date = EncryptionManager.encrypt(date, encryption_key)
        encrypted_category = EncryptionManager.encrypt(category, encryption_key)
        encrypted_amount = EncryptionManager.encrypt(str(rounded_amount), encryption_key)

        cursor.execute(
            "INSERT INTO expenses (expense_date, category, amount, user_id) VALUES (?, ?, ?, ?)",
            (encrypted_date, encrypted_category, encrypted_amount, session['user_id'])
        )
        conn.commit()
        conn.close()

        flash("Expense added successfully!", "success")
        return redirect(url_for('view_expenses'))

    conn.close()
    return render_template('add.html', categories=categories)

@app.route('/view')
def view_expenses():
    if not is_logged_in():
        flash("Please log in to view expenses.", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    encryption_key = base64.b64decode(session['encryption_key'])

    cursor.execute("SELECT id, expense_date, category, amount FROM expenses WHERE user_id = ? ORDER BY expense_date DESC", 
                   (session['user_id'],))
    rows = cursor.fetchall()

    expenses = []
    for row in rows:
        try:
            date_str = EncryptionManager.decrypt(row[1], encryption_key)
            category_str = EncryptionManager.decrypt(row[2], encryption_key)
            amount_str = EncryptionManager.decrypt(row[3], encryption_key)
            
            try:
                amount_val = float(amount_str)
                amount_formatted = f"{amount_val:.3f}"
            except:
                amount_formatted = amount_str
            
            # Parse date for sorting and grouping
            try:
                parsed_date = datetime.strptime(date_str, "%d-%m-%Y")
                year_month = parsed_date.strftime("%Y-%m")
                display_date = parsed_date.strftime("%d-%m-%Y")
            except:
                parsed_date = None
                year_month = "Unknown"
                display_date = date_str
            
            expenses.append({
                'id': row[0], 
                'date': display_date, 
                'parsed_date': parsed_date,
                'year_month': year_month,
                'category': category_str, 
                'amount': amount_formatted
            })
        except Exception:
            continue

    conn.close()
    
    # Group expenses by year-month
    from collections import defaultdict
    grouped_expenses = defaultdict(list)
    for exp in expenses:
        grouped_expenses[exp['year_month']].append(exp)
    
    # Sort groups by year-month descending
    sorted_groups = sorted(grouped_expenses.items(), key=lambda x: x[0], reverse=True)
    
    return render_template('view.html', grouped_expenses=sorted_groups)

@app.route('/analyze')
def analyze_expenses():
    if not is_logged_in():
        flash("Please log in to analyze expenses.", "warning")
        return redirect(url_for('login'))

    encryption_key = base64.b64decode(session['encryption_key'])
    
    selected_range = request.args.get('range')
    start_date_arg = request.args.get('start_date')
    end_date_arg = request.args.get('end_date')

    today = datetime.now().date()
    first_of_month = today.replace(day=1)
    
    try:
        if first_of_month.month == 12:
            next_month = first_of_month.replace(year=first_of_month.year + 1, month=1, day=1)
        else:
            next_month = first_of_month.replace(month=first_of_month.month + 1, day=1)
        last_of_month = next_month - timedelta(days=1)
    except Exception:
        last_of_month = today

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount, expense_date FROM expenses WHERE user_id = ?", 
                   (session['user_id'],))
    rows = cursor.fetchall()
    conn.close()

    def parse_date(raw_date):
        try:
            # Decrypt the date first
            decrypted = EncryptionManager.decrypt(raw_date, encryption_key)
            for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
                try:
                    return datetime.strptime(decrypted, fmt).date()
                except:
                    continue
            return None
        except:
            return None

    # Decrypt and aggregate current month totals
    current_month_totals = defaultdict(float)
    for row in rows:
        try:
            cat = EncryptionManager.decrypt(row[0], encryption_key)
            amt = float(EncryptionManager.decrypt(row[1], encryption_key))
            d = parse_date(row[2])
            if d and first_of_month <= d <= last_of_month:
                current_month_totals[cat] += amt
        except:
            continue

    pie_categories = list(current_month_totals.keys())
    pie_amounts = [current_month_totals[c] for c in pie_categories]

    # Determine date range for bar chart
    if selected_range is None:
        start_date = today.replace(month=1, day=1)
        end_date = today
        selected_range = 'ytd'
    else:
        try:
            if selected_range == 'custom' and start_date_arg and end_date_arg:
                start_date = datetime.strptime(start_date_arg, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_arg, "%Y-%m-%d").date()
            elif selected_range == 'previous_year':
                start_date = today.replace(year=today.year - 1, month=1, day=1)
                end_date = today.replace(year=today.year - 1, month=12, day=31)
            elif selected_range == 'ytd':
                start_date = today.replace(month=1, day=1)
                end_date = today
            else:
                months = int(selected_range)
                start_date = today - relativedelta(months=months)
                end_date = today
        except:
            start_date = today.replace(month=1, day=1)
            end_date = today

    # Aggregate totals for selected period
    totals = defaultdict(float)
    year_totals = defaultdict(float)
    totals_by_year = defaultdict(float)
    
    for row in rows:
        try:
            cat = EncryptionManager.decrypt(row[0], encryption_key)
            amt = float(EncryptionManager.decrypt(row[1], encryption_key))
            d = parse_date(row[2])
            
            if not d:
                continue
                
            totals_by_year[d.year] += amt
            
            if d.year == today.year:
                year_totals[cat] += amt
            
            if start_date <= d <= end_date:
                totals[cat] += amt
        except:
            continue

    bar_categories = list(totals.keys())
    bar_amounts = [totals[c] for c in bar_categories]
    
    year_categories = list(year_totals.keys())
    year_amounts = [year_totals[c] for c in year_categories]

    # Generate charts
    # determine where to save charts; when running frozen use flask's static_folder
    if getattr(sys, 'frozen', False):
        static_path = app.static_folder
    else:
        static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    
    if not os.path.exists(static_path):
        os.makedirs(static_path)
    # remove stale images from previous analyses so cache tokens reflect fresh files
    for old in ('chart.png', 'bar_chart.png', 'yearly_trend.png'):
        try:
            os.remove(os.path.join(static_path, old))
        except OSError:
            pass

    pie_file = None
    bar_chart_file = None
    yearly_trend_file = None

    try:
        if pie_categories and sum(pie_amounts) > 0:
            plt.figure(figsize=(6, 6))
            colors = plt.cm.tab10.colors[:len(pie_categories)]
            wedges, texts, autotexts = plt.pie(pie_amounts, labels=pie_categories, autopct='%1.1f%%', 
                   startangle=140, colors=colors, textprops={'color': 'white'})
            plt.title('Current Month Breakdown', color='white')
            plt.gca().set_facecolor('#121212')
            plt.gcf().set_facecolor('#121212')
            # Color the labels to match their slice colors
            for i, text in enumerate(texts):
                text.set_color(colors[i % len(colors)])
            pie_file = os.path.join(static_path, 'chart.png')
            plt.savefig(pie_file, dpi=300, bbox_inches='tight')
            plt.close()
    except Exception as e:
        print(f"Error generating pie chart: {e}")

    try:
        if bar_categories and sum(bar_amounts) > 0:
            plt.figure(figsize=(8, 5))
            plt.bar(bar_categories, bar_amounts, color='skyblue')
            plt.title('Selected Period Spending', color='white')
            plt.xlabel('Category', color='white')
            plt.ylabel('Amount', color='white')
            plt.gca().set_facecolor('#121212')
            plt.gcf().set_facecolor('#121212')
            # Wrap long category names at spaces
            wrapped_labels = [textwrap.fill(cat, width=12, break_long_words=False) for cat in bar_categories]
            plt.xticks(range(len(bar_categories)), wrapped_labels, rotation=0, color='white', ha='center')
            plt.yticks(color='white')
            bar_chart_file = os.path.join(static_path, 'bar_chart.png')
            plt.savefig(bar_chart_file, dpi=300, bbox_inches='tight')
            plt.close()
    except Exception as e:
        print(f"Error generating bar chart: {e}")

    # Generate multi-year/month trend for the selected period
    try:
        # only build a trend if we actually have data at all
        if totals_by_year:
            month_totals = defaultdict(float)
            # base the range on the start/end dates the user chose
            start_month = start_date.replace(day=1)
            end_month = end_date.replace(day=1)
            
            months = []
            cur = start_month
            while cur <= end_month:
                months.append(cur)
                cur = (cur + relativedelta(months=1))
            
            for row in rows:
                try:
                    amt = float(EncryptionManager.decrypt(row[1], encryption_key))
                    d = parse_date(row[2])
                    if d and start_date <= d <= end_date:
                        m_first = d.replace(day=1)
                        month_totals[m_first] += amt
                except:
                    continue
            
            month_vals = [month_totals.get(m, 0.0) for m in months]
            labels = [m.strftime('%b %Y') for m in months]
            
            plt.figure(figsize=(12, 4))
            plt.plot(range(len(months)), month_vals, marker='o', color='skyblue')
            plt.title('Monthly Spending Trend', color='white')
            plt.xlabel('Month', color='white')
            plt.ylabel('Total Spend', color='white')
            plt.gca().set_facecolor('#121212')
            plt.gcf().set_facecolor('#121212')
            plt.xticks(range(len(months)), labels, rotation=45, color='white')
            plt.yticks(color='white')
            yearly_trend_file = os.path.join(static_path, 'yearly_trend.png')
            plt.tight_layout()
            plt.savefig(yearly_trend_file, dpi=300, bbox_inches='tight')
            plt.close()
    except Exception as e:
        print(f"Error generating yearly trend: {e}")

    current_month_total = sum(pie_amounts)
    current_month_highest = max(pie_categories, key=lambda c: pie_amounts[pie_categories.index(c)]) if pie_categories else None
    year_total = sum(year_amounts)
    year_highest = max(year_categories, key=lambda c: year_amounts[year_categories.index(c)]) if year_categories else None

    # calculate cache-busting tokens based on file modification times
    def make_token(path):
        try:
            return str(int(os.path.getmtime(path)))
        except Exception:
            return str(int(datetime.now().timestamp()))

    chart_token = make_token(pie_file) if pie_file else ''
    bar_token = make_token(bar_chart_file) if bar_chart_file else ''
    trend_token = make_token(yearly_trend_file) if yearly_trend_file else ''

    return render_template(
        'analyze.html',
        chart=os.path.basename(pie_file) if pie_file else None,
        chart_token=chart_token,
        bar_chart=os.path.basename(bar_chart_file) if bar_chart_file else None,
        bar_token=bar_token,
        total_period=sum(bar_amounts),
        highest_period=max(bar_categories, key=lambda c: bar_amounts[bar_categories.index(c)]) if bar_categories else None,
        start_date=start_date.strftime("%d-%m-%Y"),
        end_date=end_date.strftime("%d-%m-%Y"),
        selected_range=selected_range,
        current_month_total=current_month_total,
        current_month_highest=current_month_highest,
        year_total=year_total,
        year_highest=year_highest,
        yearly_trend=os.path.basename(yearly_trend_file) if yearly_trend_file else None,
        trend_token=trend_token
    )

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if not is_logged_in():
        flash("Please log in to edit expenses.", "warning")
        return redirect(url_for('login'))
    
    encryption_key = base64.b64decode(session['encryption_key'])
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT expense_date, category, amount FROM expenses WHERE id = ? AND user_id = ?", 
                   (expense_id, session['user_id']))
    expense = cursor.fetchone()

    if not expense:
        conn.close()
        flash("Expense not found.", "danger")
        return redirect(url_for('view_expenses'))

    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']

        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_to_store = date_obj.strftime("%d-%m-%Y")
        except:
            date_to_store = date

        try:
            amount_to_store = round(float(amount), 3)
        except:
            amount_to_store = amount

        # Encrypt updated data
        encrypted_date = EncryptionManager.encrypt(date_to_store, encryption_key)
        encrypted_category = EncryptionManager.encrypt(category, encryption_key)
        encrypted_amount = EncryptionManager.encrypt(str(amount_to_store), encryption_key)

        cursor.execute(
            "UPDATE expenses SET expense_date = ?, category = ?, amount = ? WHERE id = ? AND user_id = ?",
            (encrypted_date, encrypted_category, encrypted_amount, expense_id, session['user_id'])
        )
        conn.commit()
        conn.close()

        flash("Expense updated successfully!", "success")
        return redirect(url_for('view_expenses'))

    # Decrypt for display
    try:
        decrypted_date = EncryptionManager.decrypt(expense[0], encryption_key)
        parsed_date = datetime.strptime(decrypted_date, "%d-%m-%Y")
        display_date = parsed_date.strftime("%Y-%m-%d")
    except:
        display_date = ""
    
    expense_data = {
        'date': display_date,
        'category': EncryptionManager.decrypt(expense[1], encryption_key),
        'amount': EncryptionManager.decrypt(expense[2], encryption_key)
    }

    conn.close()
    return render_template('edit.html', expense=expense_data)

@app.route('/delete/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    if not is_logged_in():
        return {"error": "Unauthorized"}, 401

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", 
                   (expense_id, session['user_id']))
    conn.commit()
    conn.close()

    return {"success": True}, 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page to manage background mode"""
    if not is_logged_in():
        flash("Please log in to access settings.", "warning")
        return redirect(url_for('login'))
    
    current_setting = should_autostart()
    
    if request.method == 'POST':
        enable_background = request.form.get('background_mode') == 'yes'
        save_autostart_preference(enable_background)
        
        if enable_background:
            flash("Background mode enabled! App will run in system tray.", "success")
        else:
            flash("Background mode disabled. App will close when you close the browser.", "info")
        
        return redirect(url_for('settings'))
    
    return render_template('settings.html', background_enabled=current_setting)

# System Tray Functions
def create_image():
    """Create a simple icon for the system tray"""
    # Create a 64x64 icon with a dollar sign
    image = Image.new('RGB', (64, 64), color=(0, 120, 215))
    dc = ImageDraw.Draw(image)
    dc.text((20, 15), "$", fill=(255, 255, 255), font=None)
    return image

def open_app(icon, item):
    """Open the app in browser"""
    webbrowser.open('http://127.0.0.1:5000')

def quit_app(icon, item):
    """Quit the application"""
    icon.stop()
    os._exit(0)

def setup_system_tray():
    """Setup system tray icon with menu"""
    global tray_icon
    
    if not TRAY_AVAILABLE:
        return
    
    # Create icon
    icon_image = create_image()
    
    # Create menu
    menu = (
        item('Open Expense Tracker', open_app, default=True),
        item('Quit', quit_app)
    )
    
    # Create tray icon
    tray_icon = pystray.Icon("ExpenseTracker", icon_image, "Expense Tracker", menu)
    
    # Run in separate thread
    threading.Thread(target=tray_icon.run, daemon=True).start()

# Flask server thread
def run_flask():
    """Run Flask server"""
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False, threaded=True)

if __name__ == '__main__':
    # Running as executable
    if getattr(sys, 'frozen', False):
        print("=" * 60)
        print("Expense Tracker Starting (Executable Mode)...")
        print("=" * 60)
        print(f"Base path: {base_path}")
        print(f"Database path: {DB_PATH}")
        print(f"Database exists: {os.path.exists(DB_PATH)}")
        print(f"Template folder: {template_folder}")
        print(f"Template folder exists: {os.path.exists(template_folder)}")
        print(f"Static folder: {static_folder}")
        print(f"Static folder exists: {os.path.exists(static_folder)}")
        print("=" * 60)
        
        # Check first run
        first_run = is_first_run()
        
        if first_run:
            # Show dialog
            enable_background = show_first_run_dialog()
            save_autostart_preference(enable_background)
        else:
            enable_background = should_autostart()
        
        # Start Flask in background thread
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        
        # Wait a moment for Flask to start
        import time
        time.sleep(2)
        
        # Open browser
        webbrowser.open('http://127.0.0.1:5000')
        
        if enable_background:
            # Setup system tray and keep running
            if TRAY_AVAILABLE:
                setup_system_tray()
                # Keep main thread alive
                while True:
                    time.sleep(1)
            else:
                # No tray available, just keep Flask running
                flask_thread.join()
        else:
            # Don't run in background, wait for Flask thread
            flask_thread.join()
    
    else:
        # Running as script (development)
        print("=" * 60)
        print("Expense Tracker Starting...")
        print("=" * 60)
        print(f"Database location: {DB_PATH}")
        print("🔒 All expense data is encrypted with AES-256")
        print("Open your browser: http://127.0.0.1:5000")
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        app.run(debug=True, host='127.0.0.1', port=5000)