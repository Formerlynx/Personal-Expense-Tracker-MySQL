from datetime import datetime, timedelta
import os
import random
import base64
from bcrypt import hashpw, gensalt

from app import EncryptionManager, get_db_connection

DEMO_USERNAME = "demo_user"
DEMO_PASSWORD = "DemoPassword123!"

def seed_demo_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Clean up existing demo user
    cursor.execute("SELECT id FROM users WHERE username = %s", (DEMO_USERNAME,))
    user = cursor.fetchone()
    if user:
        cursor.execute("DELETE FROM expenses WHERE user_id = %s", (user['id'],))
        cursor.execute("DELETE FROM users WHERE id = %s", (user['id'],))

    # 2. Create Demo User
    salt_bytes = os.urandom(32)
    password_hash = hashpw(DEMO_PASSWORD.encode(), gensalt()).decode('utf-8')
    salt_b64 = base64.b64encode(salt_bytes).decode('utf-8')

    cursor.execute(
        "INSERT INTO users (username, password, salt) VALUES (%s, %s, %s)",
        (DEMO_USERNAME, password_hash, salt_b64)
    )
    user_id = cursor.lastrowid

    encryption_key = EncryptionManager.derive_key(DEMO_PASSWORD, salt_bytes)

    # 3. Sample categories and ranges
    category_ranges = {
        'Groceries': (15.50, 120.00),
        'Utilities': (25.00, 75.00),
        'Dining': (8.25, 45.00),
        'Entertainment': (7.00, 20.00),
        'Transport': (5.00, 18.00),
        'Healthcare': (3.50, 30.00)
    }

    today = datetime.now()
    expenses_to_insert = []

    for _ in range(40):
        days_ago = random.randint(1, 355)
        expense_date = today - timedelta(days=days_ago)

        category = random.choice(list(category_ranges.keys()))
        min_amt, max_amt = category_ranges[category]
        amount_val = f"{random.uniform(min_amt, max_amt):.2f}"

        enc_date = EncryptionManager.encrypt(
            expense_date.strftime('%d-%m-%Y'), encryption_key
        )
        enc_category = EncryptionManager.encrypt(category, encryption_key)
        enc_amount = EncryptionManager.encrypt(amount_val, encryption_key)

        expenses_to_insert.append((
            user_id,
            enc_category,
            enc_amount,
            enc_date
        ))

    # Insert into database
    query = """
        INSERT INTO expenses (user_id, category, amount, expense_date)
        VALUES (%s, %s, %s, %s)
    """

    cursor.executemany(query, expenses_to_insert)
    conn.commit()
    cursor.close()
    conn.close()
    print("Demo account successfully created and populated!")

if __name__ == "__main__":
    seed_demo_data()