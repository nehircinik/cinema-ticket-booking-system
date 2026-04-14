import sqlite3
import os
from datetime import datetime

def create_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "cinema.db")
    return sqlite3.connect(db_path)

def add_booking(user_id, seat_number, booking_date, total_price):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings (user_id, session_id, seat_number, booking_date, total_price)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, 1, seat_number, booking_date, total_price))

    conn.commit()
    conn.close()

def get_user_bookings(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM bookings WHERE user_id=?
    """, (user_id,))

    bookings = cursor.fetchall()
    conn.close()
    return bookings

def get_all_bookings():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()
    return bookings