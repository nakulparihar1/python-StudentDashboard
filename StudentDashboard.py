import streamlit as st
import json
import pandas as pd

def load_from_file(filename="report_cards.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_to_file(students, filename="report_cards.json"):
    with open(filename, "w") as f:
        json.dump(students, f, indent=2)

def evaluate_student(marks):
    total = sum(marks.values())
    percentage = total / len(marks)
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"
    return total, percentage, grade

def show_charts(students, subjects):
    if not students:
        st.warning("No data to show charts.")
        return
    df = pd.DataFrame([s["marks"] for s in students], index=[s["name"] for s in students])
    st.subheader("📊 Subject-wise Marks Comparison")
    st.bar_chart(df)
    grades = [s["grade"] for s in students]
    grade_counts = pd.Series(grades).value_counts()
    st.subheader("📈 Grade Distribution")
    st.bar_chart(grade_counts)

def show_toppers(students):
    if not students:
        st.warning("No students found.")
        return
    toppers = sorted(students, key=lambda x: x["percentage"], reverse=True)
    st.subheader("🏆 Topper List (Top 3)")
    for i, s in enumerate(toppers[:3], start=1):
        st.write(f"{i}. {s['name']} - {s['percentage']}% ({s['grade']})")

def main():
    st.title("📊 Student Report Card Dashboard")
    SUBJECTS = ["Math", "Physics", "Chemistry", "English", "CS"]
    students = load_from_file()
    menu = st.sidebar.selectbox("Menu", ["Add Student", "View Reports", "Search Student", "Charts", "Topper List"])
    if menu == "Add Student":
        st.header("➕ Add New Student")
        name = st.text_input("Enter student name")
        marks = {}
        for sub in SUBJECTS:
            marks[sub] = st.number_input(f"Marks in {sub}", min_value=0.0, max_value=100.0, step=1.0)
        if st.button("Save Report"):
            total, percentage, grade = evaluate_student(marks)
            student = {"name": name, "marks": marks, "total": total, "percentage": percentage, "grade": grade}
            students.append(student)
            save_to_file(students)
            st.success(f"Report saved for {name} ✅")
    elif menu == "View Reports":
        st.header("📑 All Student Reports")
        if students:
            for s in students:
                st.subheader(s["name"])
                st.write(s["marks"])
                st.write(f"Total: {s['total']}, Percentage: {s['percentage']}%, Grade: {s['grade']}")
        else:
            st.warning("No records found.")
    elif menu == "Search Student":
        st.header("🔍 Search Student")
        query = st.text_input("Enter student name")
        if query:
            results = [s for s in students if s["name"].lower() == query.lower()]
            if results:
                for s in results:
                    st.subheader(s["name"])
                    st.write(s["marks"])
                    st.write(f"Total: {s['total']}, Percentage: {s['percentage']}%, Grade: {s['grade']}")
            else:
                st.error("No match found.")
    elif menu == "Charts":
        st.header("📊 Charts & Analytics")
        show_charts(students, SUBJECTS)
    elif menu == "Topper List":
        st.header("🏆 Topper Students")
        show_toppers(students)

if __name__ == "__main__":
    main()
