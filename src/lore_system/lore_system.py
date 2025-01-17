from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class LoreCategory(Enum):
    HISTORY = "History"
    CHARACTERS = "Characters"
    LOCATIONS = "Locations"
    CREATURES = "Creatures"
    ARTIFACTS = "Artifacts"
    FACTIONS = "Factions"

@dataclass
class LoreEntry:
    title: str
    category: LoreCategory
    content: str
    discovered: bool = False
    related_entries: List[str] = None

    def __post_init__(self):
        if self.related_entries is None:
            self.related_entries = []

class LoreManager:
    def __init__(self):
        self.lore_entries: Dict[str, LoreEntry] = {}
        self.initialize_lore()

    def initialize_lore(self):
        """Initialize basic lore entries"""
        # History
        self.add_lore_entry(
            "great_war",
            "The Great War",
            LoreCategory.HISTORY,
            "A devastating conflict that reshaped the world..."
        )

        # Characters
        self.add_lore_entry(
            "sage_elara",
            "Sage Elara",
            LoreCategory.CHARACTERS,
            "A wise mage who guards ancient knowledge..."
        )

        # Locations
        self.add_lore_entry(
            "crystal_valley",
            "Crystal Valley",
            LoreCategory.LOCATIONS,
            "A mystical valley filled with powerful crystals..."
        )

        # Creatures
        self.add_lore_entry(
            "shadow_drake",
            "Shadow Drake",
            LoreCategory.CREATURES,
            "A rare species of dragon that lurks in darkness..."
        )

        # Artifacts
        self.add_lore_entry(
            "celestial_crown",
            "Celestial Crown",
            LoreCategory.ARTIFACTS,
            "An ancient artifact of immense power..."
        )

        # Factions
        self.add_lore_entry(
            "mage_council",
            "The Mage Council",
            LoreCategory.FACTIONS,
            "A powerful organization of magic users..."
        )

    def add_lore_entry(self, entry_id: str, title: str, category: LoreCategory, content: str):
        """Add a new lore entry"""
        self.lore_entries[entry_id] = LoreEntry(title, category, content)

    def discover_entry(self, entry_id: str) -> bool:
        """Mark a lore entry as discovered"""
        if entry_id in self.lore_entries:
            self.lore_entries[entry_id].discovered = True
            return True
        return False

    def get_entry(self, entry_id: str) -> Optional[LoreEntry]:
        """Get a specific lore entry"""
        return self.lore_entries.get(entry_id)

    def get_entries_by_category(self, category: LoreCategory) -> List[LoreEntry]:
        """Get all lore entries in a category"""
        return [
            entry for entry in self.lore_entries.values()
            if entry.category == category and entry.discovered
        ]

    def display_entry(self, entry_id: str):
        """Display a lore entry"""
        entry = self.get_entry(entry_id)
        if entry and entry.discovered:
            print(f"\n=== {entry.title} ===")
            print(f"Category: {entry.category.value}")
            print(f"\n{entry.content}")
            
            if entry.related_entries:
                print("\nRelated Entries:")
                for related_id in entry.related_entries:
                    related = self.get_entry(related_id)
                    if related and related.discovered:
                        print(f"- {related.title}")
        else:
            print("Entry not found or not yet discovered.")

    def display_discovered_lore(self):
        """Display all discovered lore entries"""
        print("\n=== Discovered Lore ===")
        for category in LoreCategory:
            entries = self.get_entries_by_category(category)
            if entries:
                print(f"\n{category.value}:")
                for entry in entries:
                    print(f"- {entry.title}")

    def link_entries(self, entry_id: str, related_id: str):
        """Create a link between two lore entries"""
        if entry_id in self.lore_entries and related_id in self.lore_entries:
            entry = self.lore_entries[entry_id]
            related = self.lore_entries[related_id]
            
            if related_id not in entry.related_entries:
                entry.related_entries.append(related_id)
            if entry_id not in related.related_entries:
                related.related_entries.append(entry_id)