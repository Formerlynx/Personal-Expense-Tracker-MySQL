# Personal-Expense-Tracker
Personal expense tracker with AES-256 encryption and analytics


# 💰 Expense Tracker

A comprehensive desktop application for tracking personal expenses with powerful analytics, visualization features, and **military-grade encryption**. Built with Flask and packaged as a standalone Windows executable.

![Expense Tracker](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Encryption](https://img.shields.io/badge/Encryption-AES--256-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> 🔒 **Privacy First**: All expense data is encrypted with AES-256. Even database administrators cannot read your expenses!

> 👥 **Multi-User Ready**: Multiple people can use the app on the same computer - everyone's data stays private and encrypted separately.

---

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
  - [Running from Source](#running-from-source)
  - [Building Executable](#building-executable)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Core Functionality
- 🔐 **User Authentication** - Secure signup/login with bcrypt password hashing
- 👥 **Multi-User Support** - Multiple users can use the same application independently
- 🔒 **Data Privacy** - Each user can only access their own expenses (fully isolated)
- 🔐 **End-to-End Encryption** - All expense data encrypted in database using AES-256
- 🛡️ **Zero-Knowledge Architecture** - Expenses remain encrypted even when viewing database file directly
- ➕ **Expense Management** - Add, view, edit, and delete expenses
- 📊 **Dynamic Categories** - Create custom expense categories on-the-fly
- 💾 **Persistent Storage** - Microsoft Access database for reliable data storage

### Analytics & Visualization
- 📈 **Multi-Period Analysis**
  - Current month breakdown (pie chart)
  - Selected period spending (bar chart)
  - Year-to-date totals
  - Multi-year monthly trend (line chart)
- 🎯 **Smart Insights**
  - Highest spending category per period
  - Monthly/yearly spending comparisons
  - Automatic period calculations
- 🕐 **Flexible Time Ranges**
  - Year-to-date
  - Previous year
  - Last 3/6/12 months
  - Custom date range

### User Experience
- 🎨 **Dark Theme UI** - Easy on the eyes with modern design
- 📱 **Responsive Layout** - Works on various screen sizes
- ⚡ **Real-time Updates** - AJAX-powered delete operations
- 🔒 **Session Management** - Secure user sessions with automatic logout

---

## 🖼️ Screenshots

### Dashboard
The main interface showing expense overview and quick navigation.

### Add Expense
Simple form with date picker, category dropdown, and amount input with 3-decimal precision for Bahraini Dinar.

### Analytics Dashboard
Comprehensive visualization with:
- Current month pie chart
- Period comparison bar chart
- Year-to-date statistics
- Multi-year trend analysis

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** (tested on Python 3.8-3.11)
- **Microsoft Access Database Engine** ([Download](https://www.microsoft.com/en-us/download/details.aspx?id=54920))
- **Windows OS** (for executable; source code runs on any OS with appropriate ODBC drivers)
- **cryptography library** - For AES-256 encryption (auto-installed with requirements.txt)

### Running from Source

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   - See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed instructions
   - Your database needs a `salt` column in the users table for encryption
   - Expense fields must be TEXT type (they store encrypted data)

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser to `http://127.0.0.1:5000`
   - Create an account and start tracking!

### Building Executable

To create a standalone Windows executable:

1. **Install build dependencies**
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script**
   ```bash
   python build_executable.py
   ```
   
   Or use the batch file:
   ```bash
   simple_build.bat
   ```

3. **Find your executable**
   - Location: `dist/ExpenseTracker.exe`
   - Database automatically embedded and extracted on first run
   - User data stored in: `%LOCALAPPDATA%\ExpenseTracker`

4. **Distribute**
   - Just share `ExpenseTracker.exe`
   - No additional files needed!
   - Recipients need Microsoft Access Database Engine installed

---

## 📖 Usage

### First Time Setup

1. **Sign Up**
   - Click "Signup" on the home page
   - Enter username and password
   - Your password is securely hashed with bcrypt
   - A unique encryption key is generated from your password
   - This key encrypts all your expense data

2. **Login**
   - Use your credentials to access the system
   - Your encryption key is derived from your password
   - Session persists until logout
   - **Important**: Each user has their own isolated, encrypted data

### Adding Expenses

1. Navigate to **Add Expense**
2. Select date (defaults to today)
3. Choose existing category or create new one
4. Enter amount (supports 3 decimal places for precision)
5. Click **Add Expense**

### Viewing Expenses

- Navigate to **View Expenses**
- See all your expenses in a sortable table
- Edit or delete any expense with one click
- Date format: DD-MM-YYYY
- Amount format: X.XXX BHD

### Analyzing Spending

1. Go to **Analyze Expenses**
2. Select time range:
   - **Year to date** - Current calendar year
   - **Previous year** - Last full year
   - **Last 3/6/12 months** - Rolling period
   - **Custom range** - Pick any start/end dates

3. View insights:
   - **Current Month** - Pie chart breakdown
   - **Selected Period** - Bar chart by category
   - **Year-to-Date** - Annual totals
   - **Multi-Year Trend** - Monthly spending line chart (if data spans multiple years)

### Security

- Passwords hashed with bcrypt (industry-standard)
- Session-based authentication with secure tokens
- User-specific data isolation (SQL-level)
- **AES-256 encryption** for all expense data
- Each user has unique encryption key derived from password
- Expenses encrypted at rest - unreadable without login
- Even database administrators cannot read expense data
- Automatic session timeout on browser close
- Protection against SQL injection attacks

---

## 📁 Project Structure

```
expense-tracker/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── build_executable.py         # Automated build script
├── simple_build.bat           # Windows batch build script
│
├── Database/
│   └── expenses.accdb         # MS Access database
│
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Home page
│   ├── login.html             # Login form
│   ├── signup.html            # Registration form
│   ├── add.html               # Add expense form
│   ├── view.html              # View expenses table
│   ├── edit.html              # Edit expense form
│   └── analyze.html           # Analytics dashboard
│
├── static/
│   ├── style.css              # Custom styles
│   ├── chart.png              # Generated pie chart
│   ├── bar_chart.png          # Generated bar chart
│   └── yearly_trend.png       # Generated trend chart
│
└── dist/                      # Build output (after running build script)
    └── ExpenseTracker.exe     # Standalone executable
```

---

## 🛠️ Technologies Used

### Backend
- **Flask 3.0.0** - Web framework
- **Flask-Bcrypt 1.0.1** - Password hashing
- **cryptography 42.0.0** - AES-256 encryption for expense data
- **pyodbc 5.0.1** - Database connectivity
- **matplotlib 3.8.2** - Chart generation
- **python-dateutil** - Date calculations

### Frontend
- **Bootstrap 5.3.0** - UI framework
- **Vanilla JavaScript** - Dynamic interactions
- **HTML5/CSS3** - Structure and styling

### Database
- **Microsoft Access** - Local database storage
- **ODBC Driver** - Database connection

### Packaging
- **PyInstaller 6.3.0** - Executable creation
- **Inno Setup** (optional) - Installer creation

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id AUTOINCREMENT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    salt TEXT NOT NULL
);
```

### Expenses Table
```sql
CREATE TABLE expenses (
    id AUTOINCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    expense_date TEXT NOT NULL,        -- Encrypted
    category TEXT NOT NULL,            -- Encrypted
    amount TEXT NOT NULL,              -- Encrypted
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Encryption**: All expense fields (date, category, amount) are encrypted with AES-256  
**Date Format**: DD-MM-YYYY (encrypted before storage)  
**Amount Precision**: 3 decimal places (encrypted after rounding)  
**Key Derivation**: PBKDF2-HMAC-SHA256 with user-specific salt

---

## ⚙️ Configuration

### Changing Secret Key

Before deployment, update the Flask secret key in `app.py`:

```python
app.secret_key = 'your_secret_key_change_in_production'
```

Generate a secure random key:
```python
import secrets
print(secrets.token_hex(32))
```

### Database Password

If your Access database has a password, update it in `app.py`:

```python
def get_db_connection():
    db_password = 'password'  # Change this
    # ...
```

### Port Configuration

To change the default port (5000):

```python
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5001)  # Change port here
```

### Hide Console Window (Executable)

Edit `build_executable.py` or `.spec` file:

```python
console=False,  # Set to False to hide console
```

---

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Error
**Problem**: "ODBC Driver not found"  
**Solution**: Install Microsoft Access Database Engine
- Download from [Microsoft](https://www.microsoft.com/en-us/download/details.aspx?id=54920)
- Install matching architecture (32-bit Python → 32-bit driver)

#### Port Already in Use
**Problem**: "Address already in use: Port 5000"  
**Solution**: 
- Close other applications using port 5000
- Or change port in `app.py` (see Configuration)

#### Charts Not Displaying
**Problem**: Charts show as broken images  
**Solution**:
- Ensure `static` folder has write permissions
- For executable: Check `%LOCALAPPDATA%\ExpenseTracker\static`
- Verify matplotlib is installed: `pip install matplotlib`

#### Build Failed
**Problem**: PyInstaller build errors  
**Solution**:
```bash
# Clean previous builds
rmdir /s /q build dist
del *.spec

# Reinstall PyInstaller
pip uninstall pyinstaller
pip install pyinstaller

# Try manual build
python -m PyInstaller --onefile --add-data "templates;templates" --add-data "static;static" --add-data "Database;Database" app.py
```

#### Executable Doesn't Start
**Problem**: Double-clicking exe does nothing  
**Solution**:
- Check antivirus (may block unsigned exe)
- Run from command prompt to see errors
- Verify Visual C++ Redistributables installed

### Date Format Issues

The app handles multiple date formats internally. If you see date issues:

1. Check database date format matches DD-MM-YYYY
2. Verify input dates use YYYY-MM-DD (HTML date picker format)
3. Check `parse_date()` function in `app.py` for format handling

### Permission Errors

When running as executable:
- Database: `%LOCALAPPDATA%\ExpenseTracker\expenses.accdb`
- Charts: `%LOCALAPPDATA%\ExpenseTracker\static\`

Ensure these folders have write permissions.

---

## 🔧 Known Issues & Fixes

### Issue 1: Date Format in Edit Form
**Bug**: Edit form may show dates in wrong format  
**Status**: ✅ Fixed in latest version  
**Fix**: `edit_expense()` now normalizes dates before display

### Issue 2: Amount Precision Loss
**Bug**: Amounts may lose decimal places  
**Status**: ✅ Fixed in latest version  
**Fix**: Now rounds to 3 decimal places and formats display correctly

### Issue 3: Chart Generation on First Run
**Bug**: Charts may fail to generate on very first expense  
**Status**: ✅ Fixed in latest version  
**Fix**: Added null checks and graceful handling of empty data

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Add comments for complex logic
- Test on Windows before submitting
- Update README for new features

### Areas for Improvement

- [ ] Export to Excel/CSV
- [ ] Budget setting and alerts
- [ ] Receipt image upload
- [ ] Multi-currency support
- [ ] Mobile responsive improvements
- [ ] SQLite option (cross-platform)
- [ ] Dark/light theme toggle
- [ ] Expense search and filtering
- [ ] Recurring expenses
- [ ] Category icons

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**[Your Name]**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Flask framework and contributors
- Bootstrap team for the UI framework
- Matplotlib for visualization capabilities
- Python community for excellent libraries

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Known Issues](#known-issues--fixes)
3. Open an issue on GitHub
4. Contact: your.email@example.com

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] SQLite database option
- [ ] Export functionality (Excel, CSV, PDF)
- [ ] Budget tracking and alerts
- [ ] Receipt scanning/upload
- [ ] Mobile app version

### Version 2.1 (Future)
- [ ] Multi-user household accounts
- [ ] Shared expenses tracking
- [ ] Cloud sync option
- [ ] API for third-party integrations

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Last Updated**: March 2026  
**Version**: 1.0.0  
**Status**: Active Development
