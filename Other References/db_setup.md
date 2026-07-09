# MySQL Database Setup Guide

🗄️ Creating and Configuring the MySQL Database

## Required Tables

Your MySQL database needs two tables: `users` and `expenses`.

### 1. Users Table

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### Field Details:
- **id**: Auto-incrementing primary key (integer)
- **username**: Unique username (plaintext, VARCHAR(255))
- **password**: Bcrypt hashed password (VARCHAR(255))
- **salt**: Base64-encoded salt for encryption key derivation (32 bytes, VARCHAR(255))

---

### 2. Expenses Table

```sql
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    expense_date VARCHAR(500) NOT NULL,
    category VARCHAR(500) NOT NULL,
    amount VARCHAR(500) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### Field Details:
- **id**: Auto-incrementing primary key (integer)
- **user_id**: Foreign key referencing `users.id`
- **expense_date**: **ENCRYPTED** - Stores encrypted date (DD-MM-YYYY format before encryption, VARCHAR(500))
- **category**: **ENCRYPTED** - Stores encrypted category name (VARCHAR(500))
- **amount**: **ENCRYPTED** - Stores encrypted amount value (VARCHAR(500))

> [!IMPORTANT]
> All expense fields (date, category, amount) are stored as encrypted strings (`VARCHAR(500)`), not as native Dates or Decimals!

---

## 📝 Setup Options

### Option 1: Automatic Initialization (Recommended)
1. Ensure your MySQL server is running.
2. Run the application (`python app.py`).
3. If it is the first run or the connection fails, the application will automatically redirect you to the **Database Setup** page at `http://127.0.0.1:5000/db-setup`.
4. Enter your MySQL host, port, username, password, and database name.
5. Click **Verify & Initialize Database**. The application will automatically create the database (if it doesn't exist) and build the required tables.

### Option 2: Manual SQL Creation
If you prefer to create the database and tables manually:
1. Log in to your MySQL server:
   ```bash
   mysql -u root -p
   ```
2. Create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS expense_tracker;
   USE expense_tracker;
   ```
3. Run the table creation statements:
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(255) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL,
       salt VARCHAR(255) NOT NULL
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

   CREATE TABLE expenses (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT NOT NULL,
       expense_date VARCHAR(500) NOT NULL,
       category VARCHAR(500) NOT NULL,
       amount VARCHAR(500) NOT NULL,
       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
   ```

---

## 🔒 Understanding the Encryption Flow

1. **User Sign Up**:
   - Password is hashed with Bcrypt (for login verification).
   - A random 32-byte salt is generated and stored in the database.
2. **User Log In**:
   - Password + Salt are passed through PBKDF2 to derive a 32-byte AES-256 key.
   - The derived key is stored in the session cookie (never persisted in the database).
3. **Data Security**:
   - Expenses are encrypted/decrypted client-side (via session key) before being sent to/read from MySQL.
   - If the MySQL database is compromised, all expense data is unreadable encrypted text.

---

## ⚙️ Configuration File (`settings.txt`)

Database configurations are saved in your settings file at `%LOCALAPPDATA%\ExpenseTracker\settings.txt` (Windows) or `~/.expensetracker/settings.txt` (Unix).

Example content:
```ini
autostart=yes
first_run_done=yes
mysql_host=localhost
mysql_port=3306
mysql_user=root
mysql_password=yourpassword
mysql_db=expense_tracker
```

Alternatively, you can configure these settings using environment variables:
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`