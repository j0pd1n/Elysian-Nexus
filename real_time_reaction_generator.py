import json
import os

class RealTimeReactionGenerator:
    def __init__(self, filename="real_time_reactions.json"):
        self.filename = filename
        self.reactions = []
        self.load()

    def generate_reaction(self, action):
        reaction = self.get_reaction(action)
        self.reactions.append(reaction)
        self.save()
        return reaction

    def get_reaction(self, action):
        reactions = {
            "explore": "You hear rustling in the bushes.",
            "talk": "The NPC smiles warmly.",
            # Add more conditions as needed
        }
        return reactions.get(action, "Unknown action.")

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.reactions, f, indent=4)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.reactions = json.load(f)

# Example usage:
reaction_generator = RealTimeReactionGenerator()
print(reaction_generator.generate_reaction("explore"))
print(reaction_generator.generate_reaction("talk"))
print(reaction_generator.generate_reaction("attack"))