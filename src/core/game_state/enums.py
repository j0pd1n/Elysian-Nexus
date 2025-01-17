from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = "main_menu"
    CHARACTER_CREATION = "character_creation"
    TOWN = "town"
    EXPLORATION = "exploration"
    BATTLE = "battle"
    SHOP = "shop"
    INVENTORY = "inventory"
    QUEST_LOG = "quest_log"
    SAVE_GAME = "save_game"
    PAUSED = "paused"
    LOADING = "loading"

class Location(Enum):
    NEXUS_CITY = "Nexus City"
    MYSTIC_FOREST = "Mystic Forest"
    SHADOW_CAVES = "Shadow Caves"
    CRYSTAL_PEAKS = "Crystal Peaks"
    ANCIENT_RUINS = "Ancient Ruins"
    REALITY_NEXUS = "Reality Nexus"
    VOID_SANCTUM = "Void Sanctum"
    TEMPORAL_SANCTUM = "Temporal Sanctum"
    PRIMAL_CORE = "Primal Core"

class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class DifficultyLevel(Enum):
    EASY = auto()
    NORMAL = auto()
    HARD = auto()
    EXPERT = auto()

class GameMode(Enum):
    EXPLORATION = auto()
    COMBAT = auto()
    DIALOGUE = auto()
    MENU = auto()
    CUTSCENE = auto()
    INVENTORY = auto()
    TRADING = auto()
    CRAFTING = auto() 