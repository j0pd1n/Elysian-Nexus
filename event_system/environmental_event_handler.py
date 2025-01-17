from typing import Dict, List, Optional, Set
import random
from dataclasses import dataclass
from .event_manager import Event, EventType, EventTrigger, EventRequirements, EventEffects

@dataclass
class EnvironmentalCondition:
    name: str
    intensity_range: tuple[float, float]
    compatible_conditions: List[str]
    incompatible_conditions: List[str]
    resource_effects: Dict[str, float]
    territory_effects: Dict[str, str]

@dataclass
class WeatherPattern:
    primary_condition: str
    secondary_conditions: List[str]
    intensity: float
    duration: int
    effects: List[str]

class EnvironmentalEventHandler:
    def __init__(self):
        self.conditions: Dict[str, EnvironmentalCondition] = {
            "magical_storm": EnvironmentalCondition(
                name="Magical Storm",
                intensity_range=(1.2, 2.0),
                compatible_conditions=["mana_surge", "lightning", "wind"],
                incompatible_conditions=["clear_sky", "void_mist"],
                resource_effects={
                    "mana": 1.5,
                    "storm_essence": 2.0,
                    "lightning_crystal": 1.8
                },
                territory_effects={
                    "magical_surge": "Increases magical energy in the area",
                    "storm_damage": "May damage certain structures"
                }
            ),
            "void_mist": EnvironmentalCondition(
                name="Void Mist",
                intensity_range=(1.1, 1.8),
                compatible_conditions=["darkness", "shadow", "cold"],
                incompatible_conditions=["clear_sky", "magical_storm"],
                resource_effects={
                    "void_essence": 1.8,
                    "shadow_crystal": 1.6,
                    "dark_matter": 1.4
                },
                territory_effects={
                    "void_seepage": "Void energy seeps into the area",
                    "visibility_reduction": "Reduces visibility significantly"
                }
            ),
            "ley_surge": EnvironmentalCondition(
                name="Ley Line Surge",
                intensity_range=(1.3, 2.2),
                compatible_conditions=["magical_storm", "mana_surge", "crystal_growth"],
                incompatible_conditions=["void_mist", "null_zone"],
                resource_effects={
                    "ley_crystal": 2.0,
                    "pure_mana": 1.7,
                    "magical_ore": 1.5
                },
                territory_effects={
                    "ley_enhancement": "Enhances magical properties",
                    "crystal_formation": "Accelerates crystal formation"
                }
            )
        }
        
        self.current_pattern: Optional[WeatherPattern] = None
        self.active_conditions: Set[str] = set()

    def generate_environmental_event(
        self,
        game_state: Dict,
        territory: Optional[str] = None
    ) -> Event:
        """Generate an environmental event based on current game state"""
        # Select primary condition based on current pattern or random choice
        primary_condition = (
            self.current_pattern.primary_condition if self.current_pattern
            else random.choice(list(self.conditions.keys()))
        )
        
        # Calculate base intensity and duration
        base_intensity = self._calculate_base_intensity(game_state)
        base_duration = self._calculate_base_duration(game_state)
        
        # Generate effects based on condition
        effects = self._generate_condition_effects(primary_condition, base_intensity)
        
        # Add territory-specific effects if applicable
        if territory:
            effects = self._add_territory_effects(effects, territory, game_state)
            
        event_id = f"environmental_{primary_condition}_{int(random.random() * 10000)}"
        
        return Event(
            event_id=event_id,
            name=f"{self.conditions[primary_condition].name}",
            event_type=EventType.ENVIRONMENTAL,
            trigger=EventTrigger.TIME,
            requirements=self._generate_requirements(game_state, primary_condition),
            effects=effects,
            duration=base_duration,
            cooldown=base_duration * 2
        )

    def update_weather_pattern(self, game_state: Dict) -> None:
        """Update the current weather pattern"""
        if not self.current_pattern or random.random() < 0.15:  # 15% chance to change pattern
            primary = random.choice(list(self.conditions.keys()))
            condition_data = self.conditions[primary]
            
            # Select compatible secondary conditions
            available_secondary = [
                cond for cond in condition_data.compatible_conditions
                if cond not in condition_data.incompatible_conditions
            ]
            
            secondary = random.sample(
                available_secondary,
                min(2, len(available_secondary))  # Up to 2 secondary conditions
            )
            
            self.current_pattern = WeatherPattern(
                primary_condition=primary,
                secondary_conditions=secondary,
                intensity=random.uniform(
                    condition_data.intensity_range[0],
                    condition_data.intensity_range[1]
                ),
                duration=random.randint(300, 900),  # 5-15 minutes
                effects=self._generate_pattern_effects(primary, secondary)
            )

    def get_active_conditions(self) -> Set[str]:
        """Get currently active environmental conditions"""
        return self.active_conditions.copy()

    def _calculate_base_intensity(self, game_state: Dict) -> float:
        """Calculate base intensity for environmental events"""
        base = 1.0
        
        # Scale with territory instability
        if "territories" in game_state:
            avg_stability = sum(
                t.get("stability", 1.0)
                for t in game_state["territories"].values()
            ) / len(game_state["territories"])
            base *= (2 - avg_stability)  # Lower stability = higher intensity
            
        # Adjust for current pattern
        if self.current_pattern:
            base *= self.current_pattern.intensity
            
        # Consider magical activity
        if "magical_activity" in game_state:
            base *= (1 + game_state["magical_activity"] * 0.2)
            
        return base

    def _calculate_base_duration(self, game_state: Dict) -> int:
        """Calculate base duration for environmental events"""
        base_duration = 600  # 10 minutes
        
        if self.current_pattern:
            base_duration = int(base_duration * self.current_pattern.intensity)
            
        # Adjust for magical stability
        if "magical_stability" in game_state:
            base_duration = int(base_duration * (1 + game_state["magical_stability"] * 0.1))
            
        return base_duration

    def _generate_condition_effects(
        self,
        condition: str,
        base_intensity: float
    ) -> EventEffects:
        """Generate effects based on condition"""
        condition_data = self.conditions[condition]
        intensity = base_intensity * random.uniform(
            condition_data.intensity_range[0],
            condition_data.intensity_range[1]
        )
        
        return EventEffects(
            faction_reputation_changes={},
            resource_changes={
                resource: multiplier * intensity
                for resource, multiplier in condition_data.resource_effects.items()
            },
            environmental_changes=[
                condition,
                *condition_data.compatible_conditions[:2]  # Add up to 2 compatible conditions
            ],
            spawned_entities=[
                f"{condition}_manifestation_{i}"
                for i in range(int(intensity))
            ],
            celestial_effects=[],
            territory_effects={
                effect: description
                for effect, description in condition_data.territory_effects.items()
            }
        )

    def _generate_requirements(
        self,
        game_state: Dict,
        condition: str
    ) -> EventRequirements:
        """Generate requirements for environmental events"""
        return EventRequirements(
            player_level=None,  # No level requirement for environmental events
            faction_reputation=None,
            completed_events=None,
            celestial_alignment=None,
            environmental_conditions=[
                cond for cond in self.conditions[condition].compatible_conditions
                if cond in game_state.get("current_conditions", [])
            ][:2],  # Require up to 2 compatible conditions
            required_items=None
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
            # Add territory-specific effects based on features
            if "magical_nodes" in territory_data:
                effects.territory_effects["magical_resonance"] = (
                    "Magical nodes resonate with the environmental energy"
                )
                
            if "stability" in territory_data:
                stability = territory_data["stability"]
                if stability < 0.5:
                    effects.territory_effects["instability_surge"] = (
                        "Environmental effects are amplified by territory instability"
                    )
                
            # Affect resource nodes
            if "resource_nodes" in territory_data:
                for node in territory_data["resource_nodes"]:
                    effects.resource_changes[node] = 1.0 + random.uniform(0.2, 0.5)
                    
        return effects

    def _generate_pattern_effects(
        self,
        primary: str,
        secondary: List[str]
    ) -> List[str]:
        """Generate effects for weather patterns"""
        condition_data = self.conditions[primary]
        effects = [
            f"{primary}_dominance",
            f"{primary}_intensification",
            *[f"{effect}_enhancement" for effect in condition_data.compatible_conditions]
        ]
        
        for secondary_condition in secondary:
            effects.extend([
                f"{secondary_condition}_influence",
                f"{secondary_condition}_minor_effect"
            ])
            
        return effects 