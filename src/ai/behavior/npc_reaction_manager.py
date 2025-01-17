import json
import os

class NPCReactionManager:
    def __init__(self):
        self.reactions = []
        self.load()

    def manage_reactions(self, player_action, npc_emotion):
        if npc_emotion == "happy":
            reaction = "NPC nods approvingly."
        elif npc_emotion == "sad":
            reaction = "NPC looks disappointed."
        # Add more conditions as needed
        self.reactions.append(reaction)
        self.save()
        return reaction

    def save(self):
        with open("npc_reactions.json", "w") as f:
            json.dump(self.reactions, f, indent=4)

    def load(self):
        if os.path.exists("npc_reactions.json"):
            with open("npc_reactions.json", "r") as f:
                self.reactions = json.load(f)