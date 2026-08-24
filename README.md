# Personal-Expense-Tracker-MySQL
Personal expense tracker with AES-256 encryption, MySQL backend, and advanced analytics


# 💰 Expense Tracker

A comprehensive desktop application for tracking personal expenses with powerful analytics, visualization features, and **military-grade encryption**. Built with Flask, backed by MySQL, and packaged as a standalone executable with system tray integration.

![Expense Tracker](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Encryption](https://img.shields.io/badge/Encryption-AES--256-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> 🔒 **Privacy First**: All expense data is encrypted with AES-256. Even database administrators cannot read your expenses!

> 👥 **Multi-User Ready**: Multiple people can use the app independently - everyone's data stays private and encrypted separately.

> 🤖 **AI Assistant**: Powered by Groq's LLMs for personalized financial insights and advice.

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
- 🛡️ **Zero-Knowledge Architecture** - Expenses remain encrypted even when viewing database
- ➕ **Expense Management** - Add, view, edit, and delete expenses
- 📊 **Dynamic Categories** - Create custom expense categories on-the-fly
- 💾 **Persistent Storage** - MySQL database for reliable data storage and multi-user support

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
- 🎨 **Dark Theme UI** - Modern design with easy-on-the-eyes interface
- 📱 **Responsive Layout** - Works on various screen sizes
- ⚡ **Real-time Updates** - AJAX-powered delete operations
- 🔒 **Session Management** - Secure user sessions with automatic logout
- 🤖 **AI Chat Assistant** - Powered by Groq's LLMs for financial insights
- 🖥️ **System Tray Integration** - Run app in background with quick access
- ⚙️ **Settings Panel** - Configure MySQL connection, background mode, and preferences

---

## 🖼️ Screenshots

### Dashboard
The main interface showing expense overview and quick navigation with login/signup.

### Add Expense
Simple form with date picker, category dropdown, and amount input with 3-decimal precision support.

### View Expenses
Table view of all expenses grouped by year-month with edit and delete functionality.

### Analytics Dashboard
Comprehensive visualization with:
- Current month pie chart breakdown
- Period comparison bar chart
- Year-to-date statistics
- Multi-year trend analysis

### Settings Panel
Configure MySQL connection and background mode preferences.

### AI Chat Assistant
Chat interface powered by Groq's LLMs for financial insights.

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** (tested on Python 3.8+)
- **MySQL Server** (5.7 or higher) - [Download](https://dev.mysql.com/downloads/mysql/)
- **OS Support**: Windows, macOS, Linux
- **cryptography library** - For AES-256 encryption (auto-installed with requirements.txt)

### Prerequisites - Quick Setup

#### Windows
1. Download MySQL Community Server from [MySQL Downloads](https://dev.mysql.com/downloads/mysql/)
2. Run the installer and complete setup
3. Note your MySQL username and password (default: `root`)

#### macOS
```bash
# Using Homebrew
brew install mysql
brew services start mysql
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install mysql-server
sudo systemctl start mysql
```

### Running from Source

1. **Clone the repository**
   ```bash
   git clone https://github.com/Formerlynx/Personal-Expense-Tracker-MySQL.git
   cd Personal-Expense-Tracker-MySQL
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

4. **Run the application**
   ```bash
   python app.py
   ```

5. **First-time setup**
   - Open your browser to `http://127.0.0.1:5000`
   - If database is not configured, you'll be redirected to the DB Setup page
   - Enter your MySQL connection details:
     - **Host**: localhost (or your MySQL server address)
     - **Port**: 3306 (default MySQL port)
     - **Username**: root (or your MySQL username)
     - **Password**: (your MySQL password, leave blank if none)
     - **Database Name**: expense_tracker (or custom name)
   - Click "Save & Test Connection"
   - Once connected, create your account and start tracking!

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

3. **Find your executable**
   - Location: `dist/ExpenseTracker.exe`
   - User data stored in: `%LOCALAPPDATA%\ExpenseTracker` (Windows) or `~/.expensetracker` (Linux/Mac)

4. **Configuration on First Run**
   - On first launch, you'll see a dialog asking about background mode
   - Choose YES to run in system tray, or NO for normal mode
   - Then configure your MySQL connection settings on the DB Setup page

---

## 📖 Usage

### Database Configuration

On first run, you'll need to configure your MySQL connection:

1. **Navigate to DB Setup Page**
   - You'll automatically be redirected if no database is connected
   - Or click the database settings icon in the navigation

2. **Enter MySQL Connection Details**
   - **Host**: MySQL server address (e.g., localhost, 127.0.0.1)
   - **Port**: MySQL port (default: 3306)
   - **Username**: MySQL user (default: root)
   - **Password**: MySQL user password
   - **Database Name**: Name for your expense database (default: expense_tracker)

3. **Save & Test Connection**
   - System will test the connection
   - If successful, database tables are created automatically
   - If failed, you'll see an error message to troubleshoot

### First Time Setup

1. **Sign Up**
   - Click "Signup" on the login page
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
- Expenses are grouped by year-month

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

### AI Chat Assistant

- Click the **Chat** icon in the navigation
- Ask questions about your spending habits
- Get personalized financial insights
- Powered by Groq's advanced LLMs
- All queries are processed securely

### Settings & Preferences

1. Navigate to **Settings**
2. **Background Mode**
   - Enable/disable background running (system tray)
   - When enabled, app runs in background after closing browser
3. **MySQL Configuration**
   - Update database connection settings
   - Test new connection before saving
   - Changes take effect immediately

### Security & Privacy

- Passwords hashed with bcrypt (industry-standard)
- Session-based authentication with secure tokens
- User-specific data isolation (SQL-level with WHERE user_id checks)
- **AES-256 encryption** for all expense data (PBKDF2 key derivation)
- Each user has unique encryption key derived from password
- Expenses encrypted at rest - unreadable without login
- Even database administrators cannot read encrypted expense data
- Automatic session timeout on browser close
- Protection against SQL injection attacks (parameterized queries)
- MySQL connection credentials securely stored
- No plain-text storage of sensitive data

---

## 📁 Project Structure

```
Personal-Expense-Tracker-MySQL/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── build_executable.py         # Automated build script
├── SETUP.md                    # Setup instructions
├── RUNNING.md                  # Running guide
├── README.md                   # This file
│
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Home page
│   ├── login.html             # Login form
│   ├── signup.html            # Registration form
│   ├── add.html               # Add expense form
│   ├── view.html              # View expenses table
│   ├── edit.html              # Edit expense form
│   ├── analyze.html           # Analytics dashboard
│   ├── db_setup.html          # Database configuration page
│   └── settings.html          # Settings and preferences
│
├── static/
│   ├── style.css              # Custom styles (dark theme)
│   ├── chart.png              # Generated pie chart
│   ├── bar_chart.png          # Generated bar chart
│   └── yearly_trend.png       # Generated trend chart
│
├── Other References/           # Documentation files
│   ├── db_setup.md
│   ├── INTEGRATION.md
│   ├── privacy_doc.md
│   └── quickstart.md
│
├── build/                      # Build artifacts (created by PyInstaller)
│   └── ExpenseTracker/
│
└── dist/                       # Distribution output (after build)
    └── ExpenseTracker.exe      # Standalone Windows executable

**Note**: User data directory:
- Windows: `%LOCALAPPDATA%\ExpenseTracker`
- Linux/Mac: `~/.expensetracker`
```

---

## 🛠️ Technologies Used

### Backend
- **Flask 3.0.0** - Web framework
- **Flask-Bcrypt 1.0.1** - Password hashing
- **MySQL Connector/Python** - MySQL database connectivity
- **cryptography 42.0.0** - AES-256 encryption for expense data
- **matplotlib 3.8.2** - Chart generation
- **python-dateutil** - Date calculations
- **OpenAI Python Client** - Groq API integration for AI chat
- **pystray** - System tray integration (Windows/Linux/macOS)

### Frontend
- **Bootstrap 5.3.0** - UI framework
- **Vanilla JavaScript** - Dynamic interactions
- **HTML5/CSS3** - Structure and styling

### Database
- **MySQL 5.7+** - Relational database backend
- **MySQL Connector/Python** - Python MySQL driver

### Packaging
- **PyInstaller 6.3.0** - Executable creation

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Expenses Table
```sql
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    expense_date VARCHAR(500) NOT NULL,        -- Encrypted (DD-MM-YYYY format)
    category VARCHAR(500) NOT NULL,            -- Encrypted
    amount VARCHAR(500) NOT NULL,              -- Encrypted (3 decimal precision)
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Encryption**: All expense fields (date, category, amount) are encrypted with AES-256  
**Date Format**: DD-MM-YYYY (encrypted before storage)  
**Amount Precision**: 3 decimal places (encrypted after rounding)  
**Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations using user-specific salt

---

## ⚙️ Configuration

### Environment Variables

You can set MySQL connection via environment variables (will override defaults):

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=yourpassword
export MYSQL_DB=expense_tracker
export MYSQL_PORT=3306
export FLASK_SECRET_KEY=your_secret_key
export GROQ_API_KEY=your_groq_api_key
```

### Groq API Key Setup

For AI chat features, obtain a Groq API key:

1. Visit [Groq Console](https://console.groq.com)
2. Create an account and generate an API key
3. Set environment variable: `GROQ_API_KEY=gsk_...`
4. Or update in `app.py` (line 21)

### Changing Flask Secret Key

Before deployment, update the Flask secret key in `app.py`:

```python
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))
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

To change the default port (5000), set the environment variable or edit `app.py`:

```bash
# Via environment variable
export FLASK_PORT=5001
```

Or in code:
```python
if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(debug=False, host='127.0.0.1', port=port)
```

---

## 🐛 Troubleshooting

### Common Issues

#### MySQL Connection Error
**Problem**: "Could not connect to MySQL server" or "Access denied for user 'root'"  
**Solution**: 
- Verify MySQL is running: `mysql -u root -p` (on command line)
- Check host, port, username, and password in DB Setup page
- Ensure MySQL has a password set (or blank password is allowed)
- Try default credentials: username=`root`, password=`` (empty)
- For fresh MySQL install on Windows: username=`root`, password=`tiger` (try this)

#### MySQL Not Running
**Problem**: "Connection refused" on port 3306  
**Solution**:
- Windows: Start MySQL Service in Services app
- macOS: `brew services start mysql`
- Linux: `sudo systemctl start mysql`

#### Database Configuration
**Problem**: Tables not created after connecting  
**Solution**:
- Ensure MySQL user has CREATE privileges
- Try again via DB Setup page
- Check MySQL user has access to the specified database

#### Port Already in Use
**Problem**: "Address already in use: Port 5000"  
**Solution**: 
- Close other applications using port 5000
- Or change port: `export FLASK_PORT=5001`
- Or modify in `app.py`

#### Charts Not Displaying
**Problem**: Charts show as broken images  
**Solution**:
- Ensure `static` folder has write permissions
- For executable: Check `%LOCALAPPDATA%\ExpenseTracker\static\` (Windows) or `~/.expensetracker/static` (Linux/Mac)
- Verify matplotlib is installed: `pip install matplotlib`
- Restart the app after fixing permissions

#### Build Failed
**Problem**: PyInstaller build errors  
**Solution**:
```bash
# Clean previous builds
rm -rf build dist *.spec  # Linux/Mac
# or
rmdir /s /q build dist && del *.spec  # Windows

# Reinstall dependencies
pip install --upgrade -r requirements.txt
pip install --upgrade pyinstaller

# Try build again
python build_executable.py
```

#### Executable Doesn't Start
**Problem**: Double-clicking exe does nothing  
**Solution**:
- Check antivirus (may block unsigned exe)
- Run from command prompt to see errors: `ExpenseTracker.exe`
- Check error log in `%LOCALAPPDATA%\ExpenseTracker\`

#### AI Chat Not Working
**Problem**: Chat feature returns empty or error  
**Solution**:
- Verify Groq API key is set: `export GROQ_API_KEY=gsk_...`
- Check internet connection (required for API calls)
- Ensure API key is valid at [Groq Console](https://console.groq.com)
- Check app console for error messages

#### System Tray Not Appearing
**Problem**: System tray icon doesn't show  
**Solution**:
- Background mode is only available on systems with display (not headless)
- Choose "No" for background mode if running in headless environment
- On Linux, ensure you have a display server (X11 or Wayland)

### Date Format Issues

The app handles multiple date formats internally. If you see date issues:

1. Check database date format matches DD-MM-YYYY when viewing
2. Input dates use YYYY-MM-DD (HTML date picker format)
3. Amounts stored with 3 decimal precision

### Permission Errors

When running as executable, ensure write permissions:
- Windows: `%LOCALAPPDATA%\ExpenseTracker\` folder
- Linux/Mac: `~/.expensetracker/` folder

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
   ```
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic, especially encryption/decryption
- Test on both Windows and Unix-like systems before submitting
- Update README for new features
- Ensure all database changes are backward-compatible
- Test with headless environment if adding UI features
- Maintain encryption standards (AES-256) for sensitive data

### Areas for Improvement

- [ ] Export to Excel/CSV with filters
- [ ] Budget setting and spending alerts
- [ ] Receipt image upload and attachment
- [ ] Multi-currency support with conversion rates
- [ ] Expense search and advanced filtering
- [ ] Recurring expenses automation
- [ ] Expense categorization suggestions using AI
- [ ] Dark/light theme toggle
- [ ] Category icons and custom colors
- [ ] Mobile app or better mobile-responsive UI
- [ ] Data backup and restore functionality
- [ ] Import expenses from CSV/Excel
- [ ] Spending goals and progress tracking
- [ ] Expense sharing between users
- [ ] PDF report generation
- [ ] Calendar view for expenses
- [ ] Multi-language support
- [ ] Suggestions for better UX welcome!

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 Verghese George Keenalil

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

**[Verghese Keenalil]**
- GitHub: [@Formerlynx](https://github.com/Formerlynx)
- Email: verghese.keenalil@gmail.com

---

## 🙏 Acknowledgments

- Flask framework and contributors
- Bootstrap team for the UI framework
- Matplotlib for visualization capabilities
- MySQL database team
- Groq for powerful LLM API
- cryptography library for security
- pystray for system tray integration
- Python community for excellent libraries
- All contributors and users providing feedback

---

## 📞 Support

If you encounter any issues or have questions:

1. Open an issue on GitHub
2. Contact: verghese.keenalil@gmail.com
3. Keep in mind might take a bit of time, still in school and is new to git

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Last Updated**: August 2026  
**Version**: 2.0.0  
**Status**: Active Development  
**Database**: MySQL 5.7+ (migrated from Microsoft Access)
