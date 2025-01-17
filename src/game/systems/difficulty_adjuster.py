import json
import os

class DifficultyAdjuster:
    def __init__(self):
        self.difficulty_levels = self.load_difficulty_levels()
        self.current_difficulty = self.difficulty_levels["easy"]

    def load_difficulty_levels(self):
        if os.path.exists("difficulty_levels.json"):
            with open("difficulty_levels.json", "r") as f:
                return json.load(f)
        else:
            return {
                "easy": {
                    "enemy_health": 100,
                    "enemy_damage": 10,
                    "player_health": 200,
                    "player_damage": 20,
                    "resource_spawn_rate": 0.5
                },
                "medium": {
                    "enemy_health": 150,
                    "enemy_damage": 15,
                    "player_health": 250,
                    "player_damage": 25,
                    "resource_spawn_rate": 0.4
                },
                "hard": {
                    "enemy_health": 200,
                    "enemy_damage": 20,
                    "player_health": 300,
                    "player_damage": 30,
                    "resource_spawn_rate": 0.3
                }
            }

    def save_difficulty_levels(self):
        with open("difficulty_levels.json", "w") as f:
            json.dump(self.difficulty_levels, f, indent=4)

    def adjust_difficulty(self, difficulty):
        if difficulty in self.difficulty_levels:
            self.current_difficulty = self.difficulty_levels[difficulty]
            print(f"Difficulty adjusted to {difficulty}")
        else:
            print(f"Invalid difficulty level: {difficulty}")

    def get_difficulty(self):
        return self.current_difficulty

    def update_difficulty(self, player_behavior):
        if player_behavior == "aggressive":
            self.adjust_difficulty("hard")
        elif player_behavior == "defensive":
            self.adjust_difficulty("easy")
        elif player_behavior == "balanced":
            self.adjust_difficulty("medium")
        else:
            print(f"Invalid player behavior: {player_behavior}")