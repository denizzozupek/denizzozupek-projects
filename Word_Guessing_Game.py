import random

# Asking the user for their name and wishing them luck
name = input("Please enter your name: ")
print(f"Good luck {name}!")

# List of possible words for the game
words = ['wood', 'book', 'black', 'clean', 'spear', 'move',
         'plane', 'movie', 'rock','science', 'spaghetti',
         'sweatshirt', 'lion', 'try', 'walkthrough']

# Randomly selecting a word from the list
word = random.choice(words)

# Starting the game with a message
print("Guess the word")

# Variable to track guesses and number of turns
guesses = ''
turns = 12  # Total number of attempts the player can make

while turns > 0:

    # A variable to track how many characters in the word are guessed correctly
    failed = 0

    # Loop through the word and check each character
    for char in word:

        # If the character has been guessed, print it
        if char in guesses:
            print(char, end=" ")

        # If the character has not been guessed, print an underscore (_)
        else:
            print("_", end=" ")

            # Increment failed if the character is still missing
            failed += 1

    # If all characters are guessed, the player wins
    if failed == 0:
        print("\nYou win!")
        print(f"The word is: {word}")
        break

    print()

    # Prompt the user to guess a character
    guess = input("Guess a character: ")

    # Add the guess to the list of guesses
    guesses += guess

    # If the guess is incorrect, reduce turns and notify the player
    if guess not in word:
        turns -= 1
        print("Wrong!")
        print(f"You have {turns} guesses left")

        # If the player runs out of turns, they lose
        if turns == 0:
            print("You lose!")
            print(f"The word was: {word}")
import random

# Asking the user for their name and wishing them luck
name = input("Please enter your name: ")
print(f"Good luck {name}!")

# List of possible words for the game
words = ['wood', 'book', 'black', 'clean', 'spear', 'move',
         'plane', 'movie', 'rock','science', 'spaghetti',
         'sweatshirt', 'lion', 'try', 'walkthrough']

# Randomly selecting a word from the list
word = random.choice(words)

# Starting the game with a message
print("Guess the word")

# Variable to track guesses and number of turns
guesses = ''
turns = 12  # Total number of attempts the player can make

while turns > 0:

    # A variable to track how many characters in the word are guessed correctly
    failed = 0

    # Loop through the word and check each character
    for char in word:

        # If the character has been guessed, print it
        if char in guesses:
            print(char, end=" ")

        # If the character has not been guessed, print an underscore (_)
        else:
            print("_", end=" ")

            # Increment failed if the character is still missing
            failed += 1

    # If all characters are guessed, the player wins
    if failed == 0:
        print("\nYou win!")
        print(f"The word is: {word}")
        break

    print()

    # Prompt the user to guess a character
    guess = input("Guess a character: ")

    # Add the guess to the list of guesses
    guesses += guess

    # If the guess is incorrect, reduce turns and notify the player
    if guess not in word:
        turns -= 1
        print("Wrong!")
        print(f"You have {turns} guesses left")

        # If the player runs out of turns, they lose
        if turns == 0:
            print("You lose!")
            print(f"The word was: {word}")

