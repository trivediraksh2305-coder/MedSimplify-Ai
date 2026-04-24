# utils/auth.py

import sqlite3
import bcrypt
import os

os.makedirs('database', exist_ok=True)
DB_PATH = 'database/users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password, email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )
    try:
        cursor.execute(
            "INSERT INTO users VALUES (NULL,?,?,?,CURRENT_TIMESTAMP)",
            (username, hashed, email)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, password FROM users WHERE username=?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        # Returns user_id if password correct
        if bcrypt.checkpw(password.encode('utf-8'), result[1]):
            return result[0]  # return user id
    return None