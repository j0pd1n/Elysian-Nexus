import unittest
from src.combat_system.dimensional_combat import (
    DimensionalCombat,
    DimensionalLayer,
    DimensionalEffect,
    Position
)
from src.world.world_generator import (
    WorldGenerator,
    LandmarkType,
    Landmark,
    Region
)

class TestWorldGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.combat_system = DimensionalCombat()
        self.world_generator = WorldGenerator(self.combat_system)
        
    def test_world_generation(self):
        """Test complete world generation"""
        # Generate world with fixed seed for reproducibility
        self.world_generator.generate_world(seed=42)
        
        # Verify regions and landmarks were created for each dimension
        for layer in DimensionalLayer:
            # Check regions
            regions = self.world_generator.regions[layer]
            self.assertGreaterEqual(len(regions), 3)  # Minimum 3 regions
            self.assertLessEqual(len(regions), 6)     # Maximum 6 regions
            
            # Check landmarks
            landmarks = self.world_generator.landmarks[layer]
            self.assertGreaterEqual(len(landmarks), 1)  # At least nexus
            
            # Verify nexus
            nexus = landmarks[0]
            self.assertEqual(nexus.type, LandmarkType.NEXUS)
            self.assertEqual(nexus.position.dimensional_layer, layer.value)
            
    def test_region_generation(self):
        """Test region generation and properties"""
        self.world_generator._generate_regions()
        
        for layer in DimensionalLayer:
            for region in self.world_generator.regions[layer]:
                # Check region properties
                self.assertGreaterEqual(region.radius, self.world_generator.min_region_radius)
                self.assertLessEqual(region.radius, self.world_generator.max_region_radius)
                self.assertGreaterEqual(region.base_stability, 0.0)
                self.assertLessEqual(region.base_stability, 1.0)
                self.assertGreaterEqual(region.difficulty_rating, 0.0)
                self.assertLessEqual(region.difficulty_rating, 1.0)
                
                # Check region position
                distance_from_center = (
                    region.center.x ** 2 +
                    region.center.y ** 2 +
                    region.center.z ** 2
                ) ** 0.5
                self.assertGreaterEqual(distance_from_center, 30.0)
                self.assertLessEqual(distance_from_center, 50.0)
                
    def test_landmark_generation(self):
        """Test landmark generation and properties"""
        # Generate regions first
        self.world_generator._generate_regions()
        self.world_generator._generate_landmarks()
        
        for layer in DimensionalLayer:
            for region in self.world_generator.regions[layer]:
                # Check number of landmarks
                self.assertGreaterEqual(len(region.landmarks), 2)
                self.assertLessEqual(len(region.landmarks), 4)
                
                for landmark in region.landmarks:
                    # Check landmark properties
                    self.assertIsInstance(landmark.type, LandmarkType)
                    self.assertGreaterEqual(landmark.influence_radius, 5.0)
                    self.assertLessEqual(landmark.influence_radius, 15.0)
                    self.assertGreaterEqual(landmark.difficulty_rating, 0.0)
                    self.assertLessEqual(landmark.difficulty_rating, 1.0)
                    
                    # Check landmark position within region
                    dx = landmark.position.x - region.center.x
                    dy = landmark.position.y - region.center.y
                    dz = landmark.position.z - region.center.z
                    distance = (dx*dx + dy*dy + dz*dz) ** 0.5
                    self.assertLessEqual(distance, region.radius)
                    
    def test_landmark_connections(self):
        """Test landmark connection generation"""
        self.world_generator.generate_world(seed=42)
        
        for layer in DimensionalLayer:
            landmarks = self.world_generator.landmarks[layer]
            
            # Check that each landmark has connections
            for landmark in landmarks:
                self.assertGreater(len(landmark.connected_landmarks), 0)
                
            # Verify graph connectivity
            visited = set()
            stack = [landmarks[0]]
            
            while stack:
                current = stack.pop()
                visited.add(current)
                for neighbor in current.connected_landmarks:
                    if neighbor not in visited:
                        stack.append(neighbor)
                        
            # All landmarks should be reachable
            self.assertEqual(len(visited), len(landmarks))
            
    def test_dimensional_effects(self):
        """Test application of dimensional effects"""
        self.world_generator.generate_world(seed=42)
        
        for layer in DimensionalLayer:
            state = self.combat_system.dimensional_states[layer]
            
            # Check that effects were applied
            self.assertGreater(len(state.active_effects), 0)
            
            # Verify stability is within bounds
            self.assertGreaterEqual(state.stability, 0.0)
            self.assertLessEqual(state.stability, 1.0)
            
    def test_difficulty_scaling(self):
        """Test difficulty scaling with distance and dimension"""
        self.world_generator.generate_world(seed=42)
        
        # Test difficulty increases with dimension
        difficulties = []
        for layer in DimensionalLayer:
            layer_difficulties = [
                region.difficulty_rating
                for region in self.world_generator.regions[layer]
            ]
            difficulties.append(sum(layer_difficulties) / len(layer_difficulties))
            
        # Verify increasing difficulty
        for i in range(1, len(difficulties)):
            self.assertGreater(difficulties[i], difficulties[i-1])
            
        # Test difficulty increases with distance
        for layer in DimensionalLayer:
            regions = self.world_generator.regions[layer]
            for region in regions:
                distance = (
                    region.center.x ** 2 +
                    region.center.y ** 2 +
                    region.center.z ** 2
                ) ** 0.5
                
                # Calculate expected difficulty
                base_difficulty = {
                    DimensionalLayer.PHYSICAL: 0.2,
                    DimensionalLayer.ETHEREAL: 0.4,
                    DimensionalLayer.CELESTIAL: 0.6,
                    DimensionalLayer.VOID: 0.8,
                    DimensionalLayer.PRIMORDIAL: 1.0
                }[layer]
                
                expected_difficulty = min(1.0, base_difficulty + distance / 100.0)
                self.assertAlmostEqual(
                    region.difficulty_rating,
                    expected_difficulty,
                    places=2
                )
                
    def test_landmark_type_distribution(self):
        """Test landmark type distribution based on difficulty"""
        self.world_generator.generate_world(seed=42)
        
        # Count landmark types in easy vs hard regions
        easy_types = []
        hard_types = []
        
        for layer in DimensionalLayer:
            for region in self.world_generator.regions[layer]:
                for landmark in region.landmarks:
                    if region.difficulty_rating < 0.5:
                        easy_types.append(landmark.type)
                    else:
                        hard_types.append(landmark.type)
                        
        # Check sanctuary distribution
        easy_sanctuaries = sum(1 for t in easy_types if t == LandmarkType.SANCTUARY)
        hard_sanctuaries = sum(1 for t in hard_types if t == LandmarkType.SANCTUARY)
        
        if easy_types and hard_types:  # Only check if we have both easy and hard regions
            sanctuary_ratio = easy_sanctuaries / len(easy_types)
            hard_sanctuary_ratio = hard_sanctuaries / len(hard_types)
            self.assertGreater(sanctuary_ratio, hard_sanctuary_ratio)
            
        # Check void rift distribution
        easy_rifts = sum(1 for t in easy_types if t == LandmarkType.VOID_RIFT)
        hard_rifts = sum(1 for t in hard_types if t == LandmarkType.VOID_RIFT)
        
        if easy_types and hard_types:
            rift_ratio = easy_rifts / len(easy_types)
            hard_rift_ratio = hard_rifts / len(hard_types)
            self.assertLess(rift_ratio, hard_rift_ratio)

if __name__ == '__main__':
    unittest.main() 