# database/db.py

import sqlite3
import json
from datetime import datetime

DB_PATH = 'reports.db'


def get_connection():
    """Create and return a database connection"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """Initialize the database with all required tables"""
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Reports table (original)
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            report_name TEXT,
            report_text TEXT,
            simplified_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Chat history table (new)
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            report_id INTEGER,
            message_role TEXT,
            message_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (report_id) REFERENCES reports (id)
        )
    ''')

    conn.commit()
    conn.close()


# 🔥 IMPORTANT: AUTO CREATE TABLES WHEN FILE LOADS
init_db()


def save_report(user_id, report_name, report_text, simplified_text):
    """Save a report and return its ID"""
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        INSERT INTO reports (user_id, report_name, report_text, simplified_text)
        VALUES (?, ?, ?, ?)
    ''', (user_id, report_name, report_text, simplified_text))

    report_id = c.lastrowid
    conn.commit()
    conn.close()
    return report_id


def get_user_reports(user_id):
    """Get all reports for a user"""
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        SELECT report_name, simplified_text, created_at, id
        FROM reports
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,))

    reports = c.fetchall()
    conn.close()
    return reports


def get_report_by_id(report_id, user_id):
    """Get a specific report by ID"""
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        SELECT id, report_name, report_text, simplified_text, created_at
        FROM reports
        WHERE id = ? AND user_id = ?
    ''', (report_id, user_id))

    report = c.fetchone()
    conn.close()

    if report:
        return {
            'id': report[0],
            'name': report[1],
            'report_text': report[2],
            'simplified_text': report[3],
            'created_at': report[4]
        }
    return None


def save_chat_message(user_id, report_id, role, content):
    """Save a chat message to the database"""
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        INSERT INTO chat_history (user_id, report_id, message_role, message_content)
        VALUES (?, ?, ?, ?)
    ''', (user_id, report_id, role, content))

    conn.commit()
    conn.close()


def get_chat_history(report_id, user_id):
    """Get all chat messages for a report"""
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        SELECT message_role, message_content, created_at
        FROM chat_history
        WHERE report_id = ? AND user_id = ?
        ORDER BY created_at ASC
    ''', (report_id, user_id))

    messages = c.fetchall()
    conn.close()

    chat_history = []
    for msg in messages:
        chat_history.append({
            'role': msg[0],
            'content': msg[1],
            'timestamp': msg[2]
        })

    return chat_history


def delete_chat_history(report_id, user_id):
    """Delete all chat messages for a report"""
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        DELETE FROM chat_history
        WHERE report_id = ? AND user_id = ?
    ''', (report_id, user_id))

    conn.commit()
    conn.close()