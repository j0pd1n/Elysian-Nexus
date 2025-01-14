import json
import os

class ResourceManager:
    def __init__(self):
        self.resources = {"gold": 100, "health_potions": 5}
        self.load()

    def manage_resources(self, action):
        if action == "buy":
            if self.resources["gold"] >= 10:
                self.resources["gold"] -= 10
                self.resources["health_potions"] += 1
                print("Bought a health potion.")
            else:
                print("Not enough gold to buy a health potion.")
        # Add more conditions as needed
        self.save()
        return self.resources

    def save(self):
        with open("resources.json", "w") as f:
            json.dump(self.resources, f, indent=4)

    def load(self):
        if os.path.exists("resources.json"):
            with open("resources.json", "r") as f:
                self.resources = json.load(f)