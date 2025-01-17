import json
import os

class PlayerActionInterpreter:
    def __init__(self):
        self.player_actions = []
        self.load()

    def interpret_action(self, action):
        if action.lower() in ["explore", "visit", "talk", "buy", "fight", "find"]:
            self.player_actions.append(action.lower())
            self.save()
            return action.lower()
        else:
            return "unknown"

    def save(self):
        with open("player_actions.json", "w") as f:
            json.dump(self.player_actions, f, indent=4)

    def load(self):
        if os.path.exists("player_actions.json"):
            with open("player_actions.json", "r") as f:
                self.player_actions = json.load(f)