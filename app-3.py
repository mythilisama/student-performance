import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="au@12345678",
        database="student_db"
    )

st.title("🎓 Student Performance Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "View Students", "Update Marks", "Delete Student", "Analysis"]
)

# ADD STUDENT
if menu == "Add Student":
    st.subheader("Add Student Details")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", min_value=0, max_value=100)

    if st.button("Add Student"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, subject, marks) VALUES (%s, %s, %s, %s)",
            (name, age, subject, marks)
        )
        conn.commit()
        conn.close()
        st.success("Student added successfully!")

# VIEW STUDENTS
elif menu == "View Students":
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    if not df.empty:
        df["Result"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
        st.dataframe(df)
    else:
        st.warning("No records found")

# UPDATE MARKS
elif menu == "Update Marks":
    st.subheader("Update Student Marks")

    student_id = st.number_input("Student ID", min_value=1)
    new_marks = st.number_input("New Marks", min_value=0, max_value=100)

    if st.button("Update"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET marks=%s WHERE id=%s",
            (new_marks, student_id)
        )
        conn.commit()
        conn.close()
        st.success("Marks updated")

# DELETE STUDENT
elif menu == "Delete Student":
    st.subheader("Delete Student")

    student_id = st.number_input("Student ID", min_value=1)

    if st.button("Delete"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        conn.commit()
        conn.close()
        st.success("Student deleted")

# ANALYSIS
elif menu == "Analysis":
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    if df.empty:
        st.warning("No data available")
    else:
        st.subheader("Statistics")

        avg_marks = df["marks"].mean()
        pass_percent = (df["marks"] >= 40).mean() * 100
        top_scorer = df.loc[df["marks"].idxmax()]

        st.write("📊 Average Marks:", round(avg_marks, 2))
        st.write("✅ Pass Percentage:", round(pass_percent, 2), "%")
        st.write("🏆 Top Scorer:", top_scorer["name"])

        # Bar Chart
        st.subheader("Subject vs Average Marks")
        subject_avg = df.groupby("subject")["marks"].mean()
        plt.figure()
        subject_avg.plot(kind="bar")
        st.pyplot(plt)

        # Pie Chart
        st.subheader("Pass / Fail Ratio")
        pass_fail = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail").value_counts()
        plt.figure()
        pass_fail.plot(kind="pie", autopct="%1.1f%%")
        st.pyplot(plt)