
import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
words_file = BASE_DIR / "words.json"

def load_words():
    with open(words_file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_random_word(difficulty):
    words = load_words()
    return random.choice(words[difficulty])

