import sqlite3
import os

def create_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "cinema.db")
    return sqlite3.connect(db_path)


# REGISTER
def create_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "cinema.db")
    return sqlite3.connect(db_path)

def register_user(full_name, email, password, role="customer"):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (full_name, email, password, role)
    VALUES (?, ?, ?, ?)
    """, (full_name, email, password, role))

    conn.commit()
    conn.close()

def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()
    conn.close()

    return user


# LOGIN
def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()
    conn.close()

    return user