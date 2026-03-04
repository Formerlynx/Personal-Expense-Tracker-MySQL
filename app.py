from flask import Flask, render_template, request, redirect, url_for, session, flash
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for executables
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import os
import sys
import pyodbc
import shutil
import base64
import secrets
from flask_bcrypt import Bcrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

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
                print(f"First run detected. Creating database at: {db_path}")
                shutil.copy2(template_db, db_path)
                print("Database initialized successfully!")
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
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))
bcrypt = Bcrypt(app)

# Initialize database path
DB_PATH = initialize_database()

def get_db_connection():
    db_password = 'password'
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={DB_PATH};"
        f"PWD={db_password};"
    )
    return pyodbc.connect(conn_str)

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
        
        # Generate unique salt for this user
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
            
            # Derive encryption key from password
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
    
    # Get encryption key from session
    encryption_key = base64.b64decode(session['encryption_key'])

    # Fetch and decrypt existing categories
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
        
        # Validate inputs
        if not category:
            flash("Category cannot be empty.", "danger")
            conn.close()
            return redirect(url_for('add_expense'))
        
        if rounded_amount <= 0:
            flash("Amount must be greater than zero.", "danger")
            conn.close()
            return redirect(url_for('add_expense'))

        # Encrypt all expense data
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
    
    # Get encryption key
    encryption_key = base64.b64decode(session['encryption_key'])

    cursor.execute("SELECT id, expense_date, category, amount FROM expenses WHERE user_id = ?", 
                   (session['user_id'],))
    rows = cursor.fetchall()

    expenses = []
    for row in rows:
        try:
            # Decrypt expense data
            date_str = EncryptionManager.decrypt(row[1], encryption_key)
            category_str = EncryptionManager.decrypt(row[2], encryption_key)
            amount_str = EncryptionManager.decrypt(row[3], encryption_key)
            
            # Format amount
            try:
                amount_val = float(amount_str)
                amount_formatted = f"{amount_val:.3f}"
            except:
                amount_formatted = amount_str
            
            expenses.append({
                'id': row[0], 
                'date': date_str, 
                'category': category_str, 
                'amount': amount_formatted
            })
        except Exception as e:
            print(f"Error decrypting expense {row[0]}: {e}")
            continue

    conn.close()
    return render_template('view.html', expenses=expenses)

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
    if getattr(sys, 'frozen', False):
        static_path = os.path.join(get_user_data_path(), 'static')
    else:
        static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    pie_file = None
    bar_chart_file = None
    yearly_trend_file = None

    try:
        if pie_categories and sum(pie_amounts) > 0:
            plt.figure(figsize=(6, 6))
            plt.pie(pie_amounts, labels=pie_categories, autopct='%1.1f%%', 
                   startangle=140, textprops={'color': 'white'})
            plt.title('Current Month Breakdown', color='white')
            plt.gca().set_facecolor('#121212')
            plt.gcf().set_facecolor('#121212')
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
            plt.xticks(color='white')
            plt.yticks(color='white')
            bar_chart_file = os.path.join(static_path, 'bar_chart.png')
            plt.savefig(bar_chart_file, dpi=300, bbox_inches='tight')
            plt.close()
    except Exception as e:
        print(f"Error generating bar chart: {e}")

    # Generate multi-year trend if applicable
    try:
        if len(totals_by_year) > 1:
            month_totals = defaultdict(float)
            min_year = min(totals_by_year.keys())
            max_year = max(totals_by_year.keys())
            
            start_month = datetime(min_year, 1, 1).date()
            end_month = datetime(max_year, 12, 1).date()
            
            months = []
            cur = start_month
            while cur <= end_month:
                months.append(cur)
                cur = (cur + relativedelta(months=1))
            
            for row in rows:
                try:
                    amt = float(EncryptionManager.decrypt(row[1], encryption_key))
                    d = parse_date(row[2])
                    if d:
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

    return render_template(
        'analyze.html',
        chart=os.path.basename(pie_file) if pie_file else None,
        bar_chart=os.path.basename(bar_chart_file) if bar_chart_file else None,
        total_period=sum(bar_amounts),
        highest_period=max(bar_categories, key=lambda c: bar_amounts[bar_categories.index(c)]) if bar_categories else None,
        start_date=start_date.strftime("%d-%m-%Y"),
        end_date=end_date.strftime("%d-%m-%Y"),
        selected_range=selected_range,
        current_month_total=current_month_total,
        current_month_highest=current_month_highest,
        year_total=year_total,
        year_highest=year_highest,
        yearly_trend=os.path.basename(yearly_trend_file) if yearly_trend_file else None
    )

@app.route('/static/<path:filename>')
def serve_static(filename):
    if getattr(sys, 'frozen', False):
        static_path = os.path.join(get_user_data_path(), 'static')
        from flask import send_from_directory
        return send_from_directory(static_path, filename)
    else:
        return app.send_static_file(filename)

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

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        import webbrowser
        import threading
        
        def open_browser():
            import time
            time.sleep(1.5)
            webbrowser.open('http://127.0.0.1:5000')
        
        threading.Thread(target=open_browser).start()
    
    print("=" * 60)
    print("Expense Tracker Starting...")
    print("=" * 60)
    if getattr(sys, 'frozen', False):
        print(f"Database location: {DB_PATH}")
        print(f"Your data is safely stored at: {get_user_data_path()}")
    print("🔒 All expense data is encrypted with AES-256")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    # Minor update for contribution tracking
    app.run(debug=False, host='127.0.0.1', port=5000)