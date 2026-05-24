import sqlite3

def create_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        marks INTEGER,
        attendance INTEGER,
        study_hours INTEGER,
        previous_score INTEGER
    )
    ''')

    conn.commit()
    conn.close()

create_db()