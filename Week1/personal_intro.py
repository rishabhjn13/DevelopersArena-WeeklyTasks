"""
Personal Introduction Program
------------------------------
Asks the user for their name, age, and favorite hobby,
then displays a friendly, personalized welcome message.
"""

# Step 1: Ask the user for their information
name = input("What is your name? ")
age = input("How old are you? ")
hobby = input("What is your favorite hobby? ")

# Step 2 (bonus): Ask one more question for extra personalization
city = input("Which city are you from? ")

# Step 3: Display a friendly welcome message using f-strings
print()  # blank line for spacing
print(f"🎉 Welcome {name}! 🎉")
print(f"You are {age} years old and love {hobby}.")
print(f"It's awesome to have someone from {city} here!")
print()
print("Thanks for sharing a bit about yourself. Have a great day! 😊")
