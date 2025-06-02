
import sqlite3
from database import create_connection, create_tables

def initialize_database():
    conn = create_connection()
    if conn:
        create_tables(conn)
        conn.close()
        print("Database initialized with new schema.")
    else:
        print("Failed to initialize database.")

if __name__ == "__main__":
    initialize_database()