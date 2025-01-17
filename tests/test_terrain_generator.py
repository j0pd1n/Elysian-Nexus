import unittest
import math
from src.combat_system.dimensional_combat import (
    DimensionalCombat,
    DimensionalLayer,
    DimensionalEffect,
    Position
)
from src.world.world_generator import (
    Region,
    Landmark,
    LandmarkType
)
from src.world.terrain_generator import (
    TerrainGenerator,
    TerrainType,
    TerrainCell
)

class TestTerrainGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.generator = TerrainGenerator(cell_size=1.0)
        
    def test_terrain_generation(self):
        """Test basic terrain generation"""
        # Create test region
        region = Region(
            center=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=10.0,
            base_stability=0.8,
            ambient_effects={DimensionalEffect.RESONANCE},
            landmarks=[],
            difficulty_rating=0.5,
            terrain_seed=42
        )
        
        # Generate terrain
        terrain = self.generator.generate_terrain(region, [])
        
        # Verify terrain properties
        self.assertGreater(len(terrain), 0)
        for (x, y), cell in terrain.items():
            # Check position bounds
            self.assertLessEqual(
                math.sqrt(cell.position.x**2 + cell.position.y**2),
                region.radius
            )
            
            # Check height bounds
            self.assertGreaterEqual(cell.height, 0.0)
            self.assertLessEqual(cell.height, 1.0)
            
            # Check terrain type is appropriate for dimension
            self.assertIn(
                cell.terrain_type,
                [t for t, _ in self.generator.terrain_thresholds[DimensionalLayer.PHYSICAL]]
            )
            
    def test_terrain_types_by_dimension(self):
        """Test terrain type generation for each dimension"""
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
            
            terrain = self.generator.generate_terrain(region, [])
            
            # Get unique terrain types
            terrain_types = {cell.terrain_type for cell in terrain.values()}
            
            # Verify appropriate types for dimension
            expected_types = {t for t, _ in self.generator.terrain_thresholds[layer]}
            self.assertEqual(terrain_types, expected_types)
            
    def test_landmark_influence(self):
        """Test landmark influence on terrain"""
        region = Region(
            center=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=20.0,
            base_stability=0.8,
            ambient_effects=set(),
            landmarks=[],
            difficulty_rating=0.5,
            terrain_seed=42
        )
        
        # Create landmark
        landmark = Landmark(
            type=LandmarkType.VOID_RIFT,
            position=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            influence_radius=5.0,
            stability_modifier=-0.4,
            effects={DimensionalEffect.WARPING},
            difficulty_rating=0.7
        )
        
        # Generate terrain with and without landmark
        terrain_without = self.generator.generate_terrain(region, [])
        terrain_with = self.generator.generate_terrain(region, [landmark])
        
        # Compare cells near landmark
        for (x, y), cell in terrain_with.items():
            if (x, y) in terrain_without:
                distance = math.sqrt(x*x + y*y)
                if distance <= landmark.influence_radius:
                    # Check height modification
                    self.assertNotEqual(
                        cell.height,
                        terrain_without[(x, y)].height
                    )
                    # Check hazard level increase
                    self.assertGreater(
                        cell.hazard_level,
                        terrain_without[(x, y)].hazard_level
                    )
                    
    def test_terrain_traversability(self):
        """Test terrain traversability"""
        region = Region(
            center=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=10.0,
            base_stability=0.8,
            ambient_effects=set(),
            landmarks=[],
            difficulty_rating=0.5,
            terrain_seed=42
        )
        
        terrain = self.generator.generate_terrain(region, [])
        
        for cell in terrain.values():
            if cell.terrain_type in {
                TerrainType.WATER,
                TerrainType.VOID_POOLS,
                TerrainType.NEBULA_SEAS,
                TerrainType.DARK_MATTER_POOLS,
                TerrainType.TIME_DISTORTIONS,
                TerrainType.PRIMAL_STORMS
            }:
                self.assertFalse(cell.traversable)
            else:
                self.assertTrue(cell.traversable)
                
    def test_terrain_hazard_scaling(self):
        """Test hazard level scaling with difficulty"""
        # Create regions with different difficulties
        easy_region = Region(
            center=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=10.0,
            base_stability=0.8,
            ambient_effects=set(),
            landmarks=[],
            difficulty_rating=0.2,
            terrain_seed=42
        )
        
        hard_region = Region(
            center=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=10.0,
            base_stability=0.8,
            ambient_effects=set(),
            landmarks=[],
            difficulty_rating=0.8,
            terrain_seed=42
        )
        
        easy_terrain = self.generator.generate_terrain(easy_region, [])
        hard_terrain = self.generator.generate_terrain(hard_region, [])
        
        # Compare average hazard levels
        easy_hazard = sum(c.hazard_level for c in easy_terrain.values()) / len(easy_terrain)
        hard_hazard = sum(c.hazard_level for c in hard_terrain.values()) / len(hard_terrain)
        
        self.assertLess(easy_hazard, hard_hazard)
        
    def test_terrain_stability(self):
        """Test terrain stability calculations"""
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
            
            terrain = self.generator.generate_terrain(region, [])
            
            # Check stability bounds
            for cell in terrain.values():
                self.assertGreaterEqual(cell.stability_modifier, -1.0)
                self.assertLessEqual(cell.stability_modifier, 1.0)
                
            # Calculate average stability
            avg_stability = sum(
                c.stability_modifier for c in terrain.values()
            ) / len(terrain)
            
            # Verify stability decreases with dimension depth
            if layer != DimensionalLayer.PHYSICAL:
                prev_layer = DimensionalLayer(layer.value - 1)
                prev_region = Region(
                    center=Position(x=0, y=0, z=0, dimensional_layer=prev_layer.value),
                    radius=10.0,
                    base_stability=0.8,
                    ambient_effects=set(),
                    landmarks=[],
                    difficulty_rating=0.5,
                    terrain_seed=42
                )
                
                prev_terrain = self.generator.generate_terrain(prev_region, [])
                prev_avg_stability = sum(
                    c.stability_modifier for c in prev_terrain.values()
                ) / len(prev_terrain)
                
                self.assertLess(avg_stability, prev_avg_stability)
                
    def test_terrain_smoothing(self):
        """Test terrain height smoothing"""
        region = Region(
            center=Position(x=0, y=0, z=0, dimensional_layer=DimensionalLayer.PHYSICAL.value),
            radius=10.0,
            base_stability=0.8,
            ambient_effects=set(),
            landmarks=[],
            difficulty_rating=0.5,
            terrain_seed=42
        )
        
        terrain = self.generator.generate_terrain(region, [])
        
        # Check height differences between adjacent cells
        for (x, y), cell in terrain.items():
            neighbors = [
                terrain.get((x+dx, y+dy))
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
                if (x+dx, y+dy) in terrain
            ]
            
            if neighbors:
                height_diff = max(
                    abs(cell.height - n.height)
                    for n in neighbors
                )
                # Verify smooth transitions
                self.assertLess(height_diff, 0.3)

if __name__ == '__main__':
    unittest.main() 