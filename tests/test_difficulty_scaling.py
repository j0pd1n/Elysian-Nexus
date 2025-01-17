import unittest
from src.combat_system.dimensional_combat import (
    DimensionalLayer,
    Position,
    DimensionalEffect
)
from src.world.world_generator import Region
from src.world.terrain_generator import TerrainType, TerrainCell
from src.world.difficulty_scaling import (
    DifficultyScaling,
    PlayerProgression,
    ProgressionFactor
)

class TestDifficultyScaling(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.scaler = DifficultyScaling()
        self.player_progression = PlayerProgression(
            dimensional_mastery={
                DimensionalLayer.PHYSICAL: 0.8,
                DimensionalLayer.ETHEREAL: 0.6,
                DimensionalLayer.CELESTIAL: 0.4,
                DimensionalLayer.VOID: 0.2,
                DimensionalLayer.PRIMORDIAL: 0.1
            },
            combat_proficiency=0.7,
            stability_control=0.6,
            artifact_collection=0.5,
            quest_completion=0.4
        )
        
    def test_dimension_difficulty_scaling(self):
        """Test difficulty scaling across dimensions"""
        difficulties = []
        for layer in DimensionalLayer:
            region = Region(
                center=Position(x=0, y=0, z=0, dimensional_layer=layer.value),
                radius=10.0,
                base_stability=0.8,
                ambient_effects=set(),
                landmarks=[],
                difficulty_rating=0.5,
                terrain_seed=42
            )
            
            difficulty = self.scaler.calculate_region_difficulty(
                region,
                self.player_progression,
                []  # No safe zones
            )
            difficulties.append(difficulty)
            
        # Verify increasing difficulty
        for i in range(1, len(difficulties)):
            self.assertGreater(difficulties[i], difficulties[i-1])
            
    def test_safe_zone_distance_scaling(self):
        """Test difficulty scaling based on distance from safe zones"""
        region = Region(
            center=Position(x=100, y=100, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=10.0,
            base_stability=0.8,
            ambient_effects=set(),
            landmarks=[],
            difficulty_rating=0.5,
            terrain_seed=42
        )
        
        # Test with different safe zone distances
        safe_zones = [
            Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        ]
        
        difficulty_close = self.scaler.calculate_region_difficulty(
            region,
            self.player_progression,
            safe_zones
        )
        
        # Move region further away
        far_region = Region(
            center=Position(x=1000, y=1000, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=10.0,
            base_stability=0.8,
            ambient_effects=set(),
            landmarks=[],
            difficulty_rating=0.5,
            terrain_seed=42
        )
        
        difficulty_far = self.scaler.calculate_region_difficulty(
            far_region,
            self.player_progression,
            safe_zones
        )
        
        self.assertGreater(difficulty_far, difficulty_close)
        
    def test_progression_scaling(self):
        """Test difficulty scaling based on player progression"""
        region = Region(
            center=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=10.0,
            base_stability=0.8,
            ambient_effects=set(),
            landmarks=[],
            difficulty_rating=0.5,
            terrain_seed=42
        )
        
        # Test with different progression levels
        low_progression = PlayerProgression(
            dimensional_mastery={
                DimensionalLayer.PHYSICAL: 0.2,
                DimensionalLayer.ETHEREAL: 0.1
            },
            combat_proficiency=0.2,
            stability_control=0.2,
            artifact_collection=0.1,
            quest_completion=0.1
        )
        
        high_progression = PlayerProgression(
            dimensional_mastery={
                DimensionalLayer.PHYSICAL: 0.9,
                DimensionalLayer.ETHEREAL: 0.8
            },
            combat_proficiency=0.9,
            stability_control=0.8,
            artifact_collection=0.7,
            quest_completion=0.8
        )
        
        difficulty_low = self.scaler.calculate_region_difficulty(
            region,
            low_progression,
            []
        )
        
        difficulty_high = self.scaler.calculate_region_difficulty(
            region,
            high_progression,
            []
        )
        
        self.assertGreater(difficulty_high, difficulty_low)
        
    def test_combat_difficulty_calculation(self):
        """Test combat difficulty calculations"""
        position = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        
        # Test different terrain types
        easy_terrain = TerrainCell(
            position=position,
            height=0.5,
            terrain_type=TerrainType.PLAINS,
            traversable=True,
            hazard_level=0.1,
            stability_modifier=0.8
        )
        
        hard_terrain = TerrainCell(
            position=position,
            height=0.8,
            terrain_type=TerrainType.MOUNTAINS,
            traversable=True,
            hazard_level=0.7,
            stability_modifier=0.3
        )
        
        difficulty_easy = self.scaler.calculate_combat_difficulty(
            position,
            easy_terrain,
            set(),
            self.player_progression
        )
        
        difficulty_hard = self.scaler.calculate_combat_difficulty(
            position,
            hard_terrain,
            set(),
            self.player_progression
        )
        
        self.assertGreater(difficulty_hard, difficulty_easy)
        
    def test_dimensional_effects_scaling(self):
        """Test difficulty scaling with dimensional effects"""
        position = Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value)
        terrain_cell = TerrainCell(
            position=position,
            height=0.5,
            terrain_type=TerrainType.PLAINS,
            traversable=True,
            hazard_level=0.3,
            stability_modifier=0.6
        )
        
        # Test with different effects
        stabilizing_effects = {DimensionalEffect.STABILIZING}
        warping_effects = {DimensionalEffect.WARPING, DimensionalEffect.DISTORTION}
        
        difficulty_stable = self.scaler.calculate_combat_difficulty(
            position,
            terrain_cell,
            stabilizing_effects,
            self.player_progression
        )
        
        difficulty_warped = self.scaler.calculate_combat_difficulty(
            position,
            terrain_cell,
            warping_effects,
            self.player_progression
        )
        
        self.assertGreater(difficulty_warped, difficulty_stable)
        
    def test_encounter_recommendations(self):
        """Test encounter parameter recommendations"""
        base_difficulty = 0.5
        
        # Test with different progression levels
        low_progression = PlayerProgression(
            dimensional_mastery={DimensionalLayer.PHYSICAL: 0.2},
            combat_proficiency=0.2,
            stability_control=0.2,
            artifact_collection=0.1,
            quest_completion=0.1
        )
        
        high_progression = PlayerProgression(
            dimensional_mastery={DimensionalLayer.PHYSICAL: 0.9},
            combat_proficiency=0.9,
            stability_control=0.8,
            artifact_collection=0.7,
            quest_completion=0.8
        )
        
        low_recommendations = self.scaler.recommend_encounter_level(
            base_difficulty,
            low_progression
        )
        
        high_recommendations = self.scaler.recommend_encounter_level(
            base_difficulty,
            high_progression
        )
        
        # Verify scaling of various parameters
        self.assertGreater(
            high_recommendations['enemy_level_scaling'],
            low_recommendations['enemy_level_scaling']
        )
        self.assertGreater(
            high_recommendations['loot_quality_scaling'],
            low_recommendations['loot_quality_scaling']
        )
        self.assertGreater(
            high_recommendations['dimensional_effect_intensity'],
            low_recommendations['dimensional_effect_intensity']
        )
        
    def test_difficulty_bounds(self):
        """Test that difficulty values stay within bounds"""
        region = Region(
            center=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PRIMORDIAL.value),
            radius=10.0,
            base_stability=0.1,
            ambient_effects={
                DimensionalEffect.WARPING,
                DimensionalEffect.DISTORTION
            },
            landmarks=[],
            difficulty_rating=1.0,
            terrain_seed=42
        )
        
        # Test with maximum progression
        max_progression = PlayerProgression(
            dimensional_mastery={
                layer: 1.0 for layer in DimensionalLayer
            },
            combat_proficiency=1.0,
            stability_control=1.0,
            artifact_collection=1.0,
            quest_completion=1.0
        )
        
        difficulty = self.scaler.calculate_region_difficulty(
            region,
            max_progression,
            []
        )
        
        self.assertLessEqual(difficulty, 1.0)
        self.assertGreaterEqual(difficulty, 0.1)

if __name__ == '__main__':
    unittest.main() 