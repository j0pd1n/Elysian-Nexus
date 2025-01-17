from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum, auto
import random
import noise
import math
from src.combat_system.dimensional_combat import (
    DimensionalLayer,
    DimensionalEffect,
    Position,
    DimensionalCombat
)
from src.world.dimensional_pathfinding import DimensionalPathfinder

class LandmarkType(Enum):
    NEXUS = auto()          # Dimensional crossroads
    SANCTUARY = auto()      # Safe zones
    VOID_RIFT = auto()      # Dangerous tears in reality
    POWER_NODE = auto()     # Energy sources
    ANCIENT_RUIN = auto()   # Historical sites
    RESONANCE_WELL = auto() # Stability anchors
    DISTORTION_FIELD = auto() # Reality warping areas
    
@dataclass
class Landmark:
    """Represents a significant location in the world"""
    type: LandmarkType
    position: Position
    influence_radius: float
    stability_modifier: float
    effects: Set[DimensionalEffect]
    difficulty_rating: float
    connected_landmarks: Set['Landmark'] = None
    
    def __post_init__(self):
        if self.connected_landmarks is None:
            self.connected_landmarks = set()

@dataclass
class Region:
    """Represents a distinct area in a dimension"""
    center: Position
    radius: float
    base_stability: float
    ambient_effects: Set[DimensionalEffect]
    landmarks: List[Landmark]
    difficulty_rating: float
    terrain_seed: int

