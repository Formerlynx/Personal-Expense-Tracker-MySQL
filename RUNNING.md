# ▶️ How to Run the Expense Tracker

Quick step-by-step instructions to get the app running.

## Quick Start (5 minutes)

### For Users with Python

```bash
# 1. Navigate to the project folder
cd "C:\Users\YourUsername\Downloads\CS PROJECT"

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Browser opens automatically → `http://127.0.0.1:5000`

### For Windows Users (Executable)

✅ **Easiest Option**

1. Download `ExpenseTracker.exe`
2. Double-click it
3. Browser opens automatically
4. Select background mode preference
5. Done! Create account and start tracking

---

## Detailed Instructions

### Running from Source Code

#### On Windows

```batch
@echo off
REM Navigate to project
cd /d "C:\Users\YourUsername\Downloads\CS PROJECT"

REM Create virtual environment (first time only)
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies (first time only)
pip install -r requirements.txt

REM Run the app
python app.py

REM Press Ctrl+C to stop
```

#### On macOS/Linux

```bash
#!/bin/bash

# Navigate to project
cd ~/Downloads/CS\ PROJECT

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the app
python3 app.py

# Press Ctrl+C to stop
```

#### What You Should See

```
============================================================
Expense Tracker Starting...
============================================================
Database location: C:\Users\...\Database\expenses.accdb
🔒 All expense data is encrypted with AES-256
Open your browser: http://127.0.0.1:5000
Press Ctrl+C to stop the server
============================================================
```

Browser automatically opens → Sign up or log in

---

## Using the Application

### First Time Using the App

1. **Create Account**
   - Click "Signup" button
   - Enter username (will be used for login)
   - Enter strong password (cannot be recovered!)
   - Click "Create Account"

2. **Configure Settings** (Recommended)
   - Click "Settings" in navigation
   - Choose background mode:
     - ✅ **Background:** App runs in system tray
     - ⏹️ **Normal:** App closes with browser
   - Click "Save Settings"

3. **Start Tracking**
   - Click "Add Expense"
   - Fill in date, category, amount
   - Click "Add Expense"

### Key Features

#### Add Expense
- **Date:** When the expense occurred
- **Category:** Type or select existing category
- **Amount:** Cost (decimal accepted)

#### View Expenses
- See all your expenses in table
- Click "Edit" to modify
- Click "Delete" to remove
- Only your expenses shown!

#### Analyze Spending
- See spending by category (pie chart)
- View spending over time (bar chart)
- Filter by time period
- See monthly trends

#### Settings
- Toggle background mode
- Choose single-run or always-background
- Information about accessing the app

---

## Background Mode (System Tray)

### What is Background Mode?

Your app continues running even after closing the browser.

### Enable Background Mode

1. Open Settings page
2. Select "Run in Background (Recommended)"
3. Save Settings
4. Restart the app

### Accessing the App with Background Mode

**From System Tray:**
1. Look for **💙$** icon in bottom-right corner
2. If hidden, click ^ arrow near clock
3. Click the icon to open browser
4. Or right-click for menu options

**From Browser:**
- Anytime, open: `http://127.0.0.1:5000`
- App must be running in background
- Keep bookmark for quick access!

### Quitting Background Mode

**Option 1: System Tray**
- Right-click the **💙$** icon
- Click "Quit"

**Option 2: Task Manager**
- Press `Ctrl + Shift + Esc`
- Find "ExpenseTracker.exe"
- Click "End Task"

**Option 3: Command Line**
```bash
taskkill /IM ExpenseTracker.exe /F
```

---

## Accessing from Other Computers

### Local Network Access

By default, the app only works on **localhost** (same computer).

To access from another computer on your network:

#### Step 1: Edit app.py
```python
# Change this line:
app.run(host='127.0.0.1', port=5000)

# To this:
app.run(host='0.0.0.0', port=5000)
```

#### Step 2: Find Your Computer's IP

**On Windows:**
```bash
ipconfig
# Look for "IPv4 Address" (e.g., 192.168.1.100)
```

**On macOS/Linux:**
```bash
ifconfig
# Look for "inet" address (e.g., 192.168.1.100)
```

