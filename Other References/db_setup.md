 Database Setup Guide

 🗄️ Creating the Access Database with Encryption Support

 Required Tables

Your `expenses.accdb` database needs the following structure:



 1. Users Table


CREATE TABLE users (
    id AUTOINCREMENT PRIMARY KEY,
    username TEXT(255) NOT NULL UNIQUE,
    password TEXT(255) NOT NULL,
    salt TEXT(255) NOT NULL
);


 Field Details:
- id: Auto-incrementing primary key
- username: Unique username (plaintext)
- password: Bcrypt hashed password
- salt: Base64-encoded salt for encryption key derivation (32 bytes)



 2. Expenses Table


CREATE TABLE expenses (
    id AUTOINCREMENT PRIMARY KEY,
    user_id LONG NOT NULL,
    expense_date TEXT(500) NOT NULL,
    category TEXT(500) NOT NULL,
    amount TEXT(500) NOT NULL
);


 Field Details:
- id: Auto-incrementing primary key
- user_id: Foreign key to users table
- expense_date: ENCRYPTED - Stores encrypted date (DD-MM-YYYY format before encryption)
- category: ENCRYPTED - Stores encrypted category name
- amount: ENCRYPTED - Stores encrypted amount value

Important: All expense fields (date, category, amount) are stored as encrypted TEXT, not their original data types!



 📝 Step-by-Step Setup in Microsoft Access

 Option 1: Using Access GUI

1. Open Microsoft Access
2. Create New Blank Database
   - Name it: `expenses.accdb`
   - Save in: `Database/` folder in your project

3. Create Users Table
   - Click "Table Design"
   - Add fields:
     
     Field Name      Data Type       Properties
     
     id              AutoNumber      Primary Key
     username        Short Text      Field Size: 255, Required: Yes, Indexed: Yes (No Duplicates)
     password        Short Text      Field Size: 255, Required: Yes
     salt            Short Text      Field Size: 255, Required: Yes
     
   - Save as: `users`

4. Create Expenses Table
   - Click "Table Design"
   - Add fields:
     
     Field Name      Data Type       Properties
     
     id              AutoNumber      Primary Key
     user_id         Number          Field Size: Long Integer, Required: Yes
     expense_date    Short Text      Field Size: 500, Required: Yes
     category        Short Text      Field Size: 500, Required: Yes
     amount          Short Text      Field Size: 500, Required: Yes
     
   - Save as: `expenses`

5. Set Database Password (Optional but Recommended)
   - File → Info → Encrypt with Password
   - Enter password: `password` (or your chosen password)
   - Update `app.py` if you use a different password

6. Save and Close



 Option 2: Using SQL in Access

1. Open Access and create new database `expenses.accdb`
2. Go to "Create" → "Query Design"
3. Close the "Show Table" dialog
4. Click "SQL View" button
5. Paste and run each command separately:


-- Create Users Table
CREATE TABLE users (
    id AUTOINCREMENT PRIMARY KEY,
    username TEXT(255) NOT NULL,
    password TEXT(255) NOT NULL,
    salt TEXT(255) NOT NULL
);

-- Create Unique Index on Username
CREATE UNIQUE INDEX idx_username ON users(username);



-- Create Expenses Table
CREATE TABLE expenses (
    id AUTOINCREMENT PRIMARY KEY,
    user_id LONG NOT NULL,
    expense_date TEXT(500) NOT NULL,
    category TEXT(500) NOT NULL,
    amount TEXT(500) NOT NULL
);

-- Create Index on user_id for faster queries
CREATE INDEX idx_user_id ON expenses(user_id);




 🔒 Understanding the Encryption

 How It Works:

1. User Signs Up
   - Password is hashed with bcrypt (for authentication)
   - A random 32-byte salt is generated
   - Salt is stored in database (Base64 encoded)

2. User Logs In
   - Password + salt → PBKDF2 → Encryption Key
   - Encryption key stored in session (not in database)
   - Key used to encrypt/decrypt all expense data

3. Adding Expense
   - Date, category, amount → Encrypted with user's key
   - Encrypted data stored in database
   - Raw data never stored!

4. Viewing Expenses
   - Encrypted data fetched from database
   - Decrypted using user's session key
   - Displayed to user

 Security Features:

