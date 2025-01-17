from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Set, Optional, Tuple, Any
import random
import math
from datetime import datetime

from .dimensional_combat import DimensionalLayer, DimensionalEffect
from .ai_behavior import BehaviorType, TacticalRole
from .combat_types import Position, DamageType

class EncounterType(Enum):
    """Types of combat encounters"""
    BOSS = auto()           # Major boss battles
    ELITE = auto()          # Challenging mini-boss encounters
    STANDARD = auto()       # Regular combat encounters
    SWARM = auto()         # Multiple weak enemies
    DIMENSIONAL = auto()    # Dimension-focused encounters
    HYBRID = auto()         # Mixed enemy types

class EncounterPhase(Enum):
    """Phases within an encounter"""
    INTRODUCTION = auto()   # Opening phase
    ESCALATION = auto()     # Difficulty increases
    CLIMAX = auto()        # Peak difficulty
    RESOLUTION = auto()     # Concluding phase

class TerrainType(Enum):
    """Types of combat terrain"""
    OPEN = auto()          # Large open areas
    CONFINED = auto()      # Tight spaces
    ELEVATED = auto()      # Multiple height levels
    HAZARDOUS = auto()     # Environmental hazards
    DIMENSIONAL = auto()   # Reality-warped areas
    DYNAMIC = auto()       # Changing terrain

@dataclass
class EnemyTemplate:
    """Template for generating enemies"""
    name: str
    level_range: Tuple[int, int]
    base_stats: Dict[str, float]
    behavior_types: List[BehaviorType]
    tactical_roles: List[TacticalRole]
    abilities: List[str]
    dimensional_affinities: Dict[DimensionalLayer, float]
    spawn_conditions: Dict[str, Any]
    difficulty_rating: float

@dataclass
class EncounterTemplate:
    """Template for generating encounters"""
    name: str
    encounter_type: EncounterType
    level_range: Tuple[int, int]
    enemy_composition: Dict[str, Tuple[int, int]]  # enemy_template: (min, max)
    terrain_types: List[TerrainType]
    dimensional_properties: Dict[DimensionalLayer, float]
    phase_progression: List[EncounterPhase]
    difficulty_rating: float
    rewards: Dict[str, Any]
    special_conditions: Dict[str, Any]

@dataclass
class SpawnPoint:
    """Represents a point where enemies can spawn"""
    position: Position
    terrain_type: TerrainType
    dimensional_stability: float
    valid_enemy_types: Set[str]
    cooldown: float = 0.0
    last_spawn: Optional[datetime] = None