#### Step 3: Access from Other Computer

Open browser on another device:
```
http://192.168.1.100:5000
```

Replace `192.168.1.100` with your computer's IP from step 2.

⚠️ **Security Note:** This exposes the app to local network - use only for trusted networks!

---

## Troubleshooting

### App Won't Start

**"ModuleNotFoundError: No module named 'flask'"**

Solution:
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies again
pip install -r requirements.txt
```

### Port Already in Use

**"Address already in use"**

Either:
1. Close other app using port 5000
2. Change Flask port in app.py
3. Wait a moment and try again

### Browser Won't Open

Manual access:
1. Check command line shows Flask is running
2. Open browser
3. Type: `http://127.0.0.1:5000`
4. Press Enter

### Database Connection Error

**Check database exists:**
```bash
# Should show expenses.accdb
dir Database\

# If missing:
copy Database\expenses_template.accdb Database\expenses.accdb
```

### Can't Find System Tray Icon

1. Click ^ arrow in bottom-right corner
2. Look for **💙$** icon
3. Not showing? Make sure background mode is enabled
4. Restart app to reinitialize

### Encrypted Data Shows as Gibberish

✅ **This is correct!** Your data IS encrypted.

- Database shows: `gAAAAABm2jLWoEzVf...` (encrypted)
- Browser shows: "Food" (decrypted with your password)
- This proves encryption works!

---

## Quick Access Shortcuts

### Create Desktop Shortcut

**For Executable:**
1. Right-click desktop
2. New → Shortcut
3. Location: `C:\full\path\to\ExpenseTracker.exe`
4. Name: "Expense Tracker"
5. Finish

**For Python Script:**
1. Create batch file `run_expense_tracker.bat`:
```batch
@echo off
cd /d "C:\path\to\CS PROJECT"
call venv\Scripts\activate
python app.py
```
2. Right-click on batch file
3. Send to → Desktop (create shortcut)

### Keyboard Shortcuts

- `Ctrl + C` - Stop the server (while running)
- `Ctrl + Shift + Esc` - Open Task Manager
- `F5` - Refresh browser page
- `F12` - Open browser developer tools

---

## Backup Your Data

### Why Backup?

Your expenses are encrypted and stored locally. Backup protects against:
- Computer failure
- Accidental deletion  
- File corruption

### How to Backup

**Executable Mode:**
```bash
# Backup location:
copy %LOCALAPPDATA%\ExpenseTracker\expenses.accdb backup_location\
```

**Development Mode:**
```bash
# Backup location:
copy Database\expenses.accdb backup_expenses.accdb
```

### Restore from Backup

Simply replace the corrupted database with your backup.

---

## Performance Tips

### Reduce CPU Usage

1. Disable background mode if not needed
2. Close browser when not using
3. Restart app weekly
4. Avoid leaving open unnecessary time

### Speed Up Charts

Charts are generated on-the-fly:
- First chart load takes ~2-3 seconds
- Subsequent loads cached
- To refresh: F5 in browser

### Database Maintenance

- Old expenses don't affect speed
- App handles large datasets well
- Tested with 10,000+ expenses

---

## Keep App Updated

### Check for Updates

```bash
# Check latest from source
git pull origin main
```

### Update Dependencies

```bash
# Activate virtual environment
venv\Scripts\activate

# Update all packages
pip install -r requirements.txt --upgrade
```

---

## Uninstall Instructions

### Clean Uninstall

```bash
# Remove virtual environment
rmdir /s /q venv

# Remove project folder
rmdir /s /q "CS PROJECT"

# Remove AppData (keeps your data!)
rmdir /s %LOCALAPPDATA%\ExpenseTracker
```

### Keep Your Data

Before uninstalling:
```bash
# Backup database
copy %LOCALAPPDATA%\ExpenseTracker\expenses.accdb backup_location\
```

---

## Need Help?

- **Setup Issues?** See `SETUP.md`
- **Database Help?** See `db_setup.md`
- **Quick Start?** See `quickstart.md`
- **Security Info?** See `privacy_doc.md`

---

**Happy Tracking! 💰🔒**
