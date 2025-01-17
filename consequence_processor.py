import json
import os

class ConsequenceProcessor:
    def __init__(self):
        self.consequences = self.load_consequences()

    def load_consequences(self):
        if os.path.exists("consequences.json"):
            with open("consequences.json", "r") as f:
                return json.load(f)
        else:
            return {
                "explore": {
                    "region": "Mountain",
                    "weather": "Rainy",
                    "resources": -10
                },
                "rest": {
                    "health": 10,
                    "hunger": -5
                },
                # Add more consequences as needed
            }

    def save_consequences(self):
        with open("consequences.json", "w") as f:
            json.dump(self.consequences, f, indent=4)

    def add_consequence(self, action, consequence):
        self.consequences[action] = consequence
        self.save_consequences()

    def remove_consequence(self, action):
        if action in self.consequences:
            del self.consequences[action]
            self.save_consequences()

    def process_consequences(self, action, world_state):
        consequence = self.consequences.get(action)
        if consequence:
            for key, value in consequence.items():
                if key == "region":
                    world_state["region"] = value
                elif key == "weather":
                    world_state["weather"] = value
                elif key == "resources":
                    world_state["resources"] = world_state.get("resources", 0) + value
                elif key == "health":
                    world_state["health"] = world_state.get("health", 0) + value
                elif key == "hunger":
                    world_state["hunger"] = world_state.get("hunger", 0) + value
            print(f"Consequence of {action}: {consequence}")
            return world_state
        else:
            print(f"No consequence for {action}")
            return world_state