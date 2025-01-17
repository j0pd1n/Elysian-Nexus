import json
import os

class EnvironmentalChangeManager:
    def __init__(self):
        self.environment_changes = []
        self.load()

    def change_environment(self, action):
        if action == "explore":
            if self.environment_changes:
                last_change = self.environment_changes[-1]
                if last_change == "Weather changes to rainy.":
                    change = "Weather changes to sunny."
                else:
                    change = "Weather changes to rainy."
            else:
                change = "Weather changes to rainy."
        # Add more conditions as needed
        self.environment_changes.append(change)
        print(f"Changing environment based on action: {action} - {change}")
        self.save()
        return change

    def save(self):
        with open("environment_changes.json", "w") as f:
            json.dump(self.environment_changes, f, indent=4)

    def load(self):
        if os.path.exists("environment_changes.json"):
            with open("environment_changes.json", "r") as f:
                self.environment_changes = json.load(f)