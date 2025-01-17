import json
import os
import random

class DynamicDialogueGenerator:
    def __init__(self):
        self.dialogue_data = self.load_dialogue_data()
        self.player_name = ""
        self.player_pronouns = ""
        self.npc_names = []
        self.npc_pronouns = []
        self.dialogue_context = {}

    def load_dialogue_data(self):
        if os.path.exists("dialogue_data.json"):
            with open("dialogue_data.json", "r") as f:
                return json.load(f)
        else:
            return {
                "greetings": [
                    "Hello, {player_name}!",
                    "Hi {player_name}, how are you?",
                    "Hey {player_name}!"
                ],
                "goodbyes": [
                    "Goodbye, {player_name}!",
                    "See you later, {player_name}!",
                    "Farewell, {player_name}!"
                ],
                "introductions": [
                    "I'm {npc_name}, nice to meet you {player_name}.",
                    "Hello {player_name}, I'm {npc_name}.",
                    "Hi {player_name}, I'm {npc_name}."
                ]
            }

    def save_dialogue_data(self):
        with open("dialogue_data.json", "w") as f:
            json.dump(self.dialogue_data, f, indent=4)

    def generate_dialogue(self, dialogue_type, context=None):
        if dialogue_type in self.dialogue_data:
            dialogue = random.choice(self.dialogue_data[dialogue_type])
            dialogue = dialogue.replace("{player_name}", self.player_name)
            dialogue = dialogue.replace("{player_pronouns}", self.player_pronouns)
            for i, npc_name in enumerate(self.npc_names):
                dialogue = dialogue.replace("{npc_name" + str(i) + "}", npc_name)
                dialogue = dialogue.replace("{npc_pronouns" + str(i) + "}", self.npc_pronouns[i])
            if context:
                for key, value in context.items():
                    dialogue = dialogue.replace("{" + key + "}", value)
            return dialogue
        else:
            return "Invalid dialogue type."

    def set_player_name(self, name):
        self.player_name = name

    def set_player_pronouns(self, pronouns):
        self.player_pronouns = pronouns

    def add_npc(self, name, pronouns):
        self.npc_names.append(name)
        self.npc_pronouns.append(pronouns)

    def remove_npc(self, name):
        if name in self.npc_names:
            index = self.npc_names.index(name)
            self.npc_names.pop(index)
            self.npc_pronouns.pop(index)

    def update_dialogue_data(self, dialogue_type, new_dialogue):
        if dialogue_type in self.dialogue_data:
            self.dialogue_data[dialogue_type].append(new_dialogue)
            self.save_dialogue_data()
        else:
            print("Invalid dialogue type.")

    def get_dialogue(self, dialogue_type, context=None):
        return self.generate_dialogue(dialogue_type, context)

    def set_dialogue_context(self, context):
        self.dialogue_context = context

    def get_dialogue_context(self):
        return self.dialogue_context

    def generate_branching_dialogue(self, dialogue_type, choices):
        dialogue = self.generate_dialogue(dialogue_type)
        for choice in choices:
            dialogue += "\n" + choice
        return dialogue

    def generate_conversation(self, dialogue_types, choices):
        conversation = ""
        for dialogue_type in dialogue_types:
            conversation += self.generate_dialogue(dialogue_type) + "\n"
            if choices:
                conversation += self.generate_branching_dialogue(dialogue_type, choices) + "\n"
        return conversation