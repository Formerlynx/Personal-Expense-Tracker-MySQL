import os
import subprocess
import sys

# Install pymysql if not present
try:
    import pymysql
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql"])
    import pymysql

DB_NAME = "my_app_db"
DB_USER = "app_user"
DB_PASS = "SecurePassword123!"

def ensure_mysql_installed():
    """Checks if MySQL service is installed; if not, installs and starts it."""
    # Check if mysql binary exists
    result = subprocess.run(["which", "mysql"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("MySQL not detected. Installing MySQL Server...")
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        
        # Install mysql-server non-interactively
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "mysql-server"], env=env, check=True)
        
    # Ensure MySQL service is running
    status = subprocess.run(["sudo", "service", "mysql", "status"], capture_output=True, text=True)
    if "is running" not in status.stdout:
        print("Starting MySQL service...")
        subprocess.run(["sudo", "service", "mysql", "start"], check=True)

def setup_database():
    """Connects to MySQL root via socket and creates the database and user."""
    ensure_mysql_installed()
    
    # In Linux/Codespaces, local root connects via unix socket without a password
    connection = pymysql.connect(
        unix_socket='/var/run/mysqld/mysqld.sock',
        user='root',
        autocommit=True
    )

    try:
        with connection.cursor() as cursor:
            # Create Database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;")
            print(f"Database '{DB_NAME}' ensured.")

            # Create User and Grant Privileges
            cursor.execute(f"CREATE USER IF NOT EXISTS '{DB_USER}'@'localhost' IDENTIFIED BY '{DB_PASS}';")
            cursor.execute(f"GRANT ALL PRIVILEGES ON `{DB_NAME}`.* TO '{DB_USER}'@'localhost';")
            cursor.execute("FLUSH PRIVILEGES;")
            print(f"User '{DB_USER}' configured.")
            
    finally:
        connection.close()

if __name__ == "__main__":
    setup_database()
    print("Database ready for application connection.")