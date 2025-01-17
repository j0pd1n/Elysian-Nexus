from typing import Dict, List, Optional
import random
from .event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects

class EventGenerator:
    def __init__(self):
        self.event_templates: Dict[str, Dict] = {
            "celestial": {
                "convergence": {
                    "name": "Celestial Convergence",
                    "type": EventType.CELESTIAL,
                    "base_duration": 3600,  # 1 hour
                    "base_cooldown": 86400,  # 24 hours
                    "effects": {
                        "magical_amplification": (1.5, 2.5),
                        "reality_instability": (0.1, 0.3),
                        "dimensional_rifts": True
                    }
                },
                "void_eclipse": {
                    "name": "Void Eclipse",
                    "type": EventType.CELESTIAL,
                    "base_duration": 1800,  # 30 minutes
                    "base_cooldown": 43200,  # 12 hours
                    "effects": {
                        "void_power": (1.3, 2.0),
                        "shadow_manifestation": True,
                        "reality_distortion": (0.2, 0.4)
                    }
                }
            },
            "environmental": {
                "magical_storm": {
                    "name": "Magical Storm",
                    "type": EventType.ENVIRONMENTAL,
                    "base_duration": 900,  # 15 minutes
                    "base_cooldown": 3600,  # 1 hour
                    "effects": {
                        "mana_surge": (1.2, 1.8),
                        "lightning_strikes": True,
                        "weather_chaos": (0.1, 0.3)
                    }
                },
                "ley_line_surge": {
                    "name": "Ley Line Surge",
                    "type": EventType.ENVIRONMENTAL,
                    "base_duration": 1200,  # 20 minutes
                    "base_cooldown": 7200,  # 2 hours
                    "effects": {
                        "magical_resonance": (1.4, 2.0),
                        "energy_manifestation": True,
                        "territorial_shift": (0.2, 0.4)
                    }
                }
            },
            "faction": {
                "ritual_gathering": {
                    "name": "Ritual Gathering",
                    "type": EventType.FACTION,
                    "base_duration": 1800,  # 30 minutes
                    "base_cooldown": 21600,  # 6 hours
                    "effects": {
                        "faction_power": (1.3, 1.7),
                        "ritual_bonus": True,
                        "territory_control": (0.1, 0.3)
                    }
                },
                "power_struggle": {
                    "name": "Power Struggle",
                    "type": EventType.FACTION,
                    "base_duration": 3600,  # 1 hour
                    "base_cooldown": 43200,  # 12 hours
                    "effects": {
                        "combat_intensity": (1.4, 1.8),
                        "territory_instability": True,
                        "reputation_flux": (0.2, 0.4)
                    }
                }
            }
        }

    def generate_event_chain(
        self,
        chain_id: str,
        length: int,
        event_types: List[EventType],
        base_requirements: EventRequirements
    ) -> List[Event]:
        """Generate a chain of related events"""
        events = []
        current_requirements = base_requirements
        
        for i in range(length):
            event_type = random.choice(event_types)
            template_category = self._get_template_category(event_type)
            template = random.choice(list(self.event_templates[template_category].values()))
            
            event_id = f"{chain_id}_{i}"
            
            # Scale requirements based on position in chain
            scaled_requirements = self._scale_requirements(current_requirements, i, length)
            
            # Generate effects
            effects = self._generate_effects(template["effects"], i, length)
            
            event = Event(
                event_id=event_id,
                name=f"{template['name']} {i+1}",
                event_type=template["type"],
                trigger=EventTrigger.TIME if i == 0 else EventTrigger.RITUAL_COMPLETION,
                requirements=scaled_requirements,
                effects=effects,
                duration=template["base_duration"],
                cooldown=template["base_cooldown"],
                chain_id=chain_id,
                next_events=[f"{chain_id}_{i+1}"] if i < length-1 else None
            )
            
            events.append(event)
            current_requirements = scaled_requirements
            
        return events

    def generate_dynamic_event(
        self,
        event_type: EventType,
        game_state: Dict,
        territory: Optional[str] = None
    ) -> Event:
        """Generate a single dynamic event based on game state"""
        template_category = self._get_template_category(event_type)
        template = random.choice(list(self.event_templates[template_category].values()))
        
        # Generate requirements based on game state
        requirements = self._generate_requirements(game_state, event_type)
        
        # Generate effects
        effects = self._generate_effects(template["effects"], 0, 1)
        
        # Add territory-specific modifications if applicable
        if territory:
            effects = self._add_territory_effects(effects, territory, game_state)
            
        event_id = f"dynamic_{event_type.name.lower()}_{int(random.random() * 10000)}"
        
        return Event(
            event_id=event_id,
            name=template["name"],
            event_type=template["type"],
            trigger=EventTrigger.TIME,
            requirements=requirements,
            effects=effects,
            duration=template["base_duration"],
            cooldown=template["base_cooldown"]
        )

    def _get_template_category(self, event_type: EventType) -> str:
        """Convert EventType to template category"""
        return {
            EventType.CELESTIAL: "celestial",
            EventType.ENVIRONMENTAL: "environmental",
            EventType.FACTION: "faction"
        }.get(event_type, "celestial")

    def _scale_requirements(
        self,
        base_requirements: EventRequirements,
        position: int,
        chain_length: int
    ) -> EventRequirements:
        """Scale requirements based on position in chain"""
        scale_factor = 1 + (position / chain_length)
        
        return EventRequirements(
            player_level=base_requirements.player_level and int(base_requirements.player_level * scale_factor),
            faction_reputation={
                k: int(v * scale_factor)
                for k, v in (base_requirements.faction_reputation or {}).items()
            },
            completed_events=base_requirements.completed_events,
            celestial_alignment=base_requirements.celestial_alignment,
            environmental_conditions=base_requirements.environmental_conditions,
            required_items=base_requirements.required_items
        )

    def _generate_effects(
        self,
        template_effects: Dict,
        position: int,
        chain_length: int
    ) -> EventEffects:
        """Generate scaled effects"""
        effects = {}
        scale_factor = 1 + (position / chain_length)
        
        for key, value in template_effects.items():
            if isinstance(value, tuple):
                min_val, max_val = value
                effects[key] = random.uniform(min_val, max_val) * scale_factor
            else:
                effects[key] = value
                
        return EventEffects(
            faction_reputation_changes={"faction1": int(10 * scale_factor)},
            resource_changes={"resource1": 1.5 * scale_factor},
            environmental_changes=["effect1", "effect2"],
            spawned_entities=["entity1", "entity2"],
            celestial_effects=["effect1", "effect2"],
            territory_effects={"territory1": "effect1"}
        )

    def _generate_requirements(
        self,
        game_state: Dict,
        event_type: EventType
    ) -> EventRequirements:
        """Generate requirements based on game state"""
        player_level = game_state.get("player_level", 1)
        
        return EventRequirements(
            player_level=max(1, int(player_level * 0.8)),
            faction_reputation={
                faction: int(rep * 0.7)
                for faction, rep in game_state.get("faction_reputation", {}).items()
            },
            celestial_alignment=random.choice(game_state.get("possible_alignments", [])) if event_type == EventType.CELESTIAL else None,
            environmental_conditions=random.sample(game_state.get("possible_conditions", []), 2) if event_type == EventType.ENVIRONMENTAL else None
        )

    def _add_territory_effects(
        self,
        effects: EventEffects,
        territory: str,
        game_state: Dict
    ) -> EventEffects:
        """Add territory-specific effects"""
        territory_data = game_state.get("territories", {}).get(territory, {})
        
        if territory_data:
            effects.territory_effects = {
                territory: f"territory_effect_{random.randint(1, 3)}"
            }
            
            if "resource_nodes" in territory_data:
                effects.resource_changes.update({
                    node: random.uniform(1.2, 1.5)
                    for node in territory_data["resource_nodes"]
                })
                
        return effects 