import json
import os

class QuestTracker:
    def __init__(self):
        self.active_quests = {
            "Find the artifact": {"completed": False, "description": "Find the ancient artifact in the forest."},
            "Defeat the dragon": {"completed": False, "description": "Defeat the dragon guarding the village."}
        }
        self.load()

    def update_quests(self, action):
        if action == "find" and not self.active_quests["Find the artifact"]["completed"]:
            self.active_quests["Find the artifact"]["completed"] = True
            print("Quest completed: Find the artifact.")
        elif action == "fight" and not self.active_quests["Defeat the dragon"]["completed"]:
            self.active_quests["Defeat the dragon"]["completed"] = True
            print("Quest completed: Defeat the dragon.")
        # Add more conditions as needed
        self.save()

    def save(self):
        with open("quests.json", "w") as f:
            json.dump(self.active_quests, f, indent=4)

    def load(self):
        if os.path.exists("quests.json"):
            with open("quests.json", "r") as f:
                self.active_quests = json.load(f)