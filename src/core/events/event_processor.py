from enum import Enum, auto

class EventType(Enum):
    COMBAT = auto()
    QUEST = auto()
    DIALOGUE = auto()
    INVENTORY = auto()
    MOVEMENT = auto()
    INTERACTION = auto()
    SYSTEM = auto()
    ACHIEVEMENT = auto()
    FACTION = auto()
    TRADE = auto()

class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3 