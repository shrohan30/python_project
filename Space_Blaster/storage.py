import json
import os

FILE = "data/scores.json"

def load_data():
    if not os.path.exists(FILE):
        return {"players": [], "highscore": 0}
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_player_score(name, score, level):
    data = load_data()

    # Add player record
    data["players"].append({
        "name": name,
        "score": score,
        "level": level
    })

    # Update highscore
    if score > data["highscore"]:
        data["highscore"] = score

    save_data(data)

def get_highscore():
    data = load_data()
    return data["highscore"]