import random

words = ["tete", "mafia", "pasteque", "triangle"]
element = random.choice(words)

hide = ["_"] * len(element)
score = 0

def attempt():
    attempt = 7
    while attempt > 0 and "_" in hide:
        print(f"Guess the word: {" ".join(hide)}")
        guess = input("Choose a letter: ").lower()

        if guess in element:
            for i in range(len(element)):
                if element[i] == guess:
                    hide[i] = guess
        else:
            attempt -= 1
            if attempt > 1:
                print(f"{guess} is not in the word. You have {attempt} tries left.\n")
            elif attempt == 1:
                print(f"{guess} is not in the word. You have {attempt} last try.\n")

def winning_condition() :
    if "_" not in hide:
        print("You won")
        print(f"The word was: {element} " )
        score +=1
    else:
        print("You lost")
        print(f"The word was: {element} ")


with open("score.txt", "a") as folder:
    folder.write(f"{score}\n")