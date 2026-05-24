import sqlite3

conn = sqlite3.connect('students.db')

conn.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marks INTEGER,
    attendance INTEGER,
    study_hours INTEGER,
    previous_score INTEGER,
    subject TEXT
)
''')

conn.commit()
conn.close()

print("Data added Successfully!")