from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import random
from visual_system import VisualSystem, TextColor, EnvironmentMood

class Weather(Enum):
    CLEAR = "Clear"      # ☀️
    RAINY = "Rainy"     # 🌧️
    FOGGY = "Foggy"     # 🌫️
    STORMY = "Stormy"   # ⛈️
    WINDY = "Windy"     # 💨
    SNOWY = "Snowy"     # ❄️

class TimeOfDay(Enum):
    DAWN = "Dawn"       # 🌅
    MORNING = "Morning" # 🌄
    NOON = "Noon"      # ☀️
    EVENING = "Evening" # 🌇
    NIGHT = "Night"    # 🌙
    MIDNIGHT = "Midnight" # 🌑

class TerrainType(Enum):
    PLAINS = "Plains"          # 🌾
    FOREST = "Forest"          # 🌲
    MOUNTAIN = "Mountain"      # ⛰️
    DESERT = "Desert"          # 🏜️
    TUNDRA = "Tundra"         # ❄️
    COASTAL = "Coastal"        # 🌊
    MYSTICAL = "Mystical"      # ✨
    CORRUPTED = "Corrupted"    # 💀
    CELESTIAL = "Celestial"    # 🌟
    VOID = "Void"             # 🌌

class AdvancedTerrainType(Enum):
    CRYSTAL_CAVERNS = "Crystal Caverns"    # 💎
    ASTRAL_PLAINS = "Astral Plains"        # 🌠
    SHADOW_REALM = "Shadow Realm"          # 👻
    ANCIENT_RUINS = "Ancient Ruins"        # 🏛️
    ETHEREAL_VOID = "Ethereal Void"        # 🌌
    LIVING_FOREST = "Living Forest"        # 🌳
    ELEMENTAL_PEAKS = "Elemental Peaks"    # 🗻
    TEMPORAL_RIFTS = "Temporal Rifts"      # ⌛
    DREAM_NEXUS = "Dream Nexus"            # 💫
    CHAOS_WASTES = "Chaos Wastes"          # 🌋

class WeatherEffect(Enum):
    ARCANE_STORM = "Arcane Storm"      # ⚡
    VOID_MIST = "Void Mist"            # 🌫️
    CELESTIAL_RAIN = "Celestial Rain"   # ✨
    CHAOS_WINDS = "Chaos Winds"         # 🌪️
    TIME_DISTORTION = "Time Distortion" # ⌛
    REALITY_FLUX = "Reality Flux"       # 🌌

class AdvancedEnvironmentType(Enum):
    REALITY_NEXUS = "Reality Nexus"      # 🌐
    SOUL_SANCTUM = "Soul Sanctum"        # 👻
    PRIMAL_CORE = "Primal Core"          # 🌋
    CELESTIAL_SPIRE = "Celestial Spire"  # 🗼
    VOID_BREACH = "Void Breach"          # 🕳️
    DREAM_WEAVE = "Dream Weave"          # 💫
    TIME_FRACTURE = "Time Fracture"      # ⌛
    CHAOS_MATRIX = "Chaos Matrix"        # 🌀

class AdvancedHazardType(Enum):
    REALITY_STORM = "Reality Storm"      # 🌪️
    VOID_RUPTURE = "Void Rupture"        # 🕳️
    TIME_PARADOX = "Time Paradox"        # ⌛
    MIND_FRACTURE = "Mind Fracture"      # 🧠
    CHAOS_BREACH = "Chaos Breach"        # 🌀
    ESSENCE_SURGE = "Essence Surge"      # ✨
    DIMENSIONAL_COLLAPSE = "Dimensional Collapse"  # 🌌
    SOUL_STORM = "Soul Storm"                     # 👻
    PRIMAL_SURGE = "Primal Surge"                # 🌋
    COSMIC_ANOMALY = "Cosmic Anomaly"            # 🌠
    ENTROPY_WAVE = "Entropy Wave"                # 🌀
    REALITY_QUAKE = "Reality Quake"              # 💫

class AdvancedHazardVariation(Enum):
    REALITY_STORM_PRIME = "Reality Storm Prime"    # 🌀
    VOID_MAELSTROM = "Void Maelstrom"             # 🕳️
    CHRONO_RUPTURE = "Chrono Rupture"             # ⏰
    MIND_LABYRINTH = "Mind Labyrinth"             # 🧠
    ESSENCE_VORTEX = "Essence Vortex"             # 💫
    CHAOS_NEXUS = "Chaos Nexus"                   # 🌀

@dataclass
class Location:
    name: str
    description: str
    environment_type: str
    danger_level: int
    required_level: int = 1
    weather: Weather = Weather.CLEAR
    time: TimeOfDay = TimeOfDay.NOON
    discovered: bool = False
    connected_locations: Set[str] = None
    npcs: List[str] = None
    points_of_interest: List[str] = None
    
    def __post_init__(self):
        if self.connected_locations is None:
            self.connected_locations = set()
        if self.npcs is None:
            self.npcs = []
        if self.points_of_interest is None:
            self.points_of_interest = []

