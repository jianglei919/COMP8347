import os

FILENAME = "class_grades.txt"


def load_grades():
    grades = {}
    if not os.path.exists(FILENAME):
        return grades
    with open(FILENAME, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, raw = line.split(",", 1)
            raw = raw.strip().strip("[]")
            scores = [int(s.strip()) for s in raw.split(",") if s.strip()]
            grades[name.strip()] = scores
    return grades


def save_grades(grades):
    with open(FILENAME, "w") as f:
        for name, scores in grades.items():
            f.write(f"{name},{scores}\n")


def parse_grades_input(raw):
    raw = raw.strip().strip("[]")
    scores = [int(s.strip()) for s in raw.split(",") if s.strip()]
    for s in scores:
        if s < 0 or s > 100:
            raise ValueError("Grades must be between 0 and 100.")
    return scores


def add_student(grades):
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
    name = input("Enter name to search: ").strip()
    if name not in grades:
        print(f"Student '{name}' not found.")
        return
    scores = grades[name]
    avg = sum(scores) / len(scores) if scores else 0
    print(f"Grades for {name}: {scores} - Avg: {avg:g}")


def list_students(grades):
    if not grades:
        print("No students.")
        return
    print("Students:")
    for name, scores in grades.items():
        avg = sum(scores) / len(scores) if scores else 0
        print(f"{name} - {scores} - Avg: {avg:g}")


def main():
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
