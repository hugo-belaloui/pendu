
import json
from pathlib import Path

score_file = Path(__file__).resolve().parents[2] / "score.json"

def load_score():
    if not score_file.exists():
        return {"scores": []}
    with open(score_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_score(data):
    with open(score_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_score(name):
    data = load_score()
    for player in data["scores"]:
        if player["nom"] == name:
            player["score"] += 1
            save_score(data)
            return
    data["scores"].append({"nom": name, "score": 1})
    save_score(data)
