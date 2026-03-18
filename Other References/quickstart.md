# ⚡ Quick Start Guide

Get your encrypted expense tracker running in 5 minutes!

---

## 🚀 For Users (Using Executable)

### Download & Run

1. **Download files from GitHub Releases:**
   - `ExpenseTracker.exe`
   - `expenses_template.accdb`

2. **Create folder structure:**
   ```
   MyExpenseTracker/
   ├── ExpenseTracker.exe
   └── Database/
       └── expenses.accdb (rename from expenses_template.accdb)
   ```

3. **Double-click `ExpenseTracker.exe`**
   - Browser opens automatically
   - Go to: `http://127.0.0.1:5000`

4. **Create account**
   - Click "Signup"
   - Choose username and **strong password**
   - **Remember password** (no recovery possible!)

5. **Start tracking!** 🎉

---

## 💻 For Developers (From Source)

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/expense-tracker.git
cd expense-tracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Database

**Option A: Use Template**
```bash
copy Database\expenses_template.accdb Database\expenses.accdb
```

**Option B: Create from Scratch**
- See [DATABASE_SETUP.md](DATABASE_SETUP.md)

### 5. Run Application

```bash
python app.py
```

Open browser: `http://127.0.0.1:5000`

---

## 🏗️ Building Executable

```bash
# Install PyInstaller (if not already)
pip install pyinstaller

# Run build script
python build_executable.py

# Find executable
cd dist
ExpenseTracker.exe
```

---

## 🔒 Encryption Quick Test

### Verify Data is Encrypted:

1. **Add an expense**
   - Date: Today
   - Category: Food
   - Amount: 10.500

2. **Open database in Access**
   ```
   Database/expenses.accdb
   ```

3. **Check expenses table**
   - You should see: `gAAAAABn...` (encrypted gibberish)
   - NOT: `Food` or `10.500`

4. **Go back to app**
   - Your expense displays correctly!
   - This proves encryption/decryption works ✅

---

## 👥 Multi-User Quick Test

1. **Create User 1**
   - Username: `alice`
   - Password: `alice123!`
   - Add expense: "Groceries, 50 BHD"

2. **Logout and Create User 2**
   - Username: `bob`  
   - Password: `bob456!`
   - Add expense: "Gas, 30 BHD"

3. **Login as Alice**
   - See only: "Groceries, 50 BHD"
   - Bob's expense is hidden ✅

4. **Login as Bob**
   - See only: "Gas, 30 BHD"
   - Alice's expense is hidden ✅

**Privacy verified!** 🎉

---

## ⚙️ Configuration

### Change Database Password

In `app.py`:
```python
def get_db_connection():
    db_password = 'your_password_here'  # Change this
```

### Change Port

In `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5001)  # Change port
```

### Change Secret Key

In `app.py`:
```python
app.secret_key = 'your_secret_key_here'  # Change this
```

Or use environment variable:
```bash
set FLASK_SECRET_KEY=your_secret_key
```

---

## 🐛 Troubleshooting

### "Database driver not found"
**Solution:** Install Microsoft Access Database Engine
- [Download](https://www.microsoft.com/en-us/download/details.aspx?id=54920)

### "Port 5000 already in use"
**Solution:** Change port in app.py to 5001

### "Cannot open database"
**Solution:** Check database password matches in app.py

### Charts not showing
**Solution:** Ensure matplotlib is installed
```bash
pip install matplotlib
```

### Build fails
**Solution:** Clean and rebuild
```bash
rmdir /s /q build dist
del *.spec
python build_executable.py
```

---

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Review [PRIVACY_AND_SECURITY.md](PRIVACY_AND_SECURITY.md) to understand encryption
- Check [DATABASE_SETUP.md](DATABASE_SETUP.md) for database details
- See [GITHUB_SETUP.md](GITHUB_SETUP.md) for uploading to GitHub

---

## 🎯 Common Tasks

### Add Expense
1. Click "Add Expense"
2. Select date (or use today)
3. Choose category or create new
4. Enter amount (supports 3 decimals)
5. Click "Add Expense"

### View Expenses
1. Click "View Expenses"
2. See all your expenses in table
3. Edit or Delete as needed

### Analyze Spending
1. Click "Analyze Expenses"
2. Select time range (YTD, Last 3 months, Custom, etc.)
3. View charts and statistics

### Logout
1. Click "Logout" button
2. Your session ends
3. Data remains encrypted on disk

---

## 🔐 Security Reminders

⚠️ **Important**:
- Choose **strong passwords** (12+ characters)
- **Remember passwords** - no recovery possible
- **Lock computer** when stepping away
- **Backup database** regularly
- **Each user** has separate encrypted data

✅ **What's Protected**:
- All expense dates ✅
- All categories ✅
- All amounts ✅
- Even from database admins ✅

---

## 💡 Tips

1. **Use password manager** (LastPass, 1Password, Bitwarden)
2. **Create categories early** (they auto-complete later)
3. **Check analytics monthly** (track spending trends)
4. **Backup database weekly** (copy expenses.accdb)
5. **Lock app when done** (click Logout)

---

## 📞 Get Help

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/expense-tracker/issues)
- **Security**: Email privately (don't post publicly)
- **Docs**: Check README.md and wiki

---

**Ready to track expenses securely? Let's go! 🚀🔒**