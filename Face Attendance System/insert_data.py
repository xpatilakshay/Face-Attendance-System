from db_config import connect_db

data = [
    (1, "Akshay Patil", "Robotics", 2017, 7, "G", 4, "2025-02-08 00:54:34"),
    (2, "Rohan Patil", "Economics", 2021, 12, "B", 1, "2025-02-08 00:54:34"),
    (3, "Elon Musk", "Physics", 2020, 7, "G", 2, "2025-02-08 00:54:34")
]

conn = connect_db()
if conn is None:
    print("Error: Failed to connect to the database.")
    exit()

cursor = conn.cursor()

try:
    cursor.executemany("""
        INSERT INTO students (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    print("Data Inserted Successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    conn.close()