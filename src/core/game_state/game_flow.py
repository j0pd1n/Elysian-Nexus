from typing import Dict, List
from faction_system import FactionSystem
from .enums import GameState, Location, QuestStatus
from .story import STORY_CHAPTERS, STORY_PATHS, STORY_RELATIONSHIPS, STORY_EVENTS
from .locations import LOCATION_DATA

class GameFlow:
    def __init__(self):
        self.faction_system = FactionSystem()
        # ... other systems initialization