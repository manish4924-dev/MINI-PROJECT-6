import json
import csv
import os
from datetime import datetime

JSON_FILE = "students.json"
CSV_FILE = "students.csv"
LOG_FILE = "activity_log.txt"

SUBJECTS = ["Python", "Maths", "DBMS"]

data_safe = True

def write_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {message}\n")

def load_students():
    global data_safe

    if not os.path.exists(JSON_FILE):
        return {}

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid student data format.")

        return data

    except (json.JSONDecodeError, ValueError) as error:
        data_safe = False
        print("Error loading JSON file:", error)
        print("Original file will be preserved.")
        return {}

def save_students(students):
    if not data_safe:
        print("Saving disabled because the existing JSON file has an error.")
        return False

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)

    return True

def get_marks(subject):
    while True:
        try:
            marks = float(input(f"Enter {subject} marks: "))

            if 0 <= marks <= 100:
                return marks
            else:
                print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter numeric marks.")

def add_student(students):
    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if student_id in students:
        print("Student ID already exists!")
        return

    name = input("Enter Student Name: ").strip()
    department = input("Enter Department: ").strip()

    if not name or not department:
        print("Name and department cannot be empty.")
        return

    marks = {}

    for subject in SUBJECTS:
        marks[subject] = get_marks(subject)

    students[student_id] = {
        "name": name,
        "department": department,
        "marks": marks
    }

    if save_students(students):
        write_log(f"Student {student_id} added.")
        print("Student record saved successfully!")

def update_student(students):
    student_id = input("Enter Student ID to update: ").strip()

    if student_id not in students:
        print("Student not found!")
        return

    print("Enter updated student details.")

    name = input("Enter new name: ").strip()
    department = input("Enter new department: ").strip()

    if not name or not department:
        print("Name and department cannot be empty.")
        return

    marks = {}

    for subject in SUBJECTS:
        marks[subject] = get_marks(subject)

    students[student_id] = {
        "name": name,
        "department": department,
        "marks": marks
    }

    if save_students(students):
        write_log(f"Student {student_id} updated.")
        print("Record updated successfully!")

def display_students(students):
    if not students:
        print("No student records found.")
        return

    print("========== ALL STUDENT RECORDS ==========\n")

    for student_id, details in students.items():
        print("\nStudent ID:", student_id)
        print("Name:", details["name"])
        print("Department:", details["department"])

        for subject, marks in details["marks"].items():
            print(subject, ":", marks)

def search_student(students):
    student_id = input("Enter Student ID to search: ").strip()

    if student_id in students:
        details = students[student_id]

        print("Student Found!\n")
        print("Student ID:", student_id)
        print("Name:", details["name"])
        print("Department:", details["department"])

        for subject, marks in details["marks"].items():
            print(subject, ":", marks)

    else:
        print("Student not found!")

def export_csv(students):
    if not students:
        print("No records available for export.")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Name",
            "Department",
            "Python",
            "Maths",
            "DBMS"
        ])

        for student_id, details in students.items():
            writer.writerow([
                student_id,
                details["name"],
                details["department"],
                details["marks"]["Python"],
                details["marks"]["Maths"],
                details["marks"]["DBMS"]
            ])

    write_log("Student records exported to CSV.")
    print("CSV export completed successfully!")

def json_string_demo(students):
    if not students:
        print("No records available.")
        return

    student_id = input("Enter Student ID: ").strip()

    if student_id not in students:
        print("Student not found!")
        return

    json_text = json.dumps(students[student_id], indent=4)

    print("JSON String:\n")
    print(json_text)

    python_object = json.loads(json_text)

    print("Python Object:\n")
    print(python_object)

def view_log():
    if not os.path.exists(LOG_FILE):
        print("Activity log does not exist.")
        return

    print("1. Read using read()\n")
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        print(file.read())

    print("2. Read using readline()\n")
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        print(file.readline())

    print("3. Read using readlines()\n")
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
        print(lines)

def text_file_demo():
    filename = "text_demo.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("Student Records System\n")

    lines = [
        "Python File Handling\n",
        "JSON Data Storage\n",
        "CSV Export\n"
    ]

    with open(filename, "a", encoding="utf-8") as file:
        file.writelines(lines)

    print("Text file created using write() and writelines().")

def main():

    students = load_students()

    while True:

        print("===== STUDENT RECORDS MANAGEMENT SYSTEM =====")

        print("1. Add Student")
        print("2. Update Student")
        print("3. Display All Students")
        print("4. Search Student")
        print("5. Export Records to CSV")
        print("6. JSON String Operations")
        print("7. View Activity Log")
        print("8. Text File Demonstration")
        print("9. Exit")

        choice = input("Enter your choice: \n").strip()

        if choice == "1":
            add_student(students)

        elif choice == "2":
            update_student(students)

        elif choice == "3":
            display_students(students)

        elif choice == "4":
            search_student(students)

        elif choice == "5":
            export_csv(students)

        elif choice == "6":
            json_string_demo(students)

        elif choice == "7":
            view_log()

        elif choice == "8":
            text_file_demo()

        elif choice == "9":
            print("Thank you for using Student Records System!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()