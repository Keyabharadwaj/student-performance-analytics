from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import Flask, render_template, request
import pandas as pd
from model import model
import sqlite3
import webbrowser
import threading

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"   # IMPORTANT (fixes session error)

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        if user == 'admin' and pwd == '1234':
            session['user'] = user
            return redirect('/dashboard')
        else:
            return "Invalid Login"

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    print("Fetched Data:", data)
    conn.close()

    return render_template('dashboard.html', data=data)


# ---------------- ADD STUDENT ----------------
@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        marks = int(request.form['marks'])
        attendance = int(request.form['attendance'])
        study_hours = int(request.form['study_hours'])
        previous_score = int(request.form['previous_score'])
        subject = request.form['subject']
        # 🔹 PRINT 1 (after getting form data)
        print("Form Data:", marks, attendance, study_hours, previous_score, subject)
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO students (marks, attendance, study_hours, previous_score, subject)
            VALUES (?, ?, ?, ?, ?)
        ''', (marks, attendance, study_hours, previous_score, subject))

        conn.commit()

                # 🔹 PRINT 2 (after insert)
        print("Insert Successful!")
        # 🔥 ADD THIS PART (PREDICTION)
        import numpy as np
        prediction = model.predict([[marks, attendance, study_hours, previous_score]])

        result = "Pass" if prediction[0] == 1 else "Fail"
        print("Prediction:", result)

        # 🔥 FETCH DATA AGAIN FOR TABLE
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()

        conn.close()

        # 🔥 RETURN WITH RESULT + DATA (IMPORTANT)
        return render_template('dashboard.html', data=data, result=result)

    except Exception as e:
        return f"Error: {e}"
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        student_id = request.form['id']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
        result = cursor.fetchall()

        conn.close()

        return render_template('dashboard.html', data=result)

    return redirect('/dashboard')

@app.route('/subject-analysis')
def subject_analysis():
    data = pd.read_csv('dataset/student_data.csv')

    subject_avg = data.groupby('Subject')['Marks'].mean()

    labels = list(subject_avg.index)
    values = list(subject_avg.values)

    return render_template('dashboard.html',
                           labels=labels,
                           values=values,
                           tables=data.to_html(classes='table table-bordered'))

@app.route('/predict', methods=['POST'])
def predict():
    marks = int(request.form['marks'])
    attendance = int(request.form['attendance'])
    study_hours = int(request.form['study_hours'])
    previous_score = int(request.form['previous_score'])

    prediction = model.predict([[marks, attendance, study_hours, previous_score]])

    alert = ""
    if marks < 40:
        alert = "⚠️ Student is weak!"

    return render_template('dashboard.html',
                           prediction_text=f"Prediction: {prediction[0]}",
                           alert=alert)

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

@app.route('/download-report')
def download_report():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 1")
    student = cursor.fetchone()

    conn.close()

    # 🔥 HANDLE EMPTY CASE
    if not student:
        return "No data available!"

    # Extract data
    id, marks, attendance, study_hours, previous_score, subject = student

    # 🔥 ADD PREDICTION LOGIC
    prediction = model.predict([[marks, attendance, study_hours, previous_score]])
    result = "Pass" if prediction[0] == 1 else "Fail"

    # Create PDF
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Student Performance Report", styles['Title']))
    content.append(Spacer(1, 10))

    # 🔥 ADD REAL DATA
    content.append(Paragraph(f"Student ID: {id}", styles['Normal']))
    content.append(Paragraph(f"Marks: {marks}", styles['Normal']))
    content.append(Paragraph(f"Attendance: {attendance}", styles['Normal']))
    content.append(Paragraph(f"Study Hours: {study_hours}", styles['Normal']))
    content.append(Paragraph(f"Previous Score: {previous_score}", styles['Normal']))
    content.append(Paragraph(f"Subject: {subject}", styles['Normal']))
    content.append(Paragraph(f"Prediction: {result}", styles['Normal']))

    doc.build(content)

    return send_file("report.pdf", as_attachment=True)   

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))                      

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000) 