class ExplorationManager:
    def __init__(self, visual_system: VisualSystem):
        self.visual = visual_system
        self.locations: Dict[str, Location] = {}
        self.current_location: Optional[str] = None
        self.time_of_day = TimeOfDay.DAWN
        self.initialize_locations()
        self.discovered_locations = set()
        
    def initialize_locations(self):
        """Initialize game locations"""
        # Starting town
        self.locations["nexus_city"] = Location(
            name="Nexus City",
            description="A bustling hub of commerce and adventure",
            environment_type="urban",
            danger_level=1,
            npcs=["merchant", "guard", "innkeeper"],
            points_of_interest=[
                "marketplace",
                "inn",
                "blacksmith"
            ]
        )
        
        # Mystical locations
        self.locations["aeon_temple"] = Location(
            name="Aeon Temple",
            description="An ancient temple pulsing with mysterious energy",
            environment_type="temple",
            danger_level=8,
            required_level=5,
            npcs=["temple_guardian", "mystic"],
            points_of_interest=[
                "meditation_chamber",
                "artifact_vault",
                "energy_well"
            ]
        )
        
        # Connect locations
        self.locations["nexus_city"].connected_locations.add("aeon_temple")
        
    def get_available_actions(self, player_level: int) -> List[str]:
        """Get available actions for current location"""
        if not self.current_location:
            return []
            
        location = self.locations[self.current_location]
        actions = []
        
        # Movement options
        for connected in location.connected_locations:
            target = self.locations[connected]
            if player_level >= target.required_level:
                actions.append(f"Travel to {target.name}")
        
        # NPC interactions
        for npc in location.npcs:
            actions.append(f"Talk to {npc.replace('_', ' ').title()}")
        
        # Points of interest
        for poi in location.points_of_interest:
            actions.append(f"Examine {poi.replace('_', ' ').title()}")
        
        # Basic actions
        actions.extend([
            "Search area",
            "Rest",
            "Check inventory",
            "View map"
        ])
        
        return actions
        
    def update_environment(self):
        """Update weather and time of day"""
        # Advance time
        current_time = list(TimeOfDay).index(self.time_of_day)
        self.time_of_day = list(TimeOfDay)[(current_time + 1) % len(TimeOfDay)]
        
        # Random weather changes
        if random.random() < 0.2:  # 20% chance
            self.locations[self.current_location].weather = random.choice(list(Weather))
            
    def get_environment_effects(self) -> Dict[str, float]:
        """Get current environmental effects"""
        location = self.locations[self.current_location]
        effects = {}
        
        # Weather effects
        if location.weather == Weather.RAINY:
            effects["movement_speed"] = 0.8
            effects["visibility"] = 0.7
        elif location.weather == Weather.FOGGY:
            effects["visibility"] = 0.5
            effects["ambush_chance"] = 1.2
        
        # Time effects
        if location.time == TimeOfDay.NIGHT:
            effects["visibility"] = effects.get("visibility", 1.0) * 0.6
            effects["enemy_strength"] = 1.2
        elif location.time == TimeOfDay.DAWN:
            effects["merchant_prices"] = 0.9
        
        return effects
        
    def describe_location(self) -> str:
        """Get current location description"""
        if not self.current_location:
            return "You are lost in the void."
            
        location = self.locations[self.current_location]
        
        # Build description
        description = [
            f"\n=== {location.name} ===",
            location.description,
            f"\nTime: {location.time.value} {self._get_time_icon(location.time)}",
            f"Weather: {location.weather.value} {self._get_weather_icon(location.weather)}"
        ]
        
        # Add visible NPCs
        if location.npcs:
            description.append("\nPresent NPCs:")
            for npc in location.npcs:
                description.append(f"- {npc.replace('_', ' ').title()}")
        
        # Add points of interest
        if location.points_of_interest:
            description.append("\nPoints of Interest:")
            for poi in location.points_of_interest:
                description.append(f"- {poi.replace('_', ' ').title()}")
        
        return "\n".join(description)
        
    def _get_weather_icon(self, weather: Weather) -> str:
        """Get icon for weather type"""
        icons = {
            Weather.CLEAR: "☀️",
            Weather.RAINY: "🌧️",
            Weather.FOGGY: "🌫️",
            Weather.STORMY: "⛈️",
            Weather.WINDY: "💨",
            Weather.SNOWY: "❄️"
        }
        return icons.get(weather, "")
        
    def _get_time_icon(self, time: TimeOfDay) -> str:
        """Get icon for time of day"""
        icons = {
            TimeOfDay.DAWN: "🌅",
            TimeOfDay.MORNING: "🌄",
            TimeOfDay.NOON: "☀️",
            TimeOfDay.EVENING: "🌇",
            TimeOfDay.NIGHT: "🌙",
            TimeOfDay.MIDNIGHT: "🌑"
        }
        return icons.get(time, "") 

    def update_weather(self):
        """Randomly change the weather condition and apply effects."""
        self.weather = random.choice(["Sunny", "Rainy", "Foggy", "Snowy"])
        if self.weather == "Rainy":
            print("It's raining! Paths may be slippery.") 

    def explore_location(self, location_id):
        """Explore a specific location and reward the player."""
        print(f"You explore {location_id}.")
        self.player.experience += 10  # Reward for exploration
        print("You gained 10 experience points!") 

    def apply_weather_effects(self):
        """Apply effects based on current weather."""
        if self.weather == "Foggy":
            print("Visibility is reduced due to fog. Proceed with caution!")
        elif self.weather == "Rainy":
            print("The ground is slippery. Movement may be affected.") 

    def trigger_dynamic_event(self, location):
        """Trigger a dynamic event based on the player's location."""
        if location == "Elysia Town":
            print("You encounter a merchant offering rare items!")
        elif location == "Frosthaven":
            print("A snowstorm approaches! Seek shelter!") 

    def discover_location(self, location_id):
        """Mark a location as discovered."""
        self.discovered_locations.add(location_id)
        print(f"You have discovered {location_id}!")
        print(f"Total discovered locations: {len(self.discovered_locations)}") 