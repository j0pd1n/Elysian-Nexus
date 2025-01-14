import json
import os

class ContextualAwarenessManager:
    def __init__(self):
        self.context = {}
        self.context_history = []
        self.context_rules = self.load_context_rules()

    def load_context_rules(self):
        if os.path.exists("context_rules.json"):
            with open("context_rules.json", "r") as f:
                return json.load(f)
        else:
            return {
                "location": {
                    "forest": ["tree", "rock", "stream"],
                    "mountain": ["rock", "snow", "cave"]
                },
                "time_of_day": {
                    "day": ["sun", "light"],
                    "night": ["moon", "dark"]
                },
                "weather": {
                    "sunny": ["clear", "warm"],
                    "rainy": ["cloudy", "cool"]
                }
            }

    def save_context_rules(self):
        with open("context_rules.json", "w") as f:
            json.dump(self.context_rules, f, indent=4)

    def manage_context(self, new_context):
        self.context = new_context
        self.context_history.append(new_context)
        self.apply_context_rules()

    def apply_context_rules(self):
        for key, value in self.context.items():
            if key in self.context_rules:
                for rule in self.context_rules[key]:
                    if value in rule:
                        print(f"Context rule applied: {key} = {value}")

    def get_context(self):
        return self.context

    def get_context_history(self):
        return self.context_history

    def update_context_rule(self, key, value):
        if key in self.context_rules:
            self.context_rules[key] = value
            self.save_context_rules()
            print(f"Context rule updated: {key} = {value}")
        else:
            print(f"Invalid key: {key}")

    def add_context_rule(self, key, value):
        self.context_rules[key] = value
        self.save_context_rules()
        print(f"Context rule added: {key} = {value}")

    def remove_context_rule(self, key):
        if key in self.context_rules:
            del self.context_rules[key]
            self.save_context_rules()
            print(f"Context rule removed: {key}")
        else:
            print(f"Invalid key: {key}")

    def analyze_context(self):
        for key, value in self.context.items():
            print(f"Analyzing context: {key} = {value}")
            # Add analysis logic here

    def predict_context(self):
        # Add prediction logic here
        pass