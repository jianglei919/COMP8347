"""
COMP 8347 - Lab #2, Part 2
Author: LEI JIANG

A simple program to manage students' grades.
Data is persisted in a text file (class_grades.txt) with the format:
    Name,[grade1, grade2, grade3]
"""

import os

FILENAME = "class_grades.txt"


def load_grades():
    """Read class_grades.txt and return a dict {name: [grades]}."""
    grades = {}
    if not os.path.exists(FILENAME):
        return grades
    with open(FILENAME, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Split only on the first comma so the list portion stays intact
            name, raw = line.split(",", 1)
            raw = raw.strip().strip("[]")
            scores = [int(s.strip()) for s in raw.split(",") if s.strip()]
            grades[name.strip()] = scores
    return grades


def save_grades(grades):
    """Write the dict back to the file after every modifying operation."""
    with open(FILENAME, "w") as f:
        for name, scores in grades.items():
            f.write(f"{name},{scores}\n")


def parse_grades_input(raw):
    """Parse a user input like '[100, 90, 95]' into a list of ints.
    Raises ValueError if any grade is outside the 0-100 range."""
    raw = raw.strip().strip("[]")
    scores = [int(s.strip()) for s in raw.split(",") if s.strip()]
    for s in scores:
        if s < 0 or s > 100:
            raise ValueError("Grades must be between 0 and 100.")
    return scores


def add_student(grades):
    """Menu option 1: add a new student and persist the change."""
    name = input("Enter name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    try:
        scores = parse_grades_input(input("Enter grades: "))
    except ValueError as e:
        print(f"Invalid grades: {e}")
        return
    grades[name] = scores
    save_grades(grades)
    print("Student added successfully!")


def search_student(grades):
    """Menu option 2: look up a student by name and print grades + average."""
    name = input("Enter name to search: ").strip()
    if name not in grades:
        print(f"Student '{name}' not found.")
        return
    scores = grades[name]
    avg = sum(scores) / len(scores) if scores else 0
    print(f"Grades for {name}: {scores} - Avg: {avg:g}")


def list_students(grades):
    """Menu option 3: print every student with their grades and average."""
    if not grades:
        print("No students.")
        return
    print("Students:")
    for name, scores in grades.items():
        avg = sum(scores) / len(scores) if scores else 0
        print(f"{name} - {scores} - Avg: {avg:g}")


def main():
    """Load existing data, then loop on the menu until the user quits."""
    grades = load_grades()
    while True:
        print("\nClass Grades Program")
        print("1. Add a new student")
        print("2. Search for a student")
        print("3. List all students")
        print("4. Quit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_student(grades)
        elif choice == "2":
            search_student(grades)
        elif choice == "3":
            list_students(grades)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
