# 📊 Student Grade Calculator

A Python program that takes a student's name and marks, then calculates their grade with an encouraging message. Built as the Week 2 project of a beginner Python challenge.

## 📖 About

This project puts Week 2 theory into practice:

| Concept | Where it's used |
|---|---|
| `if-elif-else` | Grading logic in `get_grade()` |
| `while` loop | Input validation loop in `get_valid_marks()` |
| Functions | `get_grade()`, `get_valid_marks()`, `display_result()` |
| Input validation | Checks for non-numbers and out-of-range marks |
| f-strings | Formatted result card output |

## 🛠️ Requirements

- Python 3.x — no external libraries needed

## ▶️ How to Run

```bash
python3 grade_calculator.py
```

## 📊 Sample Output

```
🎓 Welcome to the Student Grade Calculator!

Enter student name: Priya
Enter marks (0-100): 85

========================================
  📊 RESULT FOR PRIYA
========================================
  Marks : 85/100
  Grade : B
  Very Good! Keep it up! 👍
========================================

Check another student? (yes/no): no

👋 Thanks for using the Grade Calculator. Goodbye!
```

## 📝 Grading Logic

| Marks | Grade | Message |
|---|---|---|
| 90 – 100 | A | Outstanding! You're a star! 🌟 |
| 80 – 89  | B | Very Good! Keep it up! 👍 |
| 70 – 79  | C | Good work! A little more effort and you'll shine! 💪 |
| 60 – 69  | D | You passed! Aim higher next time — you can do it! 🎯 |
| 0  – 59  | F | Don't give up! Study harder and you'll improve! 📚 |

## 🛡️ Input Validation

The program handles all bad inputs gracefully and keeps asking until valid data is entered:
- Non-numeric input (e.g. `"abc"`) → error + retry
- Out-of-range marks (e.g. `-5` or `105`) → error + retry
- Empty name → error + retry

## 📁 Project Structure

```
.
├── README.md               # Project documentation
├── grade_calculator.py     # Main program
├── test_cases.txt          # 15 manual test cases with results
└── screenshots/            # Terminal screenshots of the program running
```

## 📅 Development Journey (5 Days)

- **Day 1:** Designed the grading rules and planned the program structure
- **Day 2:** Added `input()` to collect student name and marks
- **Day 3:** Implemented `if-elif-else` grading logic inside a function
- **Day 4:** Added `while` loop for input validation and error handling
- **Day 5:** Refactored into clean functions, tested all edge cases, finalized