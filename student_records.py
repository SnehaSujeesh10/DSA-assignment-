"""
Student Record Management System
A menu-driven console application to add, view, search, update and delete
student records. Data is stored in a JSON file so it persists between runs.
"""

import json
import os

DATA_FILE = "students.json"


# ---------- File I/O ----------
def load_records():
    """Load records from the JSON file. Returns an empty dict if no file/corrupt file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting with empty records.")
        return {}
    except OSError as error:
        print(f"File error while reading: {error}")
        return {}


def save_records(records):
    """Write all records to the JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(records, file, indent=4)
    except OSError as error:
        print(f"File error while saving: {error}")


# ---------- Input helpers (exception handling) ----------
def get_non_empty(prompt):
    """Keep asking until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Try again.")


def get_marks(prompt):
    """Keep asking until the user enters a number between 0 and 100."""
    while True:
        try:
            marks = float(input(prompt))
            if 0 <= marks <= 100:
                return marks
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# ---------- Core operations ----------
def add_record(records):
    student_id = get_non_empty("Enter student ID: ")
    if student_id in records:
        print("A record with this ID already exists.")
        return
    records[student_id] = {
        "name": get_non_empty("Enter name: "),
        "course": get_non_empty("Enter course: "),
        "marks": get_marks("Enter marks (0-100): "),
    }
    save_records(records)
    print("Record added successfully.")


def print_record(student_id, data):
    print(f"ID: {student_id} | Name: {data['name']} | "
          f"Course: {data['course']} | Marks: {data['marks']}")


def view_records(records):
    if not records:
        print("No records found.")
        return
    print("\n--- All Records ---")
    for student_id, data in records.items():
        print_record(student_id, data)


def search_record(records):
    keyword = get_non_empty("Enter ID or name to search: ").lower()
    found = False
    for student_id, data in records.items():
        if keyword == student_id.lower() or keyword in data["name"].lower():
            print_record(student_id, data)
            found = True
    if not found:
        print("No matching record found.")


def update_record(records):
    student_id = get_non_empty("Enter ID of record to update: ")
    if student_id not in records:
        print("Record not found.")
        return
    print("Press Enter to keep the current value.")
    data = records[student_id]
    new_name = input(f"Name [{data['name']}]: ").strip()
    new_course = input(f"Course [{data['course']}]: ").strip()
    new_marks = input(f"Marks [{data['marks']}]: ").strip()
    if new_name:
        data["name"] = new_name
    if new_course:
        data["course"] = new_course
    if new_marks:
        try:
            value = float(new_marks)
            if 0 <= value <= 100:
                data["marks"] = value
            else:
                print("Marks out of range; kept old value.")
        except ValueError:
            print("Invalid marks; kept old value.")
    save_records(records)
    print("Record updated.")


def delete_record(records):
    student_id = get_non_empty("Enter ID of record to delete: ")
    if student_id not in records:
        print("Record not found.")
        return
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == "y":
        del records[student_id]
        save_records(records)
        print("Record deleted.")
    else:
        print("Deletion cancelled.")


# ---------- Menu ----------
def show_menu():
    print("\n===== Student Record Management =====")
    print("1. Add record")
    print("2. View all records")
    print("3. Search record")
    print("4. Update record")
    print("5. Delete record")
    print("6. Exit")


def main():
    records = load_records()
    actions = {
        "1": add_record,
        "2": view_records,
        "3": search_record,
        "4": update_record,
        "5": delete_record,
    }
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(records)
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram interrupted. Exiting.")
