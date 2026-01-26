import random
import json
from pathlib import Path

# ===== FICHIERS =====
score_folder = Path(__file__).resolve().parent / "score.json"
words_file = Path(__file__).resolve().parent / "words.json"

# ===== NOM JOUEUR =====
player_name = input("Entrez votre nom : ")

# ===== CHARGEMENT DES MOTS =====
def load_words():
    with open(words_file, "r", encoding="utf-8") as f:
        return json.load(f)

def random_word(difficulty):
    words = load_words()
    element = random.choice(words[difficulty])
    hide = ["_"] * len(element)
    return element, hide

# ===== CHOIX DIFFICULTÉ =====

difficulty = input("Choisissez une difficulté :\n1. facile \n2. normal \n3. difficile  ").lower()
if difficulty == 1 or "facile":
    difficulty = "easy"
elif difficulty == 2 or "normal":
    difficulty = "medium"
elif difficulty == 3 or "difficile" :
    difficulty = "hard"
element, hide = random_word(difficulty)

# ===== SCORE =====
def load_score():
    if not score_folder.exists():
        return {"scores": []}
    with open(score_folder, "r", encoding="utf-8") as f:
        return json.load(f)

def save_score(data):
    with open(score_folder, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_score(nom, points):
    data = load_score()

    for player in data["scores"]:
        if player["nom"] == nom:
            player["score"] += points
            save_score(data)
            return

    data["scores"].append({"nom": nom, "score": points})
    save_score(data)

# ===== JEU =====
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

            if attempts == 6:
                print("TU")
            if attempts == 5:
                print("TU ES")
            if attempts == 4:
                print("TU ES P")
            if attempts == 3:
                print("TU ES PE")
            if attempts == 2:
                print("TU ES PEN")
            if attempts == 1:
                print("TU ES PEND")
            if attempts == 0:
                print("TU ES PENDU !")

            if attempts > 1:
                print(f"{guess} is not in the word. You have {attempts} tries left.\n")
            elif attempts == 1:
                print(f"{guess} is not in the word. You have {attempts} last try.\n")

def winning_condition(name):
    if "_" not in hide:
        print("You won")
        print(f"The word was: {element}")
        add_score(name, 1)
    else:
        print("You lost")
        print(f"The word was: {element}")

# ===== LANCEMENT =====
play()
winning_condition(player_name)
