from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    WEATHER = "weather"
    FACTION = "faction"
    ECONOMIC = "economic"
    COMBAT = "combat"

@dataclass
class GameEvent:
    type: EventType
    name: str
    duration: int
    effects: Dict[str, float]
    conditions: List[str]

class EventHandler:
    def __init__(self):
        self.active_events: List[GameEvent] = []
        
    def create_event(
        self,
        event_type: EventType,
        name: str,
        duration: int,
        effects: Dict[str, float],
        conditions: List[str] = None
    ) -> GameEvent:
        """Create a new game event"""
        event = GameEvent(
            type=event_type,
            name=name,
            duration=duration,
            effects=effects,
            conditions=conditions or []
        )
        self.active_events.append(event)
        return event
        
    def update_events(self, game_time: int):
        """Update active events"""
        # Event update logic here
        pass 