import sqlite3
import os

def create_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "cinema.db")
    return sqlite3.connect(db_path)

def add_movie(title, genre, duration, age_limit):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO movies (title, genre, duration, age_limit)
    VALUES (?, ?, ?, ?)
    """, (title, genre, duration, age_limit))

    conn.commit()
    conn.close()

def get_movies():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()

    conn.close()
    return movies