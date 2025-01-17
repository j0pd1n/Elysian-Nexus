from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
from dataclasses import dataclass
from .event_manager import Event, EventType, EventTrigger
from .faction_event_handler import FactionEventHandler
from .combat_event_handler import CombatEventHandler
from .ritual_event_handler import RitualEventHandler
from .event_visualization import EventVisualization

class EventPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class EventDependency:
    event_id: str
    required_status: str  # "completed", "failed", "active"
    priority: EventPriority

class EventOrchestrator:
    def __init__(self):
        # Initialize handlers
        self.faction_handler = FactionEventHandler()
        self.combat_handler = CombatEventHandler()
        self.ritual_handler = RitualEventHandler()
        self.visualization = EventVisualization()
        
        # Event tracking
        self.active_events: Dict[str, Event] = {}
        self.event_dependencies: Dict[str, List[EventDependency]] = {}
        self.event_priorities: Dict[str, EventPriority] = {}
        self.event_conflicts: Dict[str, Set[str]] = {}  # event_id -> set of conflicting event_ids
        self.event_chains: Dict[str, List[str]] = {}  # chain_id -> ordered list of event_ids
        
        # Event history
        self.completed_events: List[str] = []
        self.failed_events: List[str] = []

    def register_event(self, event: Event, priority: EventPriority = EventPriority.MEDIUM) -> bool:
        """Register a new event with the orchestrator"""
        if event.event_id in self.active_events:
            return False
            
        self.active_events[event.event_id] = event
        self.event_priorities[event.event_id] = priority
        
        # Initialize conflict and dependency tracking
        self.event_conflicts[event.event_id] = set()
        
        # Add to visualization
        self.visualization.add_event_node(
            event=event,
            description=f"{event.name} (Priority: {priority.name})",
            effects=self._get_event_effects(event)
        )
        
        return True

    def add_dependency(self, event_id: str, dependency: EventDependency):
        """Add a dependency requirement for an event"""
        if event_id not in self.event_dependencies:
            self.event_dependencies[event_id] = []
        self.event_dependencies[event_id].append(dependency)
        
        # Update visualization
        self.visualization.connect_events(dependency.event_id, event_id)

    def register_conflict(self, event_id_a: str, event_id_b: str):
        """Register two events as conflicting"""
        if event_id_a in self.active_events and event_id_b in self.active_events:
            self.event_conflicts[event_id_a].add(event_id_b)
            self.event_conflicts[event_id_b].add(event_id_a)

    def create_event_chain(self, chain_id: str, event_ids: List[str]):
        """Create a chain of dependent events"""
        if chain_id in self.event_chains:
            return False
            
        self.event_chains[chain_id] = event_ids
        
        # Create dependencies between consecutive events
        for i in range(len(event_ids) - 1):
            self.add_dependency(
                event_ids[i + 1],
                EventDependency(
                    event_id=event_ids[i],
                    required_status="completed",
                    priority=self.event_priorities.get(event_ids[i], EventPriority.MEDIUM)
                )
            )
        
        return True

    def update(self, game_state: Dict) -> List[str]:
        """Update all event systems and handle interactions"""
        activated_events = []
        
        # Sort events by priority
        prioritized_events = sorted(
            self.active_events.items(),
            key=lambda x: self.event_priorities[x[0]].value,
            reverse=True
        )
        
        for event_id, event in prioritized_events:
            if self._can_activate_event(event_id, game_state):
                if self._handle_event_activation(event_id, event, game_state):
                    activated_events.append(event_id)
                    
        return activated_events

    def _can_activate_event(self, event_id: str, game_state: Dict) -> bool:
        """Check if an event can be activated"""
        # Check dependencies
        if event_id in self.event_dependencies:
            for dep in self.event_dependencies[event_id]:
                if dep.required_status == "completed" and dep.event_id not in self.completed_events:
                    return False
                if dep.required_status == "failed" and dep.event_id not in self.failed_events:
                    return False
                if dep.required_status == "active" and dep.event_id not in self.active_events:
                    return False
                    
        # Check conflicts
        if event_id in self.event_conflicts:
            for conflict_id in self.event_conflicts[event_id]:
                if conflict_id in self.active_events:
                    # If conflicting event has higher priority, this event can't activate
                    if self.event_priorities[conflict_id].value > self.event_priorities[event_id].value:
                        return False
                        
        return True

    def _handle_event_activation(self, event_id: str, event: Event, game_state: Dict) -> bool:
        """Handle the activation of an event based on its type"""
        success = False
        
        if event.event_type == EventType.FACTION:
            success = self._handle_faction_event(event_id, event, game_state)
        elif event.event_type == EventType.COMBAT:
            success = self._handle_combat_event(event_id, event, game_state)
        elif event.event_type == EventType.RITUAL:
            success = self._handle_ritual_event(event_id, event, game_state)
            
        if success:
            self.visualization.update_event_status(event_id, "active")
            
        return success

    def _handle_faction_event(self, event_id: str, event: Event, game_state: Dict) -> bool:
        """Handle faction-specific event activation"""
        # Extract faction information from event
        faction_id = event_id.split('_')[2] if len(event_id.split('_')) > 2 else None
        if not faction_id:
            return False
            
        # Check for territory conflicts
        territory_id = event_id.split('_')[3] if len(event_id.split('_')) > 3 else None
        if territory_id and territory_id in self.faction_handler.active_conflicts:
            return False
            
        return True

    def _handle_combat_event(self, event_id: str, event: Event, game_state: Dict) -> bool:
        """Handle combat-specific event activation"""
        # Check if there are any participants
        participants = self.combat_handler.get_combat_participants(event_id)
        if not participants:
            return False
            
        # Update combat state
        outcomes = self.combat_handler.update_combat_state(event_id, game_state)
        return bool(outcomes)

    def _handle_ritual_event(self, event_id: str, event: Event, game_state: Dict) -> bool:
        """Handle ritual-specific event activation"""
        # Check ritual requirements
        if event_id not in self.ritual_handler.active_rituals:
            return False
            
        # Update ritual state
        success_prob = self.ritual_handler.update_ritual_state(event_id, game_state)
        return success_prob > 0.0

    def resolve_event(self, event_id: str, success: bool):
        """Resolve an event and update dependencies"""
        if event_id not in self.active_events:
            return
            
        if success:
            self.completed_events.append(event_id)
            self.visualization.update_event_status(event_id, "completed")
        else:
            self.failed_events.append(event_id)
            self.visualization.update_event_status(event_id, "failed")
            
        # Remove from active events
        del self.active_events[event_id]
        
        # Clean up conflicts
        if event_id in self.event_conflicts:
            del self.event_conflicts[event_id]
        for conflicts in self.event_conflicts.values():
            conflicts.discard(event_id)

    def get_active_chain_events(self, chain_id: str) -> List[str]:
        """Get all active events in a chain"""
        if chain_id not in self.event_chains:
            return []
            
        return [
            event_id for event_id in self.event_chains[chain_id]
            if event_id in self.active_events
        ]

    def _get_event_effects(self, event: Event) -> List[str]:
        """Get all effects of an event"""
        effects = []
        
        if event.effects.faction_reputation_changes:
            effects.extend(f"Reputation: {faction}" for faction in event.effects.faction_reputation_changes)
        if event.effects.territory_effects:
            effects.extend(f"Territory: {effect}" for effect in event.effects.territory_effects.values())
        if event.effects.celestial_effects:
            effects.extend(f"Celestial: {effect}" for effect in event.effects.celestial_effects)
        if event.effects.environmental_changes:
            effects.extend(f"Environment: {effect}" for effect in event.effects.environmental_changes)
            
        return effects

    def get_event_status(self, event_id: str) -> Optional[str]:
        """Get the current status of an event"""
        if event_id in self.active_events:
            return "active"
        if event_id in self.completed_events:
            return "completed"
        if event_id in self.failed_events:
            return "failed"
        return None

    def get_blocking_events(self, event_id: str) -> List[str]:
        """Get events blocking the activation of an event"""
        blocking = []
        
        # Check dependencies
        if event_id in self.event_dependencies:
            for dep in self.event_dependencies[event_id]:
                if not self._dependency_satisfied(dep):
                    blocking.append(dep.event_id)
                    
        # Check conflicts
        if event_id in self.event_conflicts:
            for conflict_id in self.event_conflicts[event_id]:
                if conflict_id in self.active_events:
                    if self.event_priorities[conflict_id].value >= self.event_priorities[event_id].value:
                        blocking.append(conflict_id)
                        
        return blocking

    def _dependency_satisfied(self, dependency: EventDependency) -> bool:
        """Check if a dependency is satisfied"""
        if dependency.required_status == "completed":
            return dependency.event_id in self.completed_events
        if dependency.required_status == "failed":
            return dependency.event_id in self.failed_events
        if dependency.required_status == "active":
            return dependency.event_id in self.active_events
        return False 