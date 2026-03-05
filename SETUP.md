# 🔧 Complete Setup Guide - Expense Tracker

This guide will walk you through the complete setup of the Expense Tracker application.

## Prerequisites

### System Requirements
- **Windows 7** or later (or macOS/Linux for development)
- **Python 3.9+** (for running from source)
- **At least 500 MB** free disk space
- **Microsoft Access** (optional - for manual database creation)

### For Running from Source
You'll need Python 3.9 or newer installed on your system.

## Installation Options

### Option 1: Run from Source (Recommended for Development)

This is the recommended approach if you want to modify the code or run the latest version.

#### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repo-url> expense-tracker
cd expense-tracker

# Or download and extract the ZIP file
```

#### Step 2: Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**What Gets Installed:**
- `flask==3.0.0` - Web framework
- `matplotlib==3.8.2` - Chart generation
- `pyodbc==5.0.1` - Database connection
- `flask-bcrypt==1.0.1` - Password hashing
- `bcrypt==4.1.2` - Cryptography
- `python-dateutil==2.8.2` - Date utilities
- `cryptography==42.0.0` - AES-256 encryption
- `pystray==0.19.5` - System tray integration
- `Pillow==10.2.0` - Image processing
- `pyinstaller==6.3.0` - Executable creation

#### Step 4: Verify Database Folder

Ensure the database folder exists:

```bash
# The Database folder should already exist with expenses.accdb
# If not, create it:
mkdir Database
```

#### Step 5: Run the Application

```bash
# With virtual environment activated:
python app.py
```

The app will:
- Start Flask server on `http://127.0.0.1:5000`
- Show first-run dialog (Windows only with pystray)
- Automatically open your browser
- Wait for you to create an account

---

### Option 2: Run as Standalone Executable (For End Users)

Users can run the pre-built executable without Python installed.

#### Step 1: Download Files

Download from releases:
- `ExpenseTracker.exe` - The application
- Database folder (optional - app creates it automatically)

#### Step 2: Create Folder Structure

You can run `ExpenseTracker.exe` directly, and it will:
- Create `%LOCALAPPDATA%\ExpenseTracker` folder
- Store database and settings there
- Keep data persistent across runs

Or manually create:
```
C:\Users\YourUsername\AppData\Local\ExpenseTracker\
```

#### Step 3: Run the Executable

**Double-click `ExpenseTracker.exe`**

The app will:
1. Check if this is first run
2. Ask about background mode preference
3. Start Flask server
4. Open browser automatically
5. Save preference for next time

---

## Database Setup

### Automatic Setup (Recommended)

If you're using the executable, the database is bundled and copied automatically.

### Manual Setup (Development)

If you need to create the database manually:

#### Option A: Use Template
```bash
# Copy the template database
copy Database\expenses_template.accdb Database\expenses.accdb
```

#### Option B: Create from Scratch
See `db_setup.md` for detailed database creation instructions.

#### Required Tables

Your database must have:

**users table:**
- `id` (AutoIncrement, Primary Key)
- `username` (Text, Unique, Required)
- `password` (Text, Required) - Bcrypt hashed
- `salt` (Text, Required) - Base64 encoded salt

**expenses table:**
- `id` (AutoIncrement, Primary Key)
- `user_id` (Integer, Foreign Key)
- `expense_date` (Text, Required) - AES-256 encrypted
- `category` (Text, Required) - AES-256 encrypted
- `amount` (Text, Required) - AES-256 encrypted

---

## Configuration

### Flask Settings (app.py)

Key settings you might want to customize:

```python
# Database password (default: 'password')
db_password = 'password'

# Flask port (default: 5000)
app.run(port=5000)

# Flask host (default: 127.0.0.1 - local only)
app.run(host='127.0.0.1')
```

### Paths Configuration

The app automatically handles paths for both development and executable:

```python
# Development: Uses project folder
# Executable: Uses %LOCALAPPDATA%\ExpenseTracker

# Templates: <base_path>/templates
# Static: <base_path>/static
# Database: <base_path>/Database/expenses.accdb (dev)
# Database: %LOCALAPPDATA%\ExpenseTracker/expenses.accdb (exe)
```

---

## First Run Configuration

### What Happens on First Run?

1. **First-Run Dialog** (Executable Mode)
   - Asks: "Run in background?"
   - YES: App runs in system tray
   - NO: App closes with browser

2. **Account Creation**
   - Create username and password
   - Password cannot be recovered!
   - Choose strong password

3. **Database Initialization**
   - Database created if doesn't exist
   - Automatic on executable mode
   - Manual setup for development

### Changing Settings Later

Access Settings page while logged in:
- Click "Settings" in navigation
- Change background mode preference
- Save and restart app

---

## Troubleshooting Setup

### Issue: "Database not found"

**Solution:**
```bash
# Check Database folder exists
ls Database/

# Should see: expenses.accdb

# If missing, copy template:
copy Database\expenses_template.accdb Database\expenses.accdb
```

### Issue: "Module not found" or Import Errors

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Port 5000 already in use"

**Solution:**

The app will automatically try to use the same port. If you need to change it:

1. Edit `app.py`
2. Change the port in the `if __name__ == '__main__'` block
3. Update browser access URL

```bash
# Example: Change to port 8000
python app.py  # Browser will access 127.0.0.1:8000
```

### Issue: "Microsoft Access Driver not found"

**Solution:**

This is needed for database access:

1. Install Microsoft Access Database Engine
   - Download from Microsoft
   - Or install Office (includes driver)
   - Or use different database (code modification needed)

### Issue: "pystray module not available" (Windows)

This only affects system tray features:

**On Windows:**
- System tray should work if PIL/Pillow is installed
- Run: `pip install Pillow --upgrade`

**On macOS/Linux:**
- System tray may not work
- App still functions normally
- Use browser to access app

---

## Development Setup

### For Developers Extending the App

#### Structure

```
expense-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Database/
│   └── expenses.accdb     # SQLite database
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   ├── view.html
│   ├── edit.html
│   ├── analyze.html
│   ├── login.html
│   ├── signup.html
│   └── settings.html
├── static/
│   └── style.css          # CSS styling
└── build_executable.py    # PyInstaller build script
```

#### Adding Features

1. **New Routes:** Add to `app.py`
2. **New Templates:** Add to `templates/`
3. **Styling:** Update `static/style.css`
4. **Database:** Modify database schema and EncryptionManager

#### Testing

```bash
# Run with debug mode
python -m flask --app app run --debug

# Or directly:
python app.py
```

---

## Building Executable

### Prerequisites

```bash
pip install pyinstaller
```

### Build Process

```bash
# Create executable
python build_executable.py

# Or use PyInstaller directly
pyinstaller ExpenseTracker.spec

# Find executable in:
dist/ExpenseTracker.exe
```

### What Gets Included

The executable includes:
- All Python code
- All templates and static files
- Database template
- All dependencies (embeds Python runtime)

### Distribution

1. Package `ExpenseTracker.exe`
2. Users download and run
3. App creates its own folder in AppData
4. Everything self-contained!

---

## Next Steps

1. **Complete Setup:** Follow setup steps above
2. **Create Account:** Sign up from home page
3. **Add Expenses:** Use "Add Expense" button
4. **View Analytics:** Check spending patterns
5. **Configure:** Visit Settings page
6. **Backup:** Keep database backed up regularly

---

## Support & Documentation

- **Privacy:** See `privacy_doc.md`
- **Database:** See `db_setup.md`
- **Quickstart:** See `quickstart.md`
- **License:** See `LICENSE`

---

**Last Updated:** March 2026
