import json
import os

class WorldStateManager:
    def __init__(self):
        self.world_state = {"region": "Forest", "weather": "Sunny"}
        self.load()

    def update_world_state(self, action):
        if action == "explore":
            if self.world_state["region"] == "Forest":
                self.world_state["region"] = "Mountain"
            elif self.world_state["region"] == "Mountain":
                self.world_state["region"] = "Village"
            # Add more regions as needed
        # Add more conditions as needed
        print(f"Updating world state: {self.world_state}")
        self.save()
        return self.world_state

    def save(self):
        with open("world_state.json", "w") as f:
            json.dump(self.world_state, f, indent=4)

    def load(self):
        if os.path.exists("world_state.json"):
            with open("world_state.json", "r") as f:
                self.world_state = json.load(f)