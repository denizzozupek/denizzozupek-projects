import random

print('ROCK PAPER SCISSORS RULES:\n'
      + "Rock vs Paper --> Paper wins\n"
      + "Paper vs Scissors --> Scissors wins\n"
      + "Rock vs Scissors --> Rock wins\n")

def play_game():
    while True:
        print("Enter your choice:\n 1 - Rock\n 2 - Paper\n 3 - Scissors")

        # User input validation
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue

        while choice > 3 or choice < 1:
            choice = int(input("Please enter a valid choice (1, 2, or 3): "))

        # User's choice mapping
        if choice == 1:
            choice_name = 'Rock'
        elif choice == 2:
            choice_name = 'Paper'
        else:
            choice_name = 'Scissors'

        # Print user's choice
        print('User choice is:', choice_name)
        print("Now it's computer's turn...")

        # Computer's choice
        comp_choice = random.randint(1, 3)

        if comp_choice == 1:
            comp_choice_name = 'Rock'
        elif comp_choice == 2:
            comp_choice_name = 'Paper'
        else:
            comp_choice_name = 'Scissors'

        print("Computer choice is:", comp_choice_name)
        print(choice_name, 'vs', comp_choice_name)

        # Determine result
        if choice == comp_choice:
            result = "DRAW"
        elif (choice == 1 and comp_choice == 2) or (comp_choice == 1 and choice == 2):
            result = 'Paper'
        elif (choice == 1 and comp_choice == 3) or (comp_choice == 1 and choice == 3):
            result = 'Rock'
        elif (choice == 2 and comp_choice == 3) or (comp_choice == 2 and choice == 3):
            result = 'Scissors'

        # Print the result
        if result == "DRAW":
            print("IT'S A TIE!!")
        elif result == choice_name:
            print("USER WINS!!")
        else:
            print("COMPUTER WINS!!")

        # Ask to play again, only accept 'y' or 'n'
        while True:
            print("Do you want to play again? (Y/N)")
            ans = input().lower()
            if ans == 'y':
                break
            elif ans == 'n':
                return
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

# Run the game
play_game()