✅ Different users have different encryption keys  
✅ Each user's key derived from their password  
✅ No one can read expenses without logging in  
✅ Database admin cannot see expense data  
✅ Even if database is stolen, data is unreadable



 🔐 What's Encrypted vs Not Encrypted

 NOT Encrypted (Readable in Database):
- ❌ Usernames
- ❌ User IDs
- ❌ Password hashes (but these are one-way hashes, not reversible)
- ❌ Salt values (needed for key derivation)

 FULLY Encrypted (Unreadable in Database):
- ✅ Expense dates
- ✅ Expense categories
- ✅ Expense amounts

This means: If someone opens the Access database file directly, they will see:
- List of usernames (but not passwords)
- Gibberish encrypted text for all expenses
- No way to know what expenses are, amounts, or dates



 📊 Example Data in Database

 Users Table (as seen in Access):

id | username | password                                          | salt
|-||
1  | john     | $2b$12$KIX8Qv4t... (bcrypt hash)                   | b3BlbnNzaCB...
2  | jane     | $2b$12$mNp9Xr2w... (bcrypt hash)                   | c2VjdXJlIHN...


 Expenses Table (as seen in Access):

id | user_id | expense_date              | category                  | amount
||||
1  | 1       | Z0FBQUFBQm5... (encrypted)| Z0FBQUFBQm5... (encrypted)| Z0FBQUFBQm5... (encrypted)
2  | 1       | Z0FBQUFBQm5... (encrypted)| Z0FBQUFBQm5... (encrypted)| Z0FBQUFBQm5... (encrypted)
3  | 2       | Z0FBQUFBQm5... (encrypted)| Z0FBQUFBQm5... (encrypted)| Z0FBQUFBQm5... (encrypted)


As you can see: All expense data is completely encrypted gibberish!



 🧪 Testing the Database

After creating the database, test it:

1. Place in Project
   
   your-project/
   └── Database/
       └── expenses.accdb
   

2. Run Application
   bash
   python app.py
   

3. Create Test User
   - Go to Signup
   - Username: `testuser`
   - Password: `testpass123`

4. Add Test Expense
   - Login with test account
   - Add an expense
   - Check database in Access - you should see encrypted data!

5. Verify Encryption
   - Open `expenses.accdb` in Access
   - Look at expenses table
   - Data should be unreadable encrypted strings

6. Verify Decryption
   - Login to app
   - View expenses
   - Data should display correctly!



 🔧 Troubleshooting

 "Table 'users' does not exist"
- Ensure you created the users table exactly as specified
- Check table name is lowercase `users`

 "Column 'salt' not found"
- The salt column is required for encryption
- Add it to users table: `ALTER TABLE users ADD COLUMN salt TEXT(255);`

 "Data type mismatch"
- Ensure expense_date, category, and amount are TEXT fields, not Date/Number
- They must store encrypted strings

 Can't open database
- Verify database password in `app.py` matches your Access database password
- Check ODBC driver is installed



 🗑️ Database Maintenance

 Backup Your Database
Regular backups recommended! Copy the file:

Database/expenses.accdb → Backup/expenses_backup_[date].accdb


 Reset Database (Delete All Data)

DELETE FROM expenses;
DELETE FROM users;


 Compact Database (Reduce File Size)
In Access: File → Info → Compact & Repair Database



 ⚠️ Important Security Notes

1. Passwords are NOT reversible
   - If user forgets password, they lose access to their data
   - No password recovery possible (by design)
   - This is a security feature, not a bug!

2. Keep Database Secure
   - Set a strong database password
   - Don't share the database file
   - Keep backups in secure location

3. Multi-User Capability
   - Each user's data is isolated by user_id
   - Each user's data is encrypted with their own key
   - Users cannot access each other's expenses

4. Encryption Strength
   - AES-256 encryption (military-grade)
   - PBKDF2 with 100,000 iterations
   - Cryptographically secure random salts



 📚 Additional Resources

- [Microsoft Access Documentation](https://support.microsoft.com/en-us/access)
- [Cryptography Library Docs](https://cryptography.io/)
- [PBKDF2 Standard](https://en.wikipedia.org/wiki/PBKDF2)
- [AES Encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)