class EncounterGenerator:
    """Generates dynamic combat encounters"""
    
    def __init__(self):
        self.enemy_templates: Dict[str, EnemyTemplate] = {}
        self.encounter_templates: Dict[str, EncounterTemplate] = {}
        self.spawn_points: List[SpawnPoint] = []
        self.difficulty_curve: Dict[int, float] = {}
        self.last_encounter: Optional[str] = None
        
        self._initialize_templates()
        self._initialize_difficulty_curve()
        
    def _initialize_templates(self) -> None:
        """Initialize default templates"""
        self._add_enemy_templates()
        self._add_encounter_templates()
        
    def _add_enemy_templates(self) -> None:
        """Add default enemy templates"""
        templates = [
            EnemyTemplate(
                name="void_warrior",
                level_range=(1, 10),
                base_stats={
                    'health': 100,
                    'damage': 15,
                    'defense': 10,
                    'speed': 5
                },
                behavior_types=[
                    BehaviorType.AGGRESSIVE,
                    BehaviorType.DIMENSIONAL
                ],
                tactical_roles=[
                    TacticalRole.DPS,
                    TacticalRole.DIMENSIONIST
                ],
                abilities=[
                    'void_slash',
                    'dimensional_step',
                    'reality_tear'
                ],
                dimensional_affinities={
                    DimensionalLayer.PHYSICAL: 0.5,
                    DimensionalLayer.ETHEREAL: 0.8
                },
                spawn_conditions={
                    'min_dimensional_instability': 0.3,
                    'max_allies_nearby': 3
                },
                difficulty_rating=1.2
            ),
            EnemyTemplate(
                name="reality_weaver",
                level_range=(5, 15),
                base_stats={
                    'health': 80,
                    'damage': 20,
                    'defense': 8,
                    'speed': 7
                },
                behavior_types=[
                    BehaviorType.TACTICAL,
                    BehaviorType.DIMENSIONAL
                ],
                tactical_roles=[
                    TacticalRole.CONTROLLER,
                    TacticalRole.DIMENSIONIST
                ],
                abilities=[
                    'reality_warp',
                    'dimensional_surge',
                    'void_bolt'
                ],
                dimensional_affinities={
                    DimensionalLayer.ETHEREAL: 0.9,
                    DimensionalLayer.PHYSICAL: 0.3
                },
                spawn_conditions={
                    'min_dimensional_instability': 0.5,
                    'max_allies_nearby': 2
                },
                difficulty_rating=1.5
            ),
            # New enemy templates
            EnemyTemplate(
                name="celestial_guardian",
                level_range=(15, 25),
                base_stats={
                    'health': 200,
                    'damage': 25,
                    'defense': 18,
                    'speed': 4
                },
                behavior_types=[
                    BehaviorType.DEFENSIVE,
                    BehaviorType.SUPPORT
                ],
                tactical_roles=[
                    TacticalRole.TANK,
                    TacticalRole.HEALER
                ],
                abilities=[
                    'celestial_shield',
                    'healing_light',
                    'divine_intervention',
                    'star_pulse'
                ],
                dimensional_affinities={
                    DimensionalLayer.CELESTIAL: 1.0,
                    DimensionalLayer.VOID: 0.2,
                    DimensionalLayer.PHYSICAL: 0.6
                },
                spawn_conditions={
                    'celestial_presence': True,
                    'min_allies_nearby': 1
                },
                difficulty_rating=2.0
            ),
            EnemyTemplate(
                name="primordial_shaper",
                level_range=(20, 30),
                base_stats={
                    'health': 150,
                    'damage': 30,
                    'defense': 12,
                    'speed': 6
                },
                behavior_types=[
                    BehaviorType.DISRUPTIVE,
                    BehaviorType.DIMENSIONAL
                ],
                tactical_roles=[
                    TacticalRole.CONTROLLER,
                    TacticalRole.DIMENSIONIST
                ],
                abilities=[
                    'reality_reshape',
                    'primordial_blast',
                    'terrain_manipulation',
                    'dimensional_collapse'
                ],
                dimensional_affinities={
                    DimensionalLayer.PRIMORDIAL: 1.0,
                    DimensionalLayer.PHYSICAL: 0.3,
                    DimensionalLayer.ETHEREAL: 0.7
                },
                spawn_conditions={
                    'reality_instability': 0.7,
                    'max_similar_nearby': 1
                },
                difficulty_rating=2.5
            ),
            EnemyTemplate(
                name="ethereal_assassin",
                level_range=(10, 20),
                base_stats={
                    'health': 70,
                    'damage': 35,
                    'defense': 5,
                    'speed': 9
                },
                behavior_types=[
                    BehaviorType.AGGRESSIVE,
                    BehaviorType.TACTICAL
                ],
                tactical_roles=[
                    TacticalRole.ASSASSIN,
                    TacticalRole.DPS
                ],
                abilities=[
                    'phase_strike',
                    'shadow_step',
                    'ethereal_blade',
                    'reality_split'
                ],
                dimensional_affinities={
                    DimensionalLayer.ETHEREAL: 1.0,
                    DimensionalLayer.PHYSICAL: 0.4,
                    DimensionalLayer.VOID: 0.7
                },
                spawn_conditions={
                    'shadow_presence': True,
                    'max_similar_nearby': 2
                },
                difficulty_rating=1.8
            ),
            EnemyTemplate(
                name="void_harbinger",
                level_range=(25, 35),
                base_stats={
                    'health': 300,
                    'damage': 40,
                    'defense': 15,
                    'speed': 5
                },
                behavior_types=[
                    BehaviorType.DISRUPTIVE,
                    BehaviorType.DIMENSIONAL
                ],
                tactical_roles=[
                    TacticalRole.CONTROLLER,
                    TacticalRole.TANK
                ],
                abilities=[
                    'void_eruption',
                    'reality_decay',
                    'corruption_wave',
                    'dimensional_anchor',
                    'entropy_field'
                ],
                dimensional_affinities={
                    DimensionalLayer.VOID: 1.0,
                    DimensionalLayer.PHYSICAL: 0.2,
                    DimensionalLayer.CELESTIAL: 0.1
                },
                spawn_conditions={
                    'void_corruption': 0.8,
                    'max_similar_nearby': 1
                },
                difficulty_rating=3.0
            )
        ]
        
        for template in templates:
            self.enemy_templates[template.name] = template
            
    def _add_encounter_templates(self) -> None:
        """Add default encounter templates"""
        templates = [
            EncounterTemplate(
                name="void_breach",
                encounter_type=EncounterType.DIMENSIONAL,
                level_range=(5, 15),
                enemy_composition={
                    'void_warrior': (2, 4),
                    'reality_weaver': (1, 2)
                },
                terrain_types=[
                    TerrainType.DIMENSIONAL,
                    TerrainType.DYNAMIC
                ],
                dimensional_properties={
                    DimensionalLayer.PHYSICAL: 0.4,
                    DimensionalLayer.ETHEREAL: 0.8
                },
                phase_progression=[
                    EncounterPhase.INTRODUCTION,
                    EncounterPhase.ESCALATION,
                    EncounterPhase.CLIMAX,
                    EncounterPhase.RESOLUTION
                ],
                difficulty_rating=1.8,
                rewards={
                    'experience': 1000,
                    'dimensional_essence': 50,
                    'rare_item_chance': 0.3
                },
                special_conditions={
                    'dimensional_instability': 0.7,
                    'void_presence': True
                }
            ),
            EncounterTemplate(
                name="reality_storm",
                encounter_type=EncounterType.BOSS,
                level_range=(10, 20),
                enemy_composition={
                    'reality_weaver': (2, 3),
                    'void_warrior': (3, 5)
                },
                terrain_types=[
                    TerrainType.DIMENSIONAL,
                    TerrainType.HAZARDOUS,
                    TerrainType.DYNAMIC
                ],
                dimensional_properties={
                    DimensionalLayer.PHYSICAL: 0.3,
                    DimensionalLayer.ETHEREAL: 0.9
                },
                phase_progression=[
                    EncounterPhase.INTRODUCTION,
                    EncounterPhase.ESCALATION,
                    EncounterPhase.CLIMAX,
                    EncounterPhase.RESOLUTION
                ],
                difficulty_rating=2.5,
                rewards={
                    'experience': 2000,
                    'dimensional_essence': 100,
                    'rare_item_chance': 0.6,
                    'unique_item_chance': 0.2
                },
                special_conditions={
                    'dimensional_instability': 0.9,
                    'void_presence': True,
                    'reality_storm': True
                }
            ),
            # New encounter templates
            EncounterTemplate(
                name="celestial_convergence",
                encounter_type=EncounterType.ELITE,
                level_range=(15, 25),
                enemy_composition={
                    'celestial_guardian': (1, 2),
                    'ethereal_assassin': (2, 3),
                    'reality_weaver': (1, 2)
                },
                terrain_types=[
                    TerrainType.ELEVATED,
                    TerrainType.DIMENSIONAL,
                    TerrainType.OPEN
                ],
                dimensional_properties={
                    DimensionalLayer.CELESTIAL: 0.9,
                    DimensionalLayer.ETHEREAL: 0.6,
                    DimensionalLayer.PHYSICAL: 0.4
                },
                phase_progression=[
                    EncounterPhase.INTRODUCTION,
                    EncounterPhase.ESCALATION,
                    EncounterPhase.CLIMAX,
                    EncounterPhase.RESOLUTION
                ],
                difficulty_rating=2.2,
                rewards={
                    'experience': 2500,
                    'celestial_essence': 75,
                    'rare_item_chance': 0.5,
                    'unique_item_chance': 0.15
                },
                special_conditions={
                    'celestial_presence': True,
                    'reality_flux': True
                }
            ),
            EncounterTemplate(
                name="primordial_chaos",
                encounter_type=EncounterType.BOSS,
                level_range=(20, 30),
                enemy_composition={
                    'primordial_shaper': (1, 1),
                    'void_warrior': (3, 4),
                    'reality_weaver': (2, 3)
                },
                terrain_types=[
                    TerrainType.DYNAMIC,
                    TerrainType.HAZARDOUS,
                    TerrainType.DIMENSIONAL
                ],
                dimensional_properties={
                    DimensionalLayer.PRIMORDIAL: 1.0,
                    DimensionalLayer.VOID: 0.7,
                    DimensionalLayer.PHYSICAL: 0.3
                },
                phase_progression=[
                    EncounterPhase.INTRODUCTION,
                    EncounterPhase.ESCALATION,
                    EncounterPhase.CLIMAX,
                    EncounterPhase.RESOLUTION
                ],
                difficulty_rating=3.0,
                rewards={
                    'experience': 3500,
                    'primordial_essence': 100,
                    'rare_item_chance': 0.7,
                    'unique_item_chance': 0.3,
                    'legendary_item_chance': 0.1
                },
                special_conditions={
                    'reality_instability': 0.9,
                    'primordial_surge': True,
                    'terrain_mutation': True
                }
            ),
            EncounterTemplate(
                name="shadow_infiltration",
                encounter_type=EncounterType.SWARM,
                level_range=(10, 20),
                enemy_composition={
                    'ethereal_assassin': (4, 6),
                    'void_warrior': (2, 3)
                },
                terrain_types=[
                    TerrainType.CONFINED,
                    TerrainType.ELEVATED,
                    TerrainType.DYNAMIC
                ],
                dimensional_properties={
                    DimensionalLayer.ETHEREAL: 0.8,
                    DimensionalLayer.VOID: 0.5,
                    DimensionalLayer.PHYSICAL: 0.4
                },
                phase_progression=[
                    EncounterPhase.INTRODUCTION,
                    EncounterPhase.ESCALATION,
                    EncounterPhase.CLIMAX,
                    EncounterPhase.RESOLUTION
                ],
                difficulty_rating=2.0,
                rewards={
                    'experience': 1800,
                    'shadow_essence': 60,
                    'rare_item_chance': 0.4,
                    'stealth_bonus': True
                },
                special_conditions={
                    'shadow_presence': True,
                    'stealth_advantage': True
                }
            ),
            EncounterTemplate(
                name="void_apocalypse",
                encounter_type=EncounterType.BOSS,
                level_range=(25, 35),
                enemy_composition={
                    'void_harbinger': (1, 1),
                    'void_warrior': (4, 6),
                    'reality_weaver': (2, 3),
                    'ethereal_assassin': (1, 2)
                },
                terrain_types=[
                    TerrainType.DIMENSIONAL,
                    TerrainType.HAZARDOUS,
                    TerrainType.DYNAMIC,
                    TerrainType.OPEN
                ],
                dimensional_properties={
                    DimensionalLayer.VOID: 1.0,
                    DimensionalLayer.PHYSICAL: 0.2,
                    DimensionalLayer.ETHEREAL: 0.6,
                    DimensionalLayer.CELESTIAL: 0.1
                },
                phase_progression=[
                    EncounterPhase.INTRODUCTION,
                    EncounterPhase.ESCALATION,
                    EncounterPhase.CLIMAX,
                    EncounterPhase.RESOLUTION
                ],
                difficulty_rating=3.5,
                rewards={
                    'experience': 5000,
                    'void_essence': 150,
                    'rare_item_chance': 0.8,
                    'unique_item_chance': 0.4,
                    'legendary_item_chance': 0.2
                },
                special_conditions={
                    'void_corruption': 1.0,
                    'reality_collapse': True,
                    'dimensional_instability': 1.0,
                    'environmental_hazards': True
                }
            )
        ]
        
        for template in templates:
            self.encounter_templates[template.name] = template

    def _initialize_difficulty_curve(self) -> None:
        """Initialize the difficulty progression curve"""
        base_difficulty = 1.0
        scaling_factor = 0.1
        
        for level in range(1, 51):  # Up to level 50
            # Exponential difficulty scaling with diminishing returns
            difficulty = base_difficulty * (1 + scaling_factor * math.log(level + 1))
            self.difficulty_curve[level] = difficulty

    def generate_encounter(self,
                         player_level: int,
                         desired_difficulty: float,
                         dimensional_stability: float) -> Dict[str, Any]:
        """Generate a complete combat encounter"""
        # Select appropriate encounter template
        template = self._select_encounter_template(
            player_level, desired_difficulty, dimensional_stability
        )
        
        if not template:
            return None
            
        # Generate enemy composition
        enemies = self._generate_enemy_composition(
            template, player_level, desired_difficulty
        )
        
        # Select and configure terrain
        terrain = self._configure_terrain(template, dimensional_stability)
        
        # Generate spawn points
        spawn_points = self._generate_spawn_points(
            terrain, len(enemies), template.dimensional_properties
        )
        
        # Configure phase progression
        phases = self._configure_phases(template, enemies, terrain)
        
        # Calculate rewards
        rewards = self._calculate_rewards(
            template, player_level, desired_difficulty
        )
        
        # Record this encounter
        self.last_encounter = template.name
        
        return {
            'template_name': template.name,
            'encounter_type': template.encounter_type,
            'enemies': enemies,
            'terrain': terrain,
            'spawn_points': spawn_points,
            'phases': phases,
            'rewards': rewards,
            'dimensional_properties': template.dimensional_properties,
            'special_conditions': template.special_conditions
        }

    def _select_encounter_template(self,
                                player_level: int,
                                desired_difficulty: float,
                                dimensional_stability: float) -> Optional[EncounterTemplate]:
        """Select an appropriate encounter template"""
        valid_templates = []
        
        for template in self.encounter_templates.values():
            # Check level range
            if not (template.level_range[0] <= player_level <= template.level_range[1]):
                continue
                
            # Check difficulty rating
            if abs(template.difficulty_rating - desired_difficulty) > 0.5:
                continue
                
            # Check dimensional stability requirements
            avg_dim_requirement = sum(template.dimensional_properties.values()) / \
                                len(template.dimensional_properties)
            if abs(avg_dim_requirement - dimensional_stability) > 0.3:
                continue
                
            # Avoid repeating the last encounter
            if template.name == self.last_encounter:
                continue
                
            valid_templates.append(template)
            
        if not valid_templates:
            return None
            
        # Weight templates by how well they match the desired parameters
        weighted_templates = [
            (template, self._calculate_template_weight(
                template, player_level, desired_difficulty, dimensional_stability
            ))
            for template in valid_templates
        ]
        
        # Select template based on weights
        total_weight = sum(weight for _, weight in weighted_templates)
        if total_weight <= 0:
            return random.choice(valid_templates)
            
        selection = random.uniform(0, total_weight)
        current_weight = 0
        
        for template, weight in weighted_templates:
            current_weight += weight
            if current_weight >= selection:
                return template
                
        return valid_templates[0]

    def _calculate_template_weight(self,
                                template: EncounterTemplate,
                                player_level: int,
                                desired_difficulty: float,
                                dimensional_stability: float) -> float:
        """Calculate selection weight for a template"""
        # Base weight
        weight = 1.0
        
        # Level appropriateness
        level_mid = (template.level_range[0] + template.level_range[1]) / 2
        level_diff = abs(player_level - level_mid)
        weight *= 1 / (1 + level_diff * 0.1)
        
        # Difficulty match
        diff_match = abs(template.difficulty_rating - desired_difficulty)
        weight *= 1 / (1 + diff_match)
        
        # Dimensional stability match
        avg_dim_requirement = sum(template.dimensional_properties.values()) / \
                            len(template.dimensional_properties)
        dim_match = abs(avg_dim_requirement - dimensional_stability)
        weight *= 1 / (1 + dim_match)
        
        return weight

    def _generate_enemy_composition(self,
                                 template: EncounterTemplate,
                                 player_level: int,
                                 desired_difficulty: float) -> List[Dict[str, Any]]:
        """Generate the enemy composition for an encounter"""
        enemies = []
        
        for enemy_name, (min_count, max_count) in template.enemy_composition.items():
            if enemy_name not in self.enemy_templates:
                continue
                
            enemy_template = self.enemy_templates[enemy_name]
            
            # Determine count based on difficulty
            count_range = max_count - min_count
            difficulty_factor = desired_difficulty / template.difficulty_rating
            target_count = min_count + int(count_range * difficulty_factor)
            actual_count = random.randint(min_count, min(max_count, target_count))
            
            # Generate each enemy instance
            for _ in range(actual_count):
                enemy = self._generate_enemy_instance(
                    enemy_template, player_level, desired_difficulty
                )
                enemies.append(enemy)
                
        return enemies

    def _generate_enemy_instance(self,
                              template: EnemyTemplate,
                              player_level: int,
                              desired_difficulty: float) -> Dict[str, Any]:
        """Generate a single enemy instance"""
        # Calculate level
        level_range = template.level_range[1] - template.level_range[0]
        level_factor = (player_level - template.level_range[0]) / max(1, level_range)
        enemy_level = template.level_range[0] + int(level_range * level_factor)
        
        # Scale stats based on level and difficulty
        level_multiplier = self.difficulty_curve[enemy_level]
        difficulty_multiplier = desired_difficulty / template.difficulty_rating
        
        scaled_stats = {}
        for stat, base_value in template.base_stats.items():
            scaled_stats[stat] = base_value * level_multiplier * difficulty_multiplier
            
        # Select behaviors and roles
        behaviors = random.sample(
            template.behavior_types,
            k=min(2, len(template.behavior_types))
        )
        roles = random.sample(
            template.tactical_roles,
            k=min(2, len(template.tactical_roles))
        )
        
        # Select abilities
        num_abilities = 2 + int(level_factor * 2)
        abilities = random.sample(
            template.abilities,
            k=min(num_abilities, len(template.abilities))
        )
        
        return {
            'template_name': template.name,
            'level': enemy_level,
            'stats': scaled_stats,
            'behaviors': behaviors,
            'roles': roles,
            'abilities': abilities,
            'dimensional_affinities': template.dimensional_affinities.copy()
        }

    def _configure_terrain(self,
                         template: EncounterTemplate,
                         dimensional_stability: float) -> Dict[str, Any]:
        """Configure the combat terrain"""
        terrain_config = {
            'types': template.terrain_types.copy(),
            'dimensions': template.dimensional_properties.copy(),
            'features': [],
            'hazards': [],
            'spawn_zones': []
        }
        
        # Add terrain features based on types
        for terrain_type in template.terrain_types:
            features = self._generate_terrain_features(
                terrain_type, dimensional_stability
            )
            terrain_config['features'].extend(features)
            
        # Add hazards if appropriate
        if TerrainType.HAZARDOUS in template.terrain_types:
            hazards = self._generate_terrain_hazards(
                template.dimensional_properties
            )
            terrain_config['hazards'].extend(hazards)
            
        # Configure spawn zones
        spawn_zones = self._generate_spawn_zones(
            template.terrain_types,
            template.dimensional_properties
        )
        terrain_config['spawn_zones'].extend(spawn_zones)
        
        return terrain_config

    def _generate_terrain_features(self,
                                terrain_type: TerrainType,
                                dimensional_stability: float) -> List[Dict[str, Any]]:
        """Generate appropriate terrain features"""
        features = []
        
        if terrain_type == TerrainType.OPEN:
            features.extend([
                {'type': 'clearing', 'size': random.uniform(10, 20)},
                {'type': 'cover', 'count': random.randint(3, 6)},
                {'type': 'vantage_point', 'height': random.uniform(3, 6)},
                {'type': 'terrain_depression', 'depth': random.uniform(2, 4)},
                {'type': 'scattered_obstacles', 'density': random.uniform(0.2, 0.5)}
            ])
        elif terrain_type == TerrainType.CONFINED:
            features.extend([
                {'type': 'corridor', 'width': random.uniform(2, 4)},
                {'type': 'chamber', 'size': random.uniform(5, 10)},
                {'type': 'chokepoint', 'width': random.uniform(1, 2)},
                {'type': 'alcove', 'depth': random.uniform(2, 4)},
                {'type': 'low_ceiling', 'height': random.uniform(2, 3)}
            ])
        elif terrain_type == TerrainType.ELEVATED:
            features.extend([
                {'type': 'platform', 'height': random.uniform(2, 5)},
                {'type': 'ramp', 'slope': random.uniform(0.3, 0.6)},
                {'type': 'floating_island', 'height': random.uniform(4, 8)},
                {'type': 'bridge', 'length': random.uniform(5, 10)},
                {'type': 'vertical_shaft', 'depth': random.uniform(5, 10)}
            ])
        elif terrain_type == TerrainType.DIMENSIONAL:
            instability = 1 - dimensional_stability
            features.extend([
                {'type': 'reality_tear', 'size': random.uniform(2, 5) * instability},
                {'type': 'void_zone', 'radius': random.uniform(3, 8) * instability},
                {'type': 'dimensional_rift', 'instability': instability},
                {'type': 'reality_anchor', 'stability_radius': random.uniform(4, 8)},
                {'type': 'phase_shift_zone', 'frequency': random.uniform(0.2, 0.8) * instability}
            ])
        elif terrain_type == TerrainType.DYNAMIC:
            features.extend([
                {'type': 'shifting_ground', 'frequency': random.uniform(0.2, 0.5)},
                {'type': 'collapsing_structure', 'trigger_chance': random.uniform(0.1, 0.3)},
                {'type': 'energy_vortex', 'pull_strength': random.uniform(0.5, 1.5)},
                {'type': 'phase_barrier', 'duration': random.uniform(10, 30)},
                {'type': 'terrain_transmutation', 'cycle_time': random.uniform(15, 45)}
            ])
            
        return features

    def _generate_terrain_hazards(self,
                               dimensional_properties: Dict[DimensionalLayer, float]) -> List[Dict[str, Any]]:
        """Generate terrain hazards"""
        hazards = []
        
        # Basic environmental hazards
        hazards.extend([
            {'type': 'void_pool', 'radius': random.uniform(2, 4), 'damage_per_second': 20},
            {'type': 'unstable_ground', 'area': random.uniform(4, 8), 'collapse_chance': 0.3},
            {'type': 'energy_storm', 'radius': random.uniform(5, 10), 'damage': 15, 'frequency': 2.0},
            {'type': 'gravity_well', 'radius': random.uniform(3, 6), 'pull_force': 5.0},
            {'type': 'corruption_field', 'radius': random.uniform(4, 8), 'corruption_rate': 0.1}
        ])
        
        # Dimensional hazards based on layer properties
        for dimension, intensity in dimensional_properties.items():
            if intensity > 0.5:
                if dimension == DimensionalLayer.VOID:
                    hazards.extend([
                        {
                            'type': 'void_eruption',
                            'radius': random.uniform(3, 6),
                            'damage': 30 * intensity,
                            'frequency': 5.0
                        },
                        {
                            'type': 'entropy_field',
                            'radius': random.uniform(4, 8),
                            'decay_rate': 0.2 * intensity
                        }
                    ])
                elif dimension == DimensionalLayer.ETHEREAL:
                    hazards.extend([
                        {
                            'type': 'phase_disruption',
                            'radius': random.uniform(3, 5),
                            'displacement': 5.0 * intensity
                        },
                        {
                            'type': 'reality_static',
                            'radius': random.uniform(4, 7),
                            'interference': 0.3 * intensity
                        }
                    ])
                elif dimension == DimensionalLayer.CELESTIAL:
                    hazards.extend([
                        {
                            'type': 'star_flare',
                            'radius': random.uniform(4, 8),
                            'damage': 25 * intensity,
                            'blind_duration': 2.0
                        },
                        {
                            'type': 'gravity_anomaly',
                            'radius': random.uniform(3, 6),
                            'force_multiplier': 2.0 * intensity
                        }
                    ])
                elif dimension == DimensionalLayer.PRIMORDIAL:
                    hazards.extend([
                        {
                            'type': 'reality_quake',
                            'radius': random.uniform(5, 10),
                            'damage': 20 * intensity,
                            'knockback': 4.0
                        },
                        {
                            'type': 'primordial_surge',
                            'radius': random.uniform(3, 7),
                            'mutation_chance': 0.2 * intensity
                        }
                    ])
                    
        # Dynamic hazard combinations
        if len(dimensional_properties) >= 2:
            dimensions = list(dimensional_properties.keys())
            for i in range(len(dimensions) - 1):
                for j in range(i + 1, len(dimensions)):
                    dim1, dim2 = dimensions[i], dimensions[j]
                    intensity1, intensity2 = dimensional_properties[dim1], dimensional_properties[dim2]
                    combined_intensity = (intensity1 + intensity2) / 2
                    
                    if combined_intensity > 0.6:
                        hazards.append({
                            'type': 'dimensional_confluence',
                            'dimensions': [dim1, dim2],
                            'radius': random.uniform(4, 8),
                            'intensity': combined_intensity,
                            'effects': [
                                {'type': 'reality_distortion', 'magnitude': combined_intensity * 2},
                                {'type': 'energy_discharge', 'damage': 15 * combined_intensity}
                            ]
                        })
                
        return hazards

    def _generate_spawn_zones(self,
                           terrain_types: List[TerrainType],
                           dimensional_properties: Dict[DimensionalLayer, float]) -> List[Dict[str, Any]]:
        """Generate enemy spawn zones"""
        spawn_zones = []
        
        # Basic spawn zones
        num_zones = len(terrain_types) + 2
        
        for _ in range(num_zones):
            zone = {
                'position': Position(
                    x=random.uniform(-20, 20),
                    y=random.uniform(-20, 20),
                    z=random.uniform(0, 5)
                ),
                'radius': random.uniform(2, 4),
                'terrain_type': random.choice(terrain_types),
                'dimensional_stability': sum(dimensional_properties.values()) / len(dimensional_properties)
            }
            spawn_zones.append(zone)
            
        return spawn_zones

    def _configure_phases(self,
                        template: EncounterTemplate,
                        enemies: List[Dict[str, Any]],
                        terrain: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Configure the phase progression of the encounter"""
        phases = []
        
        for phase_type in template.phase_progression:
            phase_config = self._generate_phase_configuration(
                phase_type, template, enemies, terrain
            )
            phases.append(phase_config)
            
        return phases

    def _generate_phase_configuration(self,
                                   phase_type: EncounterPhase,
                                   template: EncounterTemplate,
                                   enemies: List[Dict[str, Any]],
                                   terrain: Dict[str, Any]) -> Dict[str, Any]:
        """Generate configuration for a specific encounter phase"""
        if phase_type == EncounterPhase.INTRODUCTION:
            return {
                'type': phase_type,
                'duration': random.uniform(15, 30),
                'enemy_groups': self._split_enemies(enemies, 0.3),
                'terrain_modifications': [],
                'dimensional_effects': []
            }
        elif phase_type == EncounterPhase.ESCALATION:
            return {
                'type': phase_type,
                'duration': random.uniform(30, 60),
                'enemy_groups': self._split_enemies(enemies, 0.5),
                'terrain_modifications': [
                    {'type': 'intensity_increase', 'factor': 1.2}
                ],
                'dimensional_effects': [
                    {'type': 'stability_decrease', 'factor': 0.8}
                ]
            }
        elif phase_type == EncounterPhase.CLIMAX:
            return {
                'type': phase_type,
                'duration': random.uniform(45, 90),
                'enemy_groups': self._split_enemies(enemies, 0.8),
                'terrain_modifications': [
                    {'type': 'intensity_increase', 'factor': 1.5},
                    {'type': 'hazard_activation', 'count': 2}
                ],
                'dimensional_effects': [
                    {'type': 'stability_decrease', 'factor': 0.6},
                    {'type': 'void_surge', 'intensity': 0.7}
                ]
            }
        else:  # RESOLUTION
            return {
                'type': phase_type,
                'duration': random.uniform(20, 40),
                'enemy_groups': self._split_enemies(enemies, 1.0),
                'terrain_modifications': [
                    {'type': 'intensity_decrease', 'factor': 0.8}
                ],
                'dimensional_effects': [
                    {'type': 'stability_increase', 'factor': 1.2}
                ]
            }

    def _split_enemies(self,
                     enemies: List[Dict[str, Any]],
                     phase_progress: float) -> List[List[Dict[str, Any]]]:
        """Split enemies into groups for a phase"""
        available_enemies = enemies.copy()
        random.shuffle(available_enemies)
        
        num_enemies = int(len(enemies) * phase_progress)
        phase_enemies = available_enemies[:num_enemies]
        
        # Group enemies by role
        role_groups = {}
        for enemy in phase_enemies:
            main_role = enemy['roles'][0]
            if main_role not in role_groups:
                role_groups[main_role] = []
            role_groups[main_role].append(enemy)
            
        # Create balanced groups
        groups = []
        while role_groups:
            group = []
            roles = list(role_groups.keys())
            
            # Try to create balanced group
            for role in roles:
                if role_groups[role]:
                    group.append(role_groups[role].pop(0))
                    if not role_groups[role]:
                        del role_groups[role]
                        
            if group:
                groups.append(group)
                
        return groups

    def _calculate_rewards(self,
                        template: EncounterTemplate,
                        player_level: int,
                        difficulty: float) -> Dict[str, Any]:
        """Calculate encounter rewards"""
        base_rewards = template.rewards.copy()
        
        # Scale rewards based on level and difficulty
        level_factor = player_level / template.level_range[1]
        difficulty_factor = difficulty / template.difficulty_rating
        
        for key, value in base_rewards.items():
            if isinstance(value, (int, float)):
                base_rewards[key] = value * level_factor * difficulty_factor
                
        # Add bonus rewards based on special conditions
        if template.special_conditions.get('void_presence', False):
            base_rewards['void_essence'] = 50 * difficulty_factor
            
        if template.special_conditions.get('reality_storm', False):
            base_rewards['reality_shard'] = 25 * difficulty_factor
            
        return base_rewards 