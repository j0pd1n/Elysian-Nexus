class InteractiveLoreLocation:
    def __init__(self, name, description, lore_entry):
        self.name = name
        self.description = description
        self.lore_entry = lore_entry  # Lore entry associated with the location

    def explore(self, player):
        """Allow the player to explore the location and discover lore."""
        print(f"You explore the {self.name}.")
        print(self.description)
        player.lore_journal.add_entry(self.lore_entry)  # Add lore entry to the player's journal
        self.lore_entry.discover()  # Mark the lore entry as discovered 

class InteractiveBook:
    def __init__(self, title, description, lore_entry):
        self.title = title
        self.description = description
        self.lore_entry = lore_entry  # Lore entry associated with the book

    def read(self, player):
        """Allow the player to read the book and discover lore."""
        print(f"You read the book titled '{self.title}'.")
        print(self.description)
        player.lore_journal.add_entry(self.lore_entry)  # Add lore entry to the player's journal
        self.lore_entry.discover()  # Mark the lore entry as discovered

class InteractiveArtifact:
    def __init__(self, name, description, lore_entry):
        self.name = name
        self.description = description
        self.lore_entry = lore_entry  # Lore entry associated with the artifact

    def examine(self, player):
        """Allow the player to examine the artifact and discover lore."""
        print(f"You examine the artifact: {self.name}.")
        print(self.description)
        player.lore_journal.add_entry(self.lore_entry)  # Add lore entry to the player's journal
        self.lore_entry.discover()  # Mark the lore entry as discovered 