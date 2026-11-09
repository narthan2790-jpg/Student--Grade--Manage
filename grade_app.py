
import streamlit as st
import pandas as pd
import ollama

# Page settings
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Grade Manager")
st.write("Add students, calculate grades and view class performance.")

# Initialize student storage
if "students" not in st.session_state:
    st.session_state.students = []

# Grade calculation
def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"

# Student entry form
st.header("Add a Student")

with st.form("add_student_form"):
    name = st.text_input("Student Name")
    mark = st.number_input(
        "Student Mark",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )

    submitted = st.form_submit_button("Add Student")

    if submitted:
        if name.strip() == "":
            st.error("Please enter a student name.")
        else:
            st.session_state.students.append({
                "Name": name.strip(),
                "Mark": int(mark),
                "Grade": get_grade(int(mark))
            })
            st.success(f"{name} added successfully!")

# Display student results
st.header("Student Results")

if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)

    st.dataframe(df, use_container_width=True)

    marks = [student["Mark"] for student in st.session_state.students]

    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    st.header("Class Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Class Average", f"{average:.1f}")
    col2.metric("Highest Mark", highest)
    col3.metric("Lowest Mark", lowest)

    if st.button("Clear All Students"):
        st.session_state.students = []
        st.rerun()

else:
    st.info("No students added yet. Please add a student above.")


# AI-Powered Student Performance Analysis

st.divider()
st.header("🤖 AI Student Performance Analysis")

if st.button("Generate AI Performance Report"):

    if st.session_state.students:

        student_data = st.session_state.students

        prompt = f"""
                You are a student performance analyst.

        Analyse ONLY the student records provided below.
        Do not invent names, marks, grades or statistics.

        Student records:
        {student_data}

        Provide the following:

        1. Overall class performance.
        2. List students who need improvement using their exact names.
        3. Individual feedback for every student.
        4. Practical suggestions to improve performance.

        Important rules:
        - Mention every student exactly once.
        - Use only the marks and grades provided.
        - Do not assume any student has a different grade.
        - Be factual, positive and encouraging.
        - Clearly identify students scoring below 60.
        """

        with st.spinner("AI is analysing student performance..."):

            try:
                response = ollama.chat(
                    model="qwen2.5:3b",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                st.subheader("AI Performance Report")
                st.write(response["message"]["content"])

            except Exception as e:
                st.error(f"AI connection error: {e}")

    else:
        st.warning("Please add students before generating the report.")