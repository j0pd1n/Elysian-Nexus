import json
import os

class StoryProgressionManager:
    def __init__(self):
        self.current_plot_point = 0
        self.plot_points = [
            {"name": "Start", "options": ["Explore the forest", "Visit the village"]},
            {"name": "Forest", "options": ["Fight the monster", "Find a hidden cave"]},
            {"name": "Village", "options": ["Talk to the elder", "Buy supplies"]},
            {"name": "End", "options": []}
        ]
        self.load()

    def progress_story(self, decision):
        if decision in self.plot_points[self.current_plot_point]["options"]:
            if decision == "Explore the forest":
                self.current_plot_point = 1
            elif decision == "Visit the village":
                self.current_plot_point = 2
            elif decision == "Fight the monster":
                self.current_plot_point = 3
            elif decision == "Find a hidden cave":
                self.current_plot_point = 3
            elif decision == "Talk to the elder":
                self.current_plot_point = 3
            elif decision == "Buy supplies":
                self.current_plot_point = 3
        self.save()
        return self.plot_points[self.current_plot_point]

    def save(self):
        with open("story_progression.json", "w") as f:
            json.dump({"current_plot_point": self.current_plot_point}, f, indent=4)

    def load(self):
        if os.path.exists("story_progression.json"):
            with open("story_progression.json", "r") as f:
                data = json.load(f)
                self.current_plot_point = data.get("current_plot_point", 0)