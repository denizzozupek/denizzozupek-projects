import random

NUM_DIGITS = 3
MAX_GUESSES = 10

print('''Bagels, a deductive logic game.
I am thinking of a {}-digit number with no repeated digits.
Try to guess what it is. Here some clues:
 When I say:    That means:
    Pico        One digit is correct but in wrong position
    Fermi       One digit is correct and in the right position
    Bagels      No digit is correct.
    
For example, if the secret number was 248 and your guess was 843, the
clues would be Fermi Pico'''.format(NUM_DIGITS))

def main():

    def getSecretNum():
        numbers = list('0123456789')
        random.shuffle(numbers)

        while numbers[0] == '0':
            random.shuffle(numbers)

        secretNum = ''.join(numbers[:NUM_DIGITS])
        return secretNum

    def getClues(guess, secretNum):
        if guess == secretNum:
            return 'You got it!'

        clues = []

        for i in range(len(guess)):
            if guess[i] == secretNum[i]:
                clues.append('Fermi')
            elif guess[i] in secretNum:
                clues.append('Pico')
        if not clues:
            return 'Bagels'

        return ''.join(clues)

    while True:
        secretNum = getSecretNum()
        print(f"I have thought up a number.\nYou have {MAX_GUESSES} guesses to get it.")

        for numGuesses in range(1, MAX_GUESSES + 1):
            guess = ''
            while len(guess) != NUM_DIGITS or not guess.isdecimal():
                print(f"Please enter a valid {NUM_DIGITS}-digit number.")
                guess = input("> ")

            clues = getClues(guess, secretNum)
            print(clues)

            if guess == secretNum:
                print(f"Congratulations! You guessed the secret number in {numGuesses} tries!")
                break
        else:
            print(f"You ran out of guesses. The answer was {secretNum}.")

        print("Do you want to play again? (yes or no)")
        if not input('>').lower().startswith('y'):
            break

    print("Thanks for playing!")

if __name__ == '__main__':
    main()

