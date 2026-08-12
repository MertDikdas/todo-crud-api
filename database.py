import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=psycopg.rows.dict_row
    )

def init_database():
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    done BOOLEAN
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM tasks")
            count = cursor.fetchone()[0]

            if count == 0:
                tasks = [
                    ("Learn Python", False),
                    ("Build a PostgreSQL app", False),
                    ("Commit the project", False)
                ]

                cursor.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    tasks
                )

        connection.commit()