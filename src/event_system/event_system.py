from enum import Enum
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

class EventType(Enum):
    COMBAT = "combat"
    QUEST = "quest"
    DIALOGUE = "dialogue"
    INVENTORY = "inventory"
    MOVEMENT = "movement"
    INTERACTION = "interaction"
    SYSTEM = "system"
    ACHIEVEMENT = "achievement"
    FACTION = "faction"
    TRADE = "trade"

class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class Event:
    type: EventType
    name: str
    data: Dict
    priority: EventPriority
    timestamp: datetime
    source: Optional[str] = None
    target: Optional[str] = None
    duration: Optional[float] = None
    callback: Optional[Callable] = None

class EventSystem:
    def __init__(self):
        self.events: List[Event] = []
        self.listeners: Dict[EventType, List[Callable]] = {
            event_type: [] for event_type in EventType
        }
        self.active_events: List[Event] = []
        self.event_history: List[Event] = []
        self.max_history = 1000

    def add_listener(self, event_type: EventType, callback: Callable):
        """Add an event listener"""
        if event_type in self.listeners:
            self.listeners[event_type].append(callback)

    def remove_listener(self, event_type: EventType, callback: Callable):
        """Remove an event listener"""
        if event_type in self.listeners:
            self.listeners[event_type] = [
                cb for cb in self.listeners[event_type]
                if cb != callback
            ]

    def dispatch_event(self, event: Event):
        """Dispatch an event to all registered listeners"""
        self.events.append(event)
        self.event_history.append(event)
        self._trim_history()

        if event.duration:
            self.active_events.append(event)

        for callback in self.listeners[event.type]:
            callback(event)

        if event.callback:
            event.callback(event)

    def create_event(self, type: EventType, name: str, data: Dict,
                    priority: EventPriority = EventPriority.NORMAL,
                    source: Optional[str] = None, target: Optional[str] = None,
                    duration: Optional[float] = None,
                    callback: Optional[Callable] = None) -> Event:
        """Create and return a new event"""
        event = Event(
            type=type,
            name=name,
            data=data,
            priority=priority,
            timestamp=datetime.now(),
            source=source,
            target=target,
            duration=duration,
            callback=callback
        )
        return event

    def get_active_events(self, event_type: Optional[EventType] = None) -> List[Event]:
        """Get all active events, optionally filtered by type"""
        if event_type:
            return [e for e in self.active_events if e.type == event_type]
        return self.active_events

    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """Get all events of a specific type"""
        return [e for e in self.events if e.type == event_type]

    def get_events_by_priority(self, priority: EventPriority) -> List[Event]:
        """Get all events of a specific priority"""
        return [e for e in self.events if e.priority == priority]

    def clear_events(self, event_type: Optional[EventType] = None):
        """Clear events, optionally of a specific type"""
        if event_type:
            self.events = [e for e in self.events if e.type != event_type]
            self.active_events = [e for e in self.active_events if e.type != event_type]
        else:
            self.events.clear()
            self.active_events.clear()

    def _trim_history(self):
        """Trim event history if it exceeds max size"""
        if len(self.event_history) > self.max_history:
            self.event_history = sorted(
                self.event_history,
                key=lambda e: (e.timestamp, -e.priority.value)
            )[:self.max_history]

    def update(self):
        """Update event system, removing expired events"""
        current_time = datetime.now()
        self.active_events = [
            event for event in self.active_events
            if event.duration is None or
            (current_time - event.timestamp).total_seconds() < event.duration
        ]

    def get_event_history(self) -> List[Event]:
        """Get complete event history"""
        return sorted(self.event_history,
                     key=lambda e: e.timestamp,
                     reverse=True)

    def get_events_by_source(self, source: str) -> List[Event]:
        """Get all events from a specific source"""
        return [e for e in self.events if e.source == source]

    def get_events_by_target(self, target: str) -> List[Event]:
        """Get all events targeting a specific entity"""
        return [e for e in self.events if e.target == target]

    def set_max_history(self, max_count: int):
        """Set maximum number of events to keep in history"""
        self.max_history = max_count
        self._trim_history()

    def has_active_event(self, event_type: EventType) -> bool:
        """Check if there are any active events of a specific type"""
        return any(e.type == event_type for e in self.active_events) 