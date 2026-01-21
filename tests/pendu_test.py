import random

words = ["tete", "mafia", "pasteque", "triangle"]
element = random.choice(words)

hide = ["_"] * len(element)
score = 0

def play():
    attempts = 7
    while attempts > 0 and "_" in hide:
        print(f"Guess the word: {' '.join(hide)}")
        guess = input("Choose a letter: ").lower()

        if guess in element:
            for i in range(len(element)):
                if element[i] == guess:
                    hide[i] = guess
        else:
            attempts -= 1
            if attempts > 1:
                print(f"{guess} is not in the word. You have {attempts} tries left.\n")
            elif attempts == 1:
                print(f"{guess} is not in the word. You have {attempts} last try.\n")

def winning_condition():
    global score
    if "_" not in hide:
        print("You won!")
        print(f"The word was: {element}")
        score += 1
    else:
        print("You lost.")
        print(f"The word was: {element}")


play()
winning_condition()


