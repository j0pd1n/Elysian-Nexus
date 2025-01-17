class LoreEntry:
    def __init__(self, title, description, type):
        self.title = title
        self.description = description
        self.type = type

class LoreEngine:
    def __init__(self):
        self.lore_entries = []

    def add_lore_entry(self, title, description, type):
        lore_entry = LoreEntry(title, description, type)
        self.lore_entries.append(lore_entry)

    def get_lore_entries(self):
        return self.lore_entries

# Create a Lore Engine instance
lore_engine = LoreEngine()

# Add some lore entries
lore_engine.add_lore_entry("The Aeon War", "A great conflict between the Aeons and the humans.", "event")
lore_engine.add_lore_entry("The Aeons", "A group of powerful beings who ruled the world.", "faction")
lore_engine.add_lore_entry("The Humans", "A group of beings who fought against the Aeons.", "faction")

# Get the lore entries
lore_entries = lore_engine.get_lore_entries()

# Print the lore entries
for lore_entry in lore_entries:
    print(lore_entry.title)
    print(lore_entry.description)
    print(lore_entry.type)