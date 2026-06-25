"""
Student Grade Calculator
------------------------
Takes a student's name and marks, then returns
their grade with an encouraging message.

Concepts used: functions, if-elif-else, while loop,
               input validation, f-strings
"""


def get_grade(marks):
    """Return (grade, message) tuple based on marks (0-100)."""
    if marks >= 90:
        return "A", "Outstanding! You're a star! 🌟"
    elif marks >= 80:
        return "B", "Very Good! Keep it up! 👍"
    elif marks >= 70:
        return "C", "Good work! A little more effort and you'll shine! 💪"
    elif marks >= 60:
        return "D", "You passed! Aim higher next time — you can do it! 🎯"
    else:
        return "F", "Don't give up! Study harder and you'll improve! 📚"


def get_valid_marks():
    """Keep asking until the user enters a number between 0 and 100."""
    while True:
        raw = input("Enter marks (0-100): ").strip()

        # Check it's actually a number
        if not raw.replace(".", "", 1).isdigit():
            print("❌ Invalid input! Please enter a number.\n")
            continue

        marks = float(raw)

        # Check it's in the valid range
        if marks < 0 or marks > 100:
            print("❌ Marks must be between 0 and 100. Try again.\n")
            continue

        return marks


def display_result(name, marks, grade, message):
    """Print a formatted result card for the student."""
    print()
    print("=" * 40)
    print(f"  📊 RESULT FOR {name.upper()}")
    print("=" * 40)
    print(f"  Marks : {marks:.0f}/100")
    print(f"  Grade : {grade}")
    print(f"  {message}")
    print("=" * 40)
    print()


# ──────────────────────────────────────────
# MAIN PROGRAM
# ──────────────────────────────────────────
def main():
    print("\n🎓 Welcome to the Student Grade Calculator!\n")

    while True:
        # Get student name
        name = input("Enter student name: ").strip()
        if not name:
            print("❌ Name cannot be empty. Try again.\n")
            continue

        # Get valid marks using our validation function
        marks = get_valid_marks()

        # Calculate grade
        grade, message = get_grade(marks)

        # Show result
        display_result(name, marks, grade, message)

        # Ask to evaluate another student
        again = input("Check another student? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\n👋 Thanks for using the Grade Calculator. Goodbye!\n")
            break
        print()


if __name__ == "__main__":
    main()
