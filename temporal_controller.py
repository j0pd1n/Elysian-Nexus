import json
import os

class TemporalController:
    def __init__(self):
        self.time_state = 0
        self.load()

    def manage_time(self, time_step):
        self.time_state += time_step
        print(f"Managing time step: {time_step} - New time state: {self.time_state}")
        self.save()
        return self.time_state

    def save(self):
        with open("time_state.json", "w") as f:
            json.dump({"time_state": self.time_state}, f, indent=4)

    def load(self):
        if os.path.exists("time_state.json"):
            with open("time_state.json", "r") as f:
                data = json.load(f)
                self.time_state = data.get("time_state", 0)