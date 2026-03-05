"""
Database migration script to add the missing 'salt' column to the users table.
Run this script once to fix the database schema.
"""
import os
import pyodbc
import sys

def get_db_path():
    """Get the database path based on whether running as executable or dev"""
    if getattr(sys, 'frozen', False):
        # Running as executable
        user_data_path = os.path.join(
            os.environ.get('LOCALAPPDATA', os.path.expanduser('~')),
            'ExpenseTracker'
        )
        return os.path.join(user_data_path, 'expenses.accdb')
    else:
        # Running as script
        return os.path.join(os.getcwd(), 'Database', 'expenses.accdb')

def add_salt_column():
    """Add the missing 'salt' column to the users table"""
    db_path = get_db_path()
    db_password = 'password'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        sys.exit(1)
    
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={db_path};"
        f"PWD={db_password};"
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        print(f"📊 Database location: {db_path}")
        print("🔄 Migrating database schema...")
        
        # Check if salt column already exists
        cursor.execute("SELECT * FROM users")
        columns = [description[0] for description in cursor.description]
        
        if 'salt' in columns:
            print("✅ The 'salt' column already exists. No migration needed!")
            conn.close()
            return
        
        # Add the salt column to users table
        print("➕ Adding 'salt' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN salt TEXT(255)")
        conn.commit()
        
        print("✅ Migration complete! The 'salt' column has been added successfully.")
        print("\nℹ️  WARNING: Existing user accounts will have NULL salt values.")
        print("   Users can still log in, but should reset their passwords for proper encryption.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure the database is not in use by the application")
        print("2. Check that you have the Microsoft Access Driver installed")
        print("3. Verify the database password is 'password'")
        sys.exit(1)

if __name__ == '__main__':
    add_salt_column()
