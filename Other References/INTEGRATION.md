# 🔗 Complete Integration Guide - Expense Tracker

This document explains how all files in the Expense Tracker project work together seamlessly.

---

## Project Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     EXPENSE TRACKER APP                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────┐         ┌──────────────────────┐   │
│  │   Flask Server      │◄────────┤   Web Browser        │   │
│  │   (app.py)          │         │   http://127.0.0.1   │   │
│  │   - Routing         │         │   :5000              │   │
│  │   - Auth            │         └──────────────────────┘   │
│  │   - Encryption      │                                    │
│  │   - Charts          │         ┌──────────────────────┐   │
│  └──────────┬──────────┘         │  System Tray (pystray)   │
│             │                    │  - Background Mode   │   │
│             │                    │  - Quick Access      │   │
│             │                    └──────────────────────┘   │
│             │                                                │
│  ┌──────────▼───────────────────┐  ┌──────────────────────┐ │
│  │   Database Connection        │  │  Data Files          │ │
│  │   (pyodbc + Access)          │  │  - Templates/        │ │
│  │                              │  │  - Static/CSS        │ │
│  │  ┌──────────────────────┐    │  │  - Settings          │ │
│  │  │   expenses.accdb     │    │  └──────────────────────┘ │
│  │  │  ┌───────────────┐   │    │                           │
│  │  │  │ users table   │   │    │  ┌──────────────────────┐ │
│  │  │  │ expenses table│   │    │  │ Encryption Manager   │ │
│  │  │  └───────────────┘   │    │  │ - AES-256 Encryption │ │
│  │  │ (All data encrypted) │    │  │ - PBKDF2 Key Deriv.  │ │
│  │  └──────────────────────┘    │  └──────────────────────┘ │
│  └──────────────────────────────┘                           │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Supporting Libraries & Features              │  │
│  │ - matplotlib (Chart generation)                       │  │
│  │ - flask-bcrypt (Password hashing)                    │  │
│  │ - cryptography (Encryption)                          │  │
│  │ - PIL/Pillow (Image processing - tray icon)         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure & Connections

### Core Application (`app.py`)

**What it does:**
- Initializes Flask web server
- Manages all routes (signup, login, add, view, edit, delete, analyze)
- Handles database connections
- Manages encryption/decryption
- Controls system tray integration
- Generates analytics charts

**Connections to other files:**
```
app.py
├─ imports Database/expenses.accdb (database connection)
├─ imports templates/*.html (renders web pages)
├─ imports static/style.css (styling)
├─ imports requirements.txt (dependencies)
└─ imports build_executable.py (for executable creation)
```

**Key Functions:**
- `get_db_connection()` → Opens database
- `EncryptionManager` → Encrypts/decrypts data
- `setup_system_tray()` → Creates system tray icon
- Route handlers (`@app.route`) → Handle web requests

---

### Web Templates (`templates/` folder)

All templates inherit from `base.html` and extend it with specific content.

#### `base.html` - Base Template
**Purpose:** Master template with header, navigation, footer

**Connections:**
- Links to `static/style.css` for styling
- Contains Flask session checks for login state
- Flash message display (success/error messages)

**Used by all other templates:**
```
base.html
├─ index.html (home page)
├─ login.html (authentication)
├─ signup.html (authentication)
├─ add.html (new expense)
├─ view.html (list expenses)
├─ edit.html (modify expense)
├─ analyze.html (charts & analytics)
└─ settings.html (app configuration)
```

#### Individual Templates

| Template | Purpose | Data Flow |
|----------|---------|-----------|
| `index.html` | Home/Dashboard | Shows welcome & navigation |
| `login.html` | User Authentication | POSTs credentials to `/login` |
| `signup.html` | Account Creation | POSTs username/password to `/signup` |
| `add.html` | Add Expense Form | POSTs expense data to `/add` |
| `view.html` | Display Expenses | GETs from `/view`, DELETEs via AJAX |
| `edit.html` | Modify Expense | GETs data from `/edit/<id>`, POSTs updates |
| `analyze.html` | Charts & Analytics | GETs from `/analyze`, displays chart images |
| `settings.html` | Configuration | POSTs settings to `/settings` |

---

### Static Files (`static/` folder)

#### `style.css` - Styling
**What it contains:**
- Dark theme CSS (matches `#0f0f0f` background)
- Component styling (buttons, forms, tables, cards)
- Animation effects
- Responsive design rules
- Print styles

**Used by:** All HTML templates via `base.html`

---

### Database (`Database/` folder)

#### `expenses.accdb` - Main Database

**Structure:**

```
expenses.accdb (Microsoft Access Database)
│
├─ users table
│  ├─ id (Primary Key)
│  ├─ username (Unique)
│  ├─ password (Bcrypt hashed)
│  └─ salt (Base64 encoded for encryption derivation)
│
└─ expenses table
   ├─ id (Primary Key)
   ├─ user_id (Foreign Key → users.id)
   ├─ expense_date (AES-256 Encrypted)
   ├─ category (AES-256 Encrypted)
   └─ amount (AES-256 Encrypted)
```

**Encryption System:**

