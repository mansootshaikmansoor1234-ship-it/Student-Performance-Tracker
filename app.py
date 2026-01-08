import streamlit as st
import sqlite3

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("student.db", check_same_thread=False)
cursor = conn.cursor()

# Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT
)
""")

# Attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    student_id INTEGER,
    status TEXT
)
""")

# Marks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    student_id INTEGER,
    marks INTEGER
)
""")
conn.commit()

# ---------- SIDEBAR MENU ----------
st.sidebar.title("Student App Menu")
menu = st.sidebar.radio("Go to", ["Add Student", "Mark Attendance", "Add Marks", "View Students", "Attendance %"])

# ---------- ADD STUDENT ----------
if menu == "Add Student":
    st.header("Add Student")
    sid = st.text_input("Student ID")
    name = st.text_input("Name")
    dept = st.text_input("Department")

    if st.button("Add Student"):
        if sid and name and dept:
            try:
                cursor.execute("INSERT INTO students VALUES (?, ?, ?)", (sid, name, dept))
                conn.commit()
                st.success("Student added successfully!")
            except:
                st.error("Student ID already exists!")
        else:
            st.error("Please fill all fields")

# ---------- MARK ATTENDANCE ----------
elif menu == "Mark Attendance":
    st.header("Mark Attendance")
    sid = st.text_input("Student ID for Attendance")
    status = st.selectbox("Status", ["Present", "Absent"])

    if st.button("Mark Attendance"):
        if sid:
            cursor.execute("INSERT INTO attendance VALUES (?, ?)", (sid, status))
            conn.commit()
            st.success("Attendance marked")
        else:
            st.error("Enter Student ID")

# ---------- ADD MARKS ----------
elif menu == "Add Marks":
    st.header("Add Marks")
    sid = st.text_input("Student ID for Marks")
    marks = st.text_input("Marks")

    if st.button("Add Marks"):
        if sid and marks.isdigit():
            cursor.execute("INSERT INTO marks VALUES (?, ?)", (sid, marks))
            conn.commit()
            st.success("Marks added")
        else:
            st.error("Enter valid Student ID and marks")

# ---------- VIEW STUDENTS ----------
elif menu == "View Students":
    st.header("Students List")
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            st.write(f"ID: {row[0]}, Name: {row[1]}, Dept: {row[2]}")
    else:
        st.info("No students found")

# ---------- ATTENDANCE PERCENTAGE ----------
elif menu == "Attendance %":
    st.header("Final Attendance Percentage")
    sid = st.text_input("Enter Student ID for Percentage")

    if st.button("Calculate %"):
        if sid:
            cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=?", (sid,))
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'", (sid,))
            present = cursor.fetchone()[0]

            if total == 0:
                st.info("No attendance records found")
            else:
                percentage = (present / total) * 100
                st.success(f"Attendance Percentage: {percentage:.2f}%")
        else:
            st.error("Enter Student ID")
