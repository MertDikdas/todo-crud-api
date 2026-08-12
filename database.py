
import sqlite3

connection = sqlite3.connect("tasks.db")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        done BOOLEAN
    )
""")

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    tasks = [
        ("Learn Python", False),
        ("Build a SQLite app", False),
        ("Commit the project", False)
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        tasks
    )

connection.commit()
connection.close()

print("Database initialized successfully.")