```
┌─────────────────────────────────────┐
│ User enters password                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ Step 1: Password verification       │
│ - Compare with bcrypt hash          │
│ - Stored in users.password          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ Step 2: Derive encryption key       │
│ - Get salt from users.salt          │
│ - Use PBKDF2 with password + salt   │
│ - Creates 32-byte AES-256 key       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ Step 3: Encrypt/Decrypt data        │
│ - Use Fernet (uses AES-256)         │
│ - Encrypt before storing            │
│ - Decrypt when retrieving           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ Stored in database as encrypted     │
│ "gAAAAABm2jLWoEzVf..." (gibberish) │
└─────────────────────────────────────┘
```

---

### Configuration Files

#### `requirements.txt` - Python Dependencies
**Purpose:** Lists all Python packages needed

**Dependencies:**
```
flask==3.0.0                    # Web framework
matplotlib==3.8.2               # Chart generation
pyodbc==5.0.1                   # Database driver
flask-bcrypt==1.0.1             # Password hashing
bcrypt==4.1.2                   # Crypto library
python-dateutil==2.8.2          # Date utilities
cryptography==42.0.0            # AES-256 encryption
pystray==0.19.5                 # System tray
Pillow==10.2.0                  # Image processing
pyinstaller==6.3.0              # Executable builder
```

**How it's used:**
```bash
pip install -r requirements.txt
# Installs all packages into virtual environment
```

#### `build_executable.py` - Executable Builder
**Purpose:** Creates standalone `ExpenseTracker.exe`

**Process:**
```
build_executable.py
│
├─ Creates PyInstaller spec file
│
├─ Includes in executable:
│  ├─ Entire Python runtime
│  ├─ All Python packages
│  ├─ templates/ folder
│  ├─ static/ folder
│  ├─ Database/expenses.accdb
│  └─ app.py
│
└─ Outputs → dist/ExpenseTracker.exe
```

**Usage:**
```bash
python build_executable.py
# Or directly:
pyinstaller ExpenseTracker.spec
```

---

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview & features |
| `SETUP.md` | Detailed installation guide |
| `RUNNING.md` | How to run the application |
| `quickstart.md` | 5-minute quick start |
| `db_setup.md` | Database creation guide |
| `privacy_doc.md` | Security & encryption details |
| `LICENSE` | MIT License |

---

## Data Flow Diagrams

### Adding an Expense

```
User Browser
    │
    ├─ Visits /add
    │    │
    │    └─> app.py route handler
    │         ├─ Checks if logged in
    │         ├─ Renders add.html template
    │         └─ Sends categories from database
    │
    ├─ Fills form & submits
    │    │
    │    └─> POST to /add
    │         │
    │         ├─ Validates data
    │         │
    │         ├─ Encrypts with user's key
    │         │  ├─ Gets encryption key from session
    │         │  └─ Encrypts date, category, amount
    │         │
    │         ├─ Stores encrypted data in database
    │         │
    │         └─ Redirect to /view
    │
    └─ Sees expense in list (decrypted for display)
```

### Viewing Expenses

```
User Browser
    │
    ├─ Visits /view
    │    │
    │    └─> app.py route handler
    │         ├─ Checks if logged in
    │         ├─ Queries database (WHERE user_id = current_user)
    │         ├─ Retrieves encrypted expense records
    │         │
    │         ├─ Decrypts for display
    │         │  ├─ Gets encryption key from session
    │         │  └─ Decrypts date, category, amount
    │         │
    │         ├─ Renders view.html template
    │         └─ Passes decrypted expenses to template
    │
    └─ Sees readable expenses with Edit/Delete buttons
```

### Analyzing Expenses

```
User Browser
    │
    ├─ Visits /analyze
    │    │
    │    └─> app.py route handler
    │         ├─ Checks if logged in
    │         ├─ Queries all user's expenses
    │         │
    │         ├─ Decrypts all for processing
    │         │
    │         ├─ Groups by category & date
    │         │
    │         ├─ Generates charts using matplotlib
    │         │  ├─ Pie chart (current month)
    │         │  ├─ Bar chart (selected period)
    │         │  └─ Trend chart (multi-year)
    │         │
    │         ├─ Saves charts as PNG images
    │         │  └─ Stored in static/ folder
    │         │
    │         ├─ Renders analyze.html template
    │         └─ Passes chart filenames
    │
    └─ Sees visualizations with data insights
```

---

## Execution Flow for Executable

When user double-clicks `ExpenseTracker.exe`:

```
1. Executable launcher starts
   │
   ├─ Checks if running as frozen (executable)
   │
   ├─ Gets user data path
   │  └─ C:\Users\[Username]\AppData\Local\ExpenseTracker\
   │
   ├─ Checks for database
   │  ├─ If exists: Use it
   │  └─ If not: Copy from embedded template
   │
   ├─ Is this first run?
   │  ├─ YES:
   │  │   ├─ Show dialog: "Run in background?"
   │  │   └─ Save preference to settings.txt
   │  │
   │  └─ NO:
   │      └─ Load saved preference
   │
   ├─ Start Flask server in background thread
   │  └─ http://127.0.0.1:5000
   │
   ├─ Wait for Flask to initialize
   │
   ├─ Open browser automatically
   │
   ├─ Should run in background?
   │  ├─ YES:
   │  │   └─ Setup system tray icon
   │  │       ├─ Show in taskbar
   │  │       ├─ Right-click menu
   │  │       └─ Keep Flask running
   │  │
   │  └─ NO:
   │      └─ Keep main thread alive
   │          while Flask runs
   │
   └─ User sees browser window with app running
```

