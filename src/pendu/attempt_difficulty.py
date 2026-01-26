import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.pendu import random_word
from src.pendu import pendu

def easy_attempts():
    attempt = 7
    while attempt > 0 and "_" in random_word.hide:
        print(f"Guess the word: {" ".join(random_word.hide)}")
        guess = input("Choose a letter: ").lower()

        if guess in random_word.element:
            for i in range(len(random_word.element)):
                if random_word.element[i] == guess:
                    random_word.hide[i] = guess
        else:
            attempt -= 1
            pendu.pendu()
            if attempt > 1:
                print(f"{guess} is not in the word. You have {attempt} tries left.\n")
            elif attempt == 1:
                print(f"{guess} is not in the word. You have {attempt} last try.\n")

def medium_attempts():
    attempt = 5
    while attempt > 0 and "_" in random_word.hide:
        print(f"Guess the word: {" ".join(random_word.hide)}")
        guess = input("Choose a letter: ").lower()

        if guess in random_word.element:
            for i in range(len(random_word.element)):
                if random_word.element[i] == guess:
                    random_word.hide[i] = guess
        else:
            attempt -= 1
            pendu.pendu()
            if attempt > 1:
                print(f"{guess} is not in the word. You have {attempt} tries left.\n")
            elif attempt == 1:
                print(f"{guess} is not in the word. You have {attempt} last try.\n")

def hard_attempts():
    attempt = 3
    while attempt > 0 and "_" in random_word.hide:
        print(f"Guess the word: {" ".join(random_word.hide)}")
        guess = input("Choose a letter: ").lower()

        if guess in random_word.element:
            for i in range(len(random_word.element)):
                if random_word.element[i] == guess:
                    random_word.hide[i] = guess
        else:
            attempt -= 1
            pendu.pendu()
            if attempt > 1:
                print(f"{guess} is not in the word. You have {attempt} tries left.\n")
            elif attempt == 1:
                print(f"{guess} is not in the word. You have {attempt} last try.\n")
