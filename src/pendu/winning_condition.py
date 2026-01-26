from src.pendu import random_word
from src.pendu import score
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


def winning_condition(name) :
    if "_" not in random_word.hide:
        print("You won")
        print(f"The word was: {random_word.element} " )
        score.score +=1
        score.add_score(name, 1)
    else:
        print("You lost")
        print(f"The word was: {random_word.element} ")