class WorldGenerator:
    """Generates the dimensional world structure"""
    
    def __init__(self, combat_system: DimensionalCombat):
        self.combat_system = combat_system
        self.pathfinder = DimensionalPathfinder(combat_system)
        self.regions: Dict[DimensionalLayer, List[Region]] = {}
        self.landmarks: Dict[DimensionalLayer, List[Landmark]] = {}
        self.noise_scale = 50.0
        self.min_region_radius = 10.0
        self.max_region_radius = 30.0
        
    def generate_world(self, seed: int = None):
        """Generate the complete world structure"""
        if seed is not None:
            random.seed(seed)
            
        # Initialize regions for each dimension
        for layer in DimensionalLayer:
            self.regions[layer] = []
            self.landmarks[layer] = []
            
        # Generate primary structures
        self._generate_dimensional_nexuses()
        self._generate_regions()
        self._generate_landmarks()
        self._connect_landmarks()
        self._apply_dimensional_effects()
        
    def _generate_dimensional_nexuses(self):
        """Generate major connection points between dimensions"""
        # Create central nexus in each dimension
        for layer in DimensionalLayer:
            nexus = Landmark(
                type=LandmarkType.NEXUS,
                position=Position(x=0, y=0, z=0, dimensional_layer=layer.value),
                influence_radius=20.0,
                stability_modifier=0.2,
                effects={DimensionalEffect.RESONANCE},
                difficulty_rating=0.5
            )
            self.landmarks[layer].append(nexus)
            
        # Connect nexuses between adjacent dimensions
        for i, layer in enumerate(DimensionalLayer):
            if i > 0:
                prev_nexus = self.landmarks[DimensionalLayer(i-1)][0]
                curr_nexus = self.landmarks[layer][0]
                prev_nexus.connected_landmarks.add(curr_nexus)
                curr_nexus.connected_landmarks.add(prev_nexus)
                
    def _generate_regions(self):
        """Generate distinct regions in each dimension"""
        for layer in DimensionalLayer:
            num_regions = random.randint(3, 6)
            
            for _ in range(num_regions):
                # Generate region center away from nexus
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(30.0, 50.0)
                x = math.cos(angle) * distance
                y = math.sin(angle) * distance
                
                region = Region(
                    center=Position(
                        x=x,
                        y=y,
                        z=0,
                        dimensional_layer=layer.value
                    ),
                    radius=random.uniform(
                        self.min_region_radius,
                        self.max_region_radius
                    ),
                    base_stability=self._calculate_base_stability(layer),
                    ambient_effects=self._generate_ambient_effects(layer),
                    landmarks=[],
                    difficulty_rating=self._calculate_region_difficulty(
                        layer,
                        distance
                    ),
                    terrain_seed=random.randint(0, 1000000)
                )
                
                self.regions[layer].append(region)
                
    def _generate_landmarks(self):
        """Generate landmarks within regions"""
        for layer in DimensionalLayer:
            for region in self.regions[layer]:
                num_landmarks = random.randint(2, 4)
                
                for _ in range(num_landmarks):
                    landmark_type = self._select_landmark_type(layer, region)
                    
                    # Generate position within region
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(0, region.radius * 0.8)
                    x = region.center.x + math.cos(angle) * distance
                    y = region.center.y + math.sin(angle) * distance
                    
                    landmark = Landmark(
                        type=landmark_type,
                        position=Position(
                            x=x,
                            y=y,
                            z=0,
                            dimensional_layer=layer.value
                        ),
                        influence_radius=random.uniform(5.0, 15.0),
                        stability_modifier=self._get_landmark_stability_modifier(
                            landmark_type
                        ),
                        effects=self._get_landmark_effects(landmark_type),
                        difficulty_rating=self._calculate_landmark_difficulty(
                            landmark_type,
                            region.difficulty_rating
                        )
                    )
                    
                    region.landmarks.append(landmark)
                    self.landmarks[layer].append(landmark)
                    
    def _connect_landmarks(self):
        """Create connections between landmarks"""
        for layer in DimensionalLayer:
            landmarks = self.landmarks[layer]
            
            # Connect each landmark to its nearest neighbors
            for landmark in landmarks:
                nearest = self._find_nearest_landmarks(landmark, 2)
                for near in nearest:
                    if self._can_connect_landmarks(landmark, near):
                        landmark.connected_landmarks.add(near)
                        near.connected_landmarks.add(landmark)
                        
            # Ensure graph is connected
            self._ensure_connected_graph(landmarks)
            
    def _apply_dimensional_effects(self):
        """Apply effects from landmarks and regions to the world"""
        for layer in DimensionalLayer:
            # Apply region effects
            for region in self.regions[layer]:
                for effect in region.ambient_effects:
                    self.combat_system.add_dimensional_effect(
                        layer,
                        effect
                    )
                    
            # Apply landmark effects
            for landmark in self.landmarks[layer]:
                state = self.combat_system.dimensional_states[layer]
                
                # Apply stability modifier
                current_stability = state.stability
                new_stability = max(0.0, min(1.0,
                    current_stability + landmark.stability_modifier
                ))
                self.combat_system.update_dimensional_stability(
                    layer,
                    new_stability - current_stability
                )
                
                # Apply effects
                for effect in landmark.effects:
                    self.combat_system.add_dimensional_effect(
                        layer,
                        effect
                    )
                    
    def _calculate_base_stability(self, layer: DimensionalLayer) -> float:
        """Calculate base stability for a region based on dimension"""
        base_stabilities = {
            DimensionalLayer.PHYSICAL: 0.9,
            DimensionalLayer.ETHEREAL: 0.8,
            DimensionalLayer.CELESTIAL: 0.7,
            DimensionalLayer.VOID: 0.5,
            DimensionalLayer.PRIMORDIAL: 0.3
        }
        return base_stabilities[layer]
        
    def _generate_ambient_effects(
        self,
        layer: DimensionalLayer
    ) -> Set[DimensionalEffect]:
        """Generate ambient effects for a region"""
        effects = set()
        num_effects = random.randint(1, 2)
        
        possible_effects = {
            DimensionalLayer.PHYSICAL: [
                DimensionalEffect.RESONANCE
            ],
            DimensionalLayer.ETHEREAL: [
                DimensionalEffect.PHASING,
                DimensionalEffect.RESONANCE
            ],
            DimensionalLayer.CELESTIAL: [
                DimensionalEffect.RESONANCE,
                DimensionalEffect.WARPING
            ],
            DimensionalLayer.VOID: [
                DimensionalEffect.DISSONANCE,
                DimensionalEffect.WARPING
            ],
            DimensionalLayer.PRIMORDIAL: [
                DimensionalEffect.WARPING,
                DimensionalEffect.ANCHORING
            ]
        }
        
        for _ in range(num_effects):
            effect = random.choice(possible_effects[layer])
            effects.add(effect)
            
        return effects
        
    def _calculate_region_difficulty(
        self,
        layer: DimensionalLayer,
        distance: float
    ) -> float:
        """Calculate difficulty rating for a region"""
        # Base difficulty by dimension
        base_difficulty = {
            DimensionalLayer.PHYSICAL: 0.2,
            DimensionalLayer.ETHEREAL: 0.4,
            DimensionalLayer.CELESTIAL: 0.6,
            DimensionalLayer.VOID: 0.8,
            DimensionalLayer.PRIMORDIAL: 1.0
        }[layer]
        
        # Add distance modifier
        distance_mod = distance / 100.0
        
        return min(1.0, base_difficulty + distance_mod)
        
    def _select_landmark_type(
        self,
        layer: DimensionalLayer,
        region: Region
    ) -> LandmarkType:
        """Select appropriate landmark type for region"""
        weights = {
            LandmarkType.SANCTUARY: 1.0 - region.difficulty_rating,
            LandmarkType.VOID_RIFT: region.difficulty_rating,
            LandmarkType.POWER_NODE: 0.5,
            LandmarkType.ANCIENT_RUIN: 0.4,
            LandmarkType.RESONANCE_WELL: 0.3,
            LandmarkType.DISTORTION_FIELD: region.difficulty_rating * 0.5
        }
        
        types = list(weights.keys())
        weights = list(weights.values())
        
        return random.choices(types, weights=weights)[0]
        
    def _get_landmark_stability_modifier(
        self,
        landmark_type: LandmarkType
    ) -> float:
        """Get stability modifier for landmark type"""
        modifiers = {
            LandmarkType.NEXUS: 0.2,
            LandmarkType.SANCTUARY: 0.3,
            LandmarkType.VOID_RIFT: -0.4,
            LandmarkType.POWER_NODE: 0.1,
            LandmarkType.ANCIENT_RUIN: 0.0,
            LandmarkType.RESONANCE_WELL: 0.4,
            LandmarkType.DISTORTION_FIELD: -0.2
        }
        return modifiers[landmark_type]
        
    def _get_landmark_effects(
        self,
        landmark_type: LandmarkType
    ) -> Set[DimensionalEffect]:
        """Get effects for landmark type"""
        effects = {
            LandmarkType.NEXUS: {DimensionalEffect.RESONANCE},
            LandmarkType.SANCTUARY: {DimensionalEffect.ANCHORING},
            LandmarkType.VOID_RIFT: {
                DimensionalEffect.WARPING,
                DimensionalEffect.DISSONANCE
            },
            LandmarkType.POWER_NODE: {DimensionalEffect.RESONANCE},
            LandmarkType.ANCIENT_RUIN: set(),
            LandmarkType.RESONANCE_WELL: {DimensionalEffect.RESONANCE},
            LandmarkType.DISTORTION_FIELD: {DimensionalEffect.WARPING}
        }
        return effects[landmark_type]
        
    def _calculate_landmark_difficulty(
        self,
        landmark_type: LandmarkType,
        region_difficulty: float
    ) -> float:
        """Calculate difficulty rating for a landmark"""
        type_modifiers = {
            LandmarkType.NEXUS: 0.0,
            LandmarkType.SANCTUARY: -0.2,
            LandmarkType.VOID_RIFT: 0.4,
            LandmarkType.POWER_NODE: 0.2,
            LandmarkType.ANCIENT_RUIN: 0.1,
            LandmarkType.RESONANCE_WELL: -0.1,
            LandmarkType.DISTORTION_FIELD: 0.3
        }
        
        difficulty = region_difficulty + type_modifiers[landmark_type]
        return max(0.0, min(1.0, difficulty))
        
    def _find_nearest_landmarks(
        self,
        landmark: Landmark,
        count: int
    ) -> List[Landmark]:
        """Find nearest landmarks to given landmark"""
        layer = DimensionalLayer(landmark.position.dimensional_layer)
        others = [l for l in self.landmarks[layer] if l != landmark]
        
        def distance(l1: Landmark, l2: Landmark) -> float:
            return math.sqrt(
                (l1.position.x - l2.position.x) ** 2 +
                (l1.position.y - l2.position.y) ** 2 +
                (l1.position.z - l2.position.z) ** 2
            )
            
        others.sort(key=lambda l: distance(landmark, l))
        return others[:count]
        
    def _can_connect_landmarks(
        self,
        l1: Landmark,
        l2: Landmark
    ) -> bool:
        """Check if two landmarks can be connected"""
        # Check if path exists between landmarks
        path = self.pathfinder.find_path(l1.position, l2.position)
        if path is None:
            return False
            
        # Check distance
        dx = l1.position.x - l2.position.x
        dy = l1.position.y - l2.position.y
        dz = l1.position.z - l2.position.z
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        return distance <= (l1.influence_radius + l2.influence_radius) * 1.5
        
    def _ensure_connected_graph(self, landmarks: List[Landmark]):
        """Ensure all landmarks are connected in a single graph"""
        if not landmarks:
            return
            
        # Find disconnected components
        components = self._find_components(landmarks)
        
        # Connect components
        while len(components) > 1:
            c1 = components[0]
            c2 = components[1]
            
            # Find closest landmarks between components
            min_dist = float('inf')
            l1_connect = None
            l2_connect = None
            
            for l1 in c1:
                for l2 in c2:
                    dx = l1.position.x - l2.position.x
                    dy = l1.position.y - l2.position.y
                    dz = l1.position.z - l2.position.z
                    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                    
                    if dist < min_dist:
                        min_dist = dist
                        l1_connect = l1
                        l2_connect = l2
                        
            # Connect landmarks
            if l1_connect and l2_connect:
                l1_connect.connected_landmarks.add(l2_connect)
                l2_connect.connected_landmarks.add(l1_connect)
                
            # Recalculate components
            components = self._find_components(landmarks)
            
    def _find_components(self, landmarks: List[Landmark]) -> List[Set[Landmark]]:
        """Find connected components in landmark graph"""
        components = []
        unvisited = set(landmarks)
        
        while unvisited:
            # Start new component
            start = unvisited.pop()
            component = {start}
            stack = [start]
            
            # DFS to find connected landmarks
            while stack:
                current = stack.pop()
                for neighbor in current.connected_landmarks:
                    if neighbor in unvisited:
                        unvisited.remove(neighbor)
                        component.add(neighbor)
                        stack.append(neighbor)
                        
            components.append(component)
            
        return components 