---

## Background Mode Flow

```
System Tray Integration
│
├─ pystray library creates system tray icon
│  └─ Icon: Blue square with "$" symbol
│
├─ User right-clicks icon
│  │
│  ├─ Menu option 1: "Open Expense Tracker"
│  │  └─ Opens browser to http://127.0.0.1:5000
│  │
│  └─ Menu option 2: "Quit"
│     └─ Stops Flask server and exits
│
├─ Flask server keeps running in background
│  ├─ Accessible 24/7 at http://127.0.0.1:5000
│  ├─ Can open multiple browser windows
│  └─ Database stays locked to single user
│
└─ User can close browser anytime
   └─ App continues running in background
```

---

## Security Architecture

### Multi-Layer Protection

```
Layer 1: Authentication
├─ Username + Password
├─ bcrypt hashing (one-way)
└─ Verified on every login

   ↓

Layer 2: Authorization
├─ Session-based authentication
├─ User ID stored in session
├─ All queries filtered by user ID
└─ Cannot see other users' data

   ↓

Layer 3: Encryption
├─ User's password + salt → Encryption key
├─ All sensitive fields encrypted
├─ AES-256 (military-grade)
└─ Data unreadable without password

   ↓

Layer 4: Data Isolation
├─ Each user has separate key
├─ Database stores only encrypted data
├─ Even admins cannot read user data
└─ Zero-knowledge architecture
```

---

## File Modifications & Extensions

### Adding a New Route

**Steps:**
1. Edit `app.py`
2. Add route handler:
```python
@app.route('/mynewroute', methods=['GET', 'POST'])
def my_new_route():
    if not is_logged_in():
        return redirect(url_for('login'))
    # Your code here
    return render_template('mynewroute.html')
```
3. Create `templates/mynewroute.html`
4. Restart app

### Adding a New Template

**Steps:**
1. Create `templates/mytemplate.html`
2. Start with:
```html
{% extends "base.html" %}
{% block title %}My Page Title{% endblock %}
{% block content %}
<!-- Your content here -->
{% endblock %}
```
3. Link from other templates
4. Create corresponding route in `app.py`

### Customizing Styles

**Edit:** `static/style.css`

**Cascades to all templates through:**
```html
<!-- in base.html -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

---

## Troubleshooting Connections

### "Cannot find database"
**Check:**
1. `Database/` folder exists
2. `expenses.accdb` file present
3. Database path correct in app.py
4. Permissions allow read/write

### "Template not found"
**Check:**
1. Template file in `templates/` folder
2. Correct filename in `render_template()`
3. No typos in filename

### "Static files not loading"
**Check:**
1. Files in `static/` folder
2. Correct stylesheet link in base.html
3. Flask server restarted
4. Browser cache cleared (Ctrl+Shift+Delete)

### "Encryption errors"
**Check:**
1. Encryption key in session
2. Salt retrieved from database
3. Password matches encrypted hash
4. Cryptography package installed

---

## Performance Optimization

### Database Queries
- Uses WHERE clause to filter by user_id
- Reduces data transferred
- Faster decryption

### Chart Generation
- Charts cached as PNG files
- Generated once, reused
- Delete `static/*.png` to regenerate

### Session Management
- Encryption key stored in Flask session
- Not recomputed on every request
- Cleared on logout

---

## Deployment Considerations

### Development
- Run from source with `python app.py`
- Uses development Flask server
- Debug mode available

### Production (Executable)
- Self-contained package
- No Python installation needed
- Settings stored per-user
- Database auto-initialized

### Local Network Access
- Change `host='127.0.0.1'` to `host='0.0.0.0'`
- Access from other computers
- Use with caution (network security)

---

## Summary of Connections

```
┌─────────────┐
│  Browser    │  User Interface
└──────┬──────┘
       │ HTTP
┌──────▼──────┐
│  app.py     │  Business Logic
│  (Flask)    │  
└──────┬──────┘
       │ SQL (encrypted)
┌──────▼──────────────┐
│ expenses.accdb      │  Data Storage
│ (Access Database)   │
└─────────────────────┘
       │ Imports
┌──────▼──────────────┐
│ templates/          │  Frontend
│ static/             │  Styling
└─────────────────────┘
       │ Uses
┌──────▼──────────────┐
│ requirements.txt    │  Dependencies
│ (packages list)     │
└─────────────────────┘
```

All files work together to create a secure, encrypted expense tracking application that:
- ✅ Protects user data with encryption
- ✅ Runs locally (no cloud)
- ✅ Works as desktop app or web app
- ✅ Supports multiple users
- ✅ Provides analytics & insights

---

**Last Updated:** March 2026
**Version:** 1.0
