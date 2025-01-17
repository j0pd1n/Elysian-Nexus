import json
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from pathlib import Path
from .event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects
from .event_orchestrator import EventOrchestrator, EventPriority, EventDependency

class EventPersistence:
    def __init__(self, save_directory: str = "saves/events"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(parents=True, exist_ok=True)

    def save_event_state(self, orchestrator: EventOrchestrator, save_name: str):
        """Save the current state of all events"""
        save_data = {
            "active_events": self._serialize_events(orchestrator.active_events),
            "event_dependencies": self._serialize_dependencies(orchestrator.event_dependencies),
            "event_priorities": {k: v.value for k, v in orchestrator.event_priorities.items()},
            "event_conflicts": {k: list(v) for k, v in orchestrator.event_conflicts.items()},
            "event_chains": orchestrator.event_chains,
            "completed_events": orchestrator.completed_events,
            "failed_events": orchestrator.failed_events,
            
            # Save handler-specific states
            "faction_state": self._serialize_faction_state(orchestrator.faction_handler),
            "combat_state": self._serialize_combat_state(orchestrator.combat_handler),
            "ritual_state": self._serialize_ritual_state(orchestrator.ritual_handler)
        }
        
        save_path = self.save_directory / f"{save_name}.json"
        with save_path.open('w') as f:
            json.dump(save_data, f, indent=2)

    def load_event_state(self, orchestrator: EventOrchestrator, save_name: str) -> bool:
        """Load event state from a save file"""
        save_path = self.save_directory / f"{save_name}.json"
        if not save_path.exists():
            return False
            
        try:
            with save_path.open('r') as f:
                save_data = json.load(f)
                
            # Clear current state
            orchestrator.active_events.clear()
            orchestrator.event_dependencies.clear()
            orchestrator.event_priorities.clear()
            orchestrator.event_conflicts.clear()
            orchestrator.event_chains.clear()
            orchestrator.completed_events.clear()
            orchestrator.failed_events.clear()
            
            # Restore events and their properties
            orchestrator.active_events = self._deserialize_events(save_data["active_events"])
            orchestrator.event_dependencies = self._deserialize_dependencies(save_data["event_dependencies"])
            orchestrator.event_priorities = {k: EventPriority(v) for k, v in save_data["event_priorities"].items()}
            orchestrator.event_conflicts = {k: set(v) for k, v in save_data["event_conflicts"].items()}
            orchestrator.event_chains = save_data["event_chains"]
            orchestrator.completed_events = save_data["completed_events"]
            orchestrator.failed_events = save_data["failed_events"]
            
            # Restore handler states
            self._restore_faction_state(orchestrator.faction_handler, save_data["faction_state"])
            self._restore_combat_state(orchestrator.combat_handler, save_data["combat_state"])
            self._restore_ritual_state(orchestrator.ritual_handler, save_data["ritual_state"])
            
            # Rebuild visualization
            self._rebuild_visualization(orchestrator)
            
            return True
            
        except Exception as e:
            print(f"Error loading event state: {e}")
            return False

    def _serialize_events(self, events: Dict[str, Event]) -> Dict[str, Dict]:
        """Convert Event objects to serializable dictionaries"""
        return {
            event_id: {
                "event_id": event.event_id,
                "name": event.name,
                "event_type": event.event_type.value,
                "trigger": event.trigger.value,
                "requirements": asdict(event.requirements),
                "effects": asdict(event.effects),
                "duration": event.duration,
                "cooldown": event.cooldown,
                "chain_id": event.chain_id,
                "next_events": event.next_events
            }
            for event_id, event in events.items()
        }

    def _deserialize_events(self, event_data: Dict[str, Dict]) -> Dict[str, Event]:
        """Convert serialized data back to Event objects"""
        events = {}
        for event_id, data in event_data.items():
            events[event_id] = Event(
                event_id=data["event_id"],
                name=data["name"],
                event_type=EventType[data["event_type"]],
                trigger=EventTrigger[data["trigger"]],
                requirements=EventRequirements(**data["requirements"]),
                effects=EventEffects(**data["effects"]),
                duration=data["duration"],
                cooldown=data["cooldown"],
                chain_id=data.get("chain_id"),
                next_events=data.get("next_events", [])
            )
        return events

    def _serialize_dependencies(self, dependencies: Dict[str, List[EventDependency]]) -> Dict[str, List[Dict]]:
        """Convert EventDependency objects to serializable dictionaries"""
        return {
            event_id: [
                {
                    "event_id": dep.event_id,
                    "required_status": dep.required_status,
                    "priority": dep.priority.value
                }
                for dep in deps
            ]
            for event_id, deps in dependencies.items()
        }

    def _deserialize_dependencies(self, dep_data: Dict[str, List[Dict]]) -> Dict[str, List[EventDependency]]:
        """Convert serialized data back to EventDependency objects"""
        dependencies = {}
        for event_id, deps in dep_data.items():
            dependencies[event_id] = [
                EventDependency(
                    event_id=dep["event_id"],
                    required_status=dep["required_status"],
                    priority=EventPriority(dep["priority"])
                )
                for dep in deps
            ]
        return dependencies

    def _serialize_faction_state(self, faction_handler: Any) -> Dict:
        """Serialize faction handler state"""
        return {
            "relationships": {
                k: dict(v) for k, v in faction_handler.faction_relationships.items()
            },
            "territory_control": faction_handler.territory_control,
            "active_conflicts": list(faction_handler.active_conflicts),
            "alliance_networks": {
                k: list(v) for k, v in faction_handler.alliance_networks.items()
            }
        }

    def _serialize_combat_state(self, combat_handler: Any) -> Dict:
        """Serialize combat handler state"""
        return {
            "active_combats": {
                combat_id: [asdict(p) for p in participants]
                for combat_id, participants in combat_handler.active_combats.items()
            },
            "combat_outcomes": combat_handler.combat_outcomes,
            "territory_conflicts": {
                k: list(v) for k, v in combat_handler.territory_conflicts.items()
            }
        }

    def _serialize_ritual_state(self, ritual_handler: Any) -> Dict:
        """Serialize ritual handler state"""
        return {
            "active_rituals": {
                ritual_id: asdict(circle)
                for ritual_id, circle in ritual_handler.active_rituals.items()
            },
            "ritual_outcomes": ritual_handler.ritual_outcomes,
            "celestial_influences": ritual_handler.celestial_influences
        }

    def _restore_faction_state(self, faction_handler: Any, state_data: Dict):
        """Restore faction handler state"""
        faction_handler.faction_relationships = {
            k: {k2: v2 for k2, v2 in v.items()}
            for k, v in state_data["relationships"].items()
        }
        faction_handler.territory_control = state_data["territory_control"]
        faction_handler.active_conflicts = set(state_data["active_conflicts"])
        faction_handler.alliance_networks = {
            k: set(v) for k, v in state_data["alliance_networks"].items()
        }

    def _restore_combat_state(self, combat_handler: Any, state_data: Dict):
        """Restore combat handler state"""
        from .combat_event_handler import CombatParticipant
        
        combat_handler.active_combats = {
            combat_id: [
                CombatParticipant(**p_data)
                for p_data in participants
            ]
            for combat_id, participants in state_data["active_combats"].items()
        }
        combat_handler.combat_outcomes = state_data["combat_outcomes"]
        combat_handler.territory_conflicts = {
            k: set(v) for k, v in state_data["territory_conflicts"].items()
        }

    def _restore_ritual_state(self, ritual_handler: Any, state_data: Dict):
        """Restore ritual handler state"""
        from .ritual_event_handler import RitualCircle, RitualComponent
        
        ritual_handler.active_rituals = {
            ritual_id: RitualCircle(
                components=[RitualComponent(**c) for c in circle_data["components"]],
                position=tuple(circle_data["position"]),
                active_effects=circle_data["active_effects"],
                power_level=circle_data["power_level"],
                stability=circle_data["stability"]
            )
            for ritual_id, circle_data in state_data["active_rituals"].items()
        }
        ritual_handler.ritual_outcomes = state_data["ritual_outcomes"]
        ritual_handler.celestial_influences = state_data["celestial_influences"]

    def _rebuild_visualization(self, orchestrator: EventOrchestrator):
        """Rebuild the visualization state"""
        # Clear current visualization
        orchestrator.visualization.event_nodes.clear()
        orchestrator.visualization.occupied_positions.clear()
        orchestrator.visualization.ui_components.clear()
        
        # Rebuild nodes for active events
        for event_id, event in orchestrator.active_events.items():
            orchestrator.visualization.add_event_node(
                event=event,
                description=f"{event.name} (Priority: {orchestrator.event_priorities[event_id].name})",
                effects=orchestrator._get_event_effects(event)
            )
            
        # Rebuild connections from dependencies
        for event_id, dependencies in orchestrator.event_dependencies.items():
            for dep in dependencies:
                orchestrator.visualization.connect_events(dep.event_id, event_id)

    def list_saves(self) -> List[str]:
        """List all available save files"""
        return [f.stem for f in self.save_directory.glob("*.json")]

    def delete_save(self, save_name: str) -> bool:
        """Delete a save file"""
        save_path = self.save_directory / f"{save_name}.json"
        if save_path.exists():
            save_path.unlink()
            return True
        return False 