import sqlite3

from config import DATABASE_FILE


def create_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    return conn
