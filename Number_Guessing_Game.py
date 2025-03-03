import random

guess = None
attempts = 0
target_number = random.randint(0, 100)

while guess != target_number:
    try:
        guess = int(input(" Please enter a number: "))
        attempts += 1

        if guess < target_number:
            print("⬆ Try a higher number!")
        elif guess > target_number:
            print("⬇ Try a lower number!")
        else:
            print(f" Congratulations! You found the number in {attempts} attempts.")
    except ValueError:
        print(" Invalid input! Please enter a valid number.")
