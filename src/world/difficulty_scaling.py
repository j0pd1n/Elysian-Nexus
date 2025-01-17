from dataclasses import dataclass
from typing import Dict, List, Set, Optional
from enum import Enum, auto
import math
from src.combat_system.dimensional_combat import DimensionalLayer, Position, DimensionalEffect
from src.world.world_generator import Region, Landmark, LandmarkType
from src.world.terrain_generator import TerrainType, TerrainCell

class ProgressionFactor(Enum):
    DIMENSIONAL_MASTERY = auto()
    COMBAT_PROFICIENCY = auto()
    STABILITY_CONTROL = auto()
    ARTIFACT_COLLECTION = auto()
    QUEST_COMPLETION = auto()

@dataclass
class PlayerProgression:
    """Tracks player's progression metrics"""
    dimensional_mastery: Dict[DimensionalLayer, float]  # 0.0 to 1.0
    combat_proficiency: float  # 0.0 to 1.0
    stability_control: float  # 0.0 to 1.0
    artifact_collection: float  # 0.0 to 1.0
    quest_completion: float  # 0.0 to 1.0
    
    @property
    def overall_progression(self) -> float:
        """Calculate overall progression level"""
        return (
            sum(self.dimensional_mastery.values()) / len(DimensionalLayer) +
            self.combat_proficiency +
            self.stability_control +
            self.artifact_collection +
            self.quest_completion
        ) / 5.0

class DifficultyScaling:
    """Manages dynamic difficulty scaling across dimensions"""
    
    def __init__(self):
        self.dimension_base_difficulty = {
            DimensionalLayer.PHYSICAL: 0.2,
            DimensionalLayer.ETHEREAL: 0.4,
            DimensionalLayer.CELESTIAL: 0.6,
            DimensionalLayer.VOID: 0.8,
            DimensionalLayer.PRIMORDIAL: 1.0
        }
        
        self.terrain_difficulty_modifiers = {
            # Physical
            TerrainType.PLAINS: 0.0,
            TerrainType.MOUNTAINS: 0.3,
            TerrainType.FOREST: 0.1,
            TerrainType.WATER: 0.2,
            
            # Ethereal
            TerrainType.MIST_FIELDS: 0.1,
            TerrainType.CRYSTAL_FORMATIONS: 0.2,
            TerrainType.SPIRIT_GROVES: 0.1,
            TerrainType.VOID_POOLS: 0.4,
            
            # Celestial
            TerrainType.STARDUST_FIELDS: 0.2,
            TerrainType.ASTRAL_PEAKS: 0.4,
            TerrainType.CONSTELLATION_FORESTS: 0.2,
            TerrainType.NEBULA_SEAS: 0.5,
            
            # Void
            TerrainType.SHADOW_WASTES: 0.3,
            TerrainType.CHAOS_SPIRES: 0.6,
            TerrainType.ENTROPY_FIELDS: 0.4,
            TerrainType.DARK_MATTER_POOLS: 0.7,
            
            # Primordial
            TerrainType.REALITY_FRACTURES: 0.5,
            TerrainType.ESSENCE_CRYSTALS: 0.4,
            TerrainType.PRIMAL_STORMS: 0.8,
            TerrainType.TIME_DISTORTIONS: 0.6
        }
        
        self.effect_difficulty_modifiers = {
            DimensionalEffect.WARPING: 0.3,
            DimensionalEffect.RESONANCE: 0.2,
            DimensionalEffect.DISTORTION: 0.4,
            DimensionalEffect.STABILIZING: -0.2,
            DimensionalEffect.ANCHORING: -0.1
        }
    
    def calculate_region_difficulty(
        self,
        region: Region,
        player_progression: PlayerProgression,
        safe_zones: List[Position]
    ) -> float:
        """Calculate difficulty rating for a region"""
        # Start with base difficulty for dimension
        difficulty = self.dimension_base_difficulty[
            DimensionalLayer(region.center.dimensional_layer)
        ]
        
        # Adjust for distance from safe zones
        min_distance = float('inf')
        for safe_zone in safe_zones:
            if safe_zone.dimensional_layer == region.center.dimensional_layer:
                distance = math.sqrt(
                    (region.center.x - safe_zone.x)**2 +
                    (region.center.y - safe_zone.y)**2
                )
                min_distance = min(min_distance, distance)
        
        if min_distance != float('inf'):
            # Scale distance factor from 0.0 to 0.3
            distance_factor = min(0.3, min_distance / 1000.0)
            difficulty += distance_factor
        
        # Adjust for player progression
        progression_scaling = self._calculate_progression_scaling(
            player_progression,
            DimensionalLayer(region.center.dimensional_layer)
        )
        difficulty *= progression_scaling
        
        # Adjust for ambient effects
        for effect in region.ambient_effects:
            if effect in self.effect_difficulty_modifiers:
                difficulty += self.effect_difficulty_modifiers[effect]
        
        return max(0.1, min(1.0, difficulty))
    
    def calculate_combat_difficulty(
        self,
        position: Position,
        terrain_cell: TerrainCell,
        active_effects: Set[DimensionalEffect],
        player_progression: PlayerProgression
    ) -> float:
        """Calculate difficulty rating for combat at a specific position"""
        # Start with base difficulty for dimension
        difficulty = self.dimension_base_difficulty[
            DimensionalLayer(position.dimensional_layer)
        ]
        
        # Add terrain difficulty
        difficulty += self.terrain_difficulty_modifiers[terrain_cell.terrain_type]
        
        # Add effect difficulties
        for effect in active_effects:
            if effect in self.effect_difficulty_modifiers:
                difficulty += self.effect_difficulty_modifiers[effect]
        
        # Scale with player progression
        progression_scaling = self._calculate_progression_scaling(
            player_progression,
            DimensionalLayer(position.dimensional_layer)
        )
        difficulty *= progression_scaling
        
        # Add terrain hazard level
        difficulty += terrain_cell.hazard_level * 0.3
        
        # Adjust for stability
        stability_factor = 0.2 * (1.0 - terrain_cell.stability_modifier)
        difficulty += stability_factor
        
        return max(0.1, min(1.0, difficulty))
    
    def _calculate_progression_scaling(
        self,
        player_progression: PlayerProgression,
        dimension: DimensionalLayer
    ) -> float:
        """Calculate difficulty scaling based on player progression"""
        # Base scaling from 0.8 to 1.2
        base_scale = 0.8 + player_progression.overall_progression * 0.4
        
        # Additional scaling based on dimensional mastery
        if dimension in player_progression.dimensional_mastery:
            mastery = player_progression.dimensional_mastery[dimension]
            # Scale from 0.9 to 1.1 based on mastery
            mastery_scale = 0.9 + mastery * 0.2
        else:
            mastery_scale = 1.0
        
        return base_scale * mastery_scale
    
    def recommend_encounter_level(
        self,
        base_difficulty: float,
        player_progression: PlayerProgression
    ) -> Dict[str, float]:
        """Recommend encounter parameters based on difficulty"""
        # Scale enemy stats based on difficulty and progression
        enemy_scaling = base_difficulty * (1.0 + player_progression.combat_proficiency * 0.3)
        
        return {
            'enemy_level_scaling': enemy_scaling,
            'enemy_count_scaling': base_difficulty * 1.2,
            'boss_probability': base_difficulty * 0.4,
            'elite_probability': base_difficulty * 0.6,
            'loot_quality_scaling': base_difficulty * (1.0 + player_progression.overall_progression * 0.5),
            'dimensional_effect_intensity': base_difficulty * (1.0 + player_progression.stability_control * 0.4)
        } 