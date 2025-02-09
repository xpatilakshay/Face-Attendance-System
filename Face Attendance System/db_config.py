import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Default XAMPP username
            password="",  # No password in XAMPP by default
            database="face_attendance",
            autocommit=True  # Auto-commit for queries
        )
        if conn.is_connected():
            print("✅ Database connected successfully!")
            return conn
    except mysql.connector.Error as err:
        print(f"❌ Database Connection Error: {err}")
        return None
