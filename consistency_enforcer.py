import json
import os

class ConsistencyEnforcer:
    def __init__(self):
        self.rules = self.load_rules()
        self.world_state = {}

    def load_rules(self):
        if os.path.exists("consistency_rules.json"):
            with open("consistency_rules.json", "r") as f:
                return json.load(f)
        else:
            return {
                "region": {
                    "forest": ["tree", "rock", "stream"],
                    "mountain": ["rock", "snow", "cave"]
                },
                "weather": {
                    "sunny": ["clear", "warm"],
                    "rainy": ["cloudy", "cool"]
                },
                "time_of_day": {
                    "day": ["sun", "light"],
                    "night": ["moon", "dark"]
                }
            }

    def save_rules(self):
        with open("consistency_rules.json", "w") as f:
            json.dump(self.rules, f, indent=4)

    def enforce_consistency(self, world_state):
        self.world_state = world_state
        for key, value in self.rules.items():
            self.check_rule(key, value)
        print("Consistency enforced")

    def check_rule(self, key, value):
        if key in self.world_state:
            if self.world_state[key] not in value:
                print(f"Consistency error: {key} is not in {value}")
                self.correct_rule(key, value)
        else:
            print(f"Consistency error: {key} is not defined")
            self.add_rule(key, value)

    def correct_rule(self, key, value):
        if key == "region":
            self.world_state[key] = "forest"
        elif key == "weather":
            self.world_state[key] = "sunny"
        elif key == "time_of_day":
            self.world_state[key] = "day"

    def add_rule(self, key, value):
        if key == "region":
            self.world_state[key] = "forest"
        elif key == "weather":
            self.world_state[key] = "sunny"
        elif key == "time_of_day":
            self.world_state[key] = "day"

    def get_world_state(self):
        return self.world_state

    def update_rule(self, key, value):
        if key in self.rules:
            self.rules[key] = value
            self.save_rules()
            print(f"Rule updated: {key} = {value}")
        else:
            print(f"Invalid key: {key}")

    def add_new_rule(self, key, value):
        self.rules[key] = value
        self.save_rules()
        print(f"New rule added: {key} = {value}")

    def remove_rule(self, key):
        if key in self.rules:
            del self.rules[key]
            self.save_rules()
            print(f"Rule removed: {key}")
        else:
            print(f"Invalid key: {key}")