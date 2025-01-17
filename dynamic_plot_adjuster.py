import json
import os

class DynamicPlotAdjuster:
    def __init__(self):
        self.adjusted_plot = {}
        self.load()

    def adjust_plot(self, world_state, player_action):
        if player_action == "explore" and world_state["region"] == "Forest":
            self.adjusted_plot = {"event": "Encounter forest creature"}
        elif player_action == "talk" and world_state["region"] == "Village":
            self.adjusted_plot = {"event": "Elder gives quest"}
        # Add more conditions as needed
        self.save()

    def save(self):
        with open("dynamic_plot.json", "w") as f:
            json.dump(self.adjusted_plot, f, indent=4)

    def load(self):
        if os.path.exists("dynamic_plot.json"):
            with open("dynamic_plot.json", "r") as f:
                self.adjusted_plot = json.load(f)