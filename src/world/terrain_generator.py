from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum, auto
import noise
import numpy as np
from src.combat_system.dimensional_combat import DimensionalLayer, Position
from src.world.world_generator import Region, Landmark, LandmarkType

class TerrainType(Enum):
    # Physical Dimension
    PLAINS = auto()
    MOUNTAINS = auto()
    FOREST = auto()
    WATER = auto()
    
    # Ethereal Dimension
    MIST_FIELDS = auto()
    CRYSTAL_FORMATIONS = auto()
    SPIRIT_GROVES = auto()
    VOID_POOLS = auto()
    
    # Celestial Dimension
    STARDUST_FIELDS = auto()
    ASTRAL_PEAKS = auto()
    CONSTELLATION_FORESTS = auto()
    NEBULA_SEAS = auto()
    
    # Void Dimension
    SHADOW_WASTES = auto()
    CHAOS_SPIRES = auto()
    ENTROPY_FIELDS = auto()
    DARK_MATTER_POOLS = auto()
    
    # Primordial Dimension
    REALITY_FRACTURES = auto()
    ESSENCE_CRYSTALS = auto()
    PRIMAL_STORMS = auto()
    TIME_DISTORTIONS = auto()

@dataclass
class TerrainCell:
    """Represents a single cell in the terrain grid"""
    position: Position
    height: float
    terrain_type: TerrainType
    traversable: bool
    hazard_level: float
    stability_modifier: float

class TerrainGenerator:
    """Generates terrain for dimensional regions"""
    
    def __init__(self, cell_size: float = 1.0):
        self.cell_size = cell_size
        self.octaves = 6
        self.persistence = 0.5
        self.lacunarity = 2.0
        self.dimension_frequencies = {
            DimensionalLayer.PHYSICAL: 1.0,
            DimensionalLayer.ETHEREAL: 1.5,
            DimensionalLayer.CELESTIAL: 2.0,
            DimensionalLayer.VOID: 2.5,
            DimensionalLayer.PRIMORDIAL: 3.0
        }
        self.terrain_thresholds = self._initialize_terrain_thresholds()
        
    def generate_terrain(
        self,
        region: Region,
        landmarks: List[Landmark]
    ) -> Dict[Tuple[int, int], TerrainCell]:
        """Generate terrain for a region"""
        terrain = {}
        
        # Calculate grid bounds
        min_x = int((region.center.x - region.radius) / self.cell_size)
        max_x = int((region.center.x + region.radius) / self.cell_size)
        min_y = int((region.center.y - region.radius) / self.cell_size)
        max_y = int((region.center.y + region.radius) / self.cell_size)
        
        # Generate base terrain
        base_terrain = self._generate_base_terrain(
            region,
            min_x, max_x,
            min_y, max_y
        )
        
        # Apply landmark influences
        terrain = self._apply_landmark_influences(
            base_terrain,
            landmarks,
            region
        )
        
        # Post-process terrain
        terrain = self._post_process_terrain(terrain, region)
        
        return terrain
        
    def _generate_base_terrain(
        self,
        region: Region,
        min_x: int,
        max_x: int,
        min_y: int,
        max_y: int
    ) -> Dict[Tuple[int, int], TerrainCell]:
        """Generate base terrain using noise functions"""
        terrain = {}
        layer = DimensionalLayer(region.center.dimensional_layer)
        frequency = self.dimension_frequencies[layer]
        
        # Generate height map
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                # Calculate world position
                world_x = x * self.cell_size
                world_y = y * self.cell_size
                
                # Check if within region
                dx = world_x - region.center.x
                dy = world_y - region.center.y
                if (dx*dx + dy*dy) > region.radius * region.radius:
                    continue
                
                # Generate height using multiple noise layers
                height = noise.snoise3(
                    x=x * frequency * 0.1,
                    y=y * frequency * 0.1,
                    z=region.terrain_seed,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity
                )
                
                # Add variation noise
                variation = noise.snoise3(
                    x=x * frequency * 0.2,
                    y=y * frequency * 0.2,
                    z=region.terrain_seed + 1000,
                    octaves=3
                )
                
                height = (height + variation * 0.3) * 0.5 + 0.5
                
                # Determine terrain type
                terrain_type = self._determine_terrain_type(
                    height,
                    layer,
                    variation
                )
                
                # Create terrain cell
                cell = TerrainCell(
                    position=Position(
                        x=world_x,
                        y=world_y,
                        z=height * 10.0,
                        dimensional_layer=layer.value
                    ),
                    height=height,
                    terrain_type=terrain_type,
                    traversable=self._is_traversable(terrain_type),
                    hazard_level=self._calculate_hazard_level(
                        height,
                        terrain_type,
                        region.difficulty_rating
                    ),
                    stability_modifier=self._calculate_stability_modifier(
                        height,
                        terrain_type,
                        layer
                    )
                )
                
                terrain[(x, y)] = cell
                
        return terrain
        
    def _apply_landmark_influences(
        self,
        terrain: Dict[Tuple[int, int], TerrainCell],
        landmarks: List[Landmark],
        region: Region
    ) -> Dict[Tuple[int, int], TerrainCell]:
        """Apply landmark influences to terrain"""
        for landmark in landmarks:
            # Calculate influence radius in grid cells
            radius_cells = int(landmark.influence_radius / self.cell_size)
            
            # Get affected cells
            center_x = int(landmark.position.x / self.cell_size)
            center_y = int(landmark.position.y / self.cell_size)
            
            for dx in range(-radius_cells, radius_cells + 1):
                for dy in range(-radius_cells, radius_cells + 1):
                    x = center_x + dx
                    y = center_y + dy
                    
                    if (x, y) not in terrain:
                        continue
                        
                    # Calculate influence factor
                    distance = (dx*dx + dy*dy) ** 0.5
                    if distance > radius_cells:
                        continue
                        
                    influence = 1.0 - (distance / radius_cells)
                    cell = terrain[(x, y)]
                    
                    # Apply landmark-specific modifications
                    cell = self._apply_landmark_effect(
                        cell,
                        landmark,
                        influence
                    )
                    
                    terrain[(x, y)] = cell
                    
        return terrain
        
    def _post_process_terrain(
        self,
        terrain: Dict[Tuple[int, int], TerrainCell],
        region: Region
    ) -> Dict[Tuple[int, int], TerrainCell]:
        """Post-process terrain for consistency"""
        processed = terrain.copy()
        
        # Smooth terrain heights
        for (x, y), cell in terrain.items():
            neighbors = [
                terrain.get((x+dx, y+dy))
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
                if (x+dx, y+dy) in terrain
            ]
            
            if not neighbors:
                continue
                
            # Average height with neighbors
            avg_height = sum(n.height for n in neighbors) / len(neighbors)
            new_height = cell.height * 0.7 + avg_height * 0.3
            
            # Update cell
            processed[(x, y)] = TerrainCell(
                position=Position(
                    x=cell.position.x,
                    y=cell.position.y,
                    z=new_height * 10.0,
                    dimensional_layer=cell.position.dimensional_layer
                ),
                height=new_height,
                terrain_type=cell.terrain_type,
                traversable=cell.traversable,
                hazard_level=cell.hazard_level,
                stability_modifier=cell.stability_modifier
            )
            
        return processed
        
    def _determine_terrain_type(
        self,
        height: float,
        layer: DimensionalLayer,
        variation: float
    ) -> TerrainType:
        """Determine terrain type based on height and dimension"""
        thresholds = self.terrain_thresholds[layer]
        
        # Add some randomness to thresholds
        adjusted_height = height + variation * 0.2
        
        for terrain_type, threshold in thresholds:
            if adjusted_height <= threshold:
                return terrain_type
                
        return thresholds[-1][0]  # Return highest terrain type
        
    def _is_traversable(self, terrain_type: TerrainType) -> bool:
        """Determine if terrain type is traversable"""
        non_traversable = {
            TerrainType.WATER,
            TerrainType.VOID_POOLS,
            TerrainType.NEBULA_SEAS,
            TerrainType.DARK_MATTER_POOLS,
            TerrainType.TIME_DISTORTIONS,
            TerrainType.PRIMAL_STORMS
        }
        return terrain_type not in non_traversable
        
    def _calculate_hazard_level(
        self,
        height: float,
        terrain_type: TerrainType,
        region_difficulty: float
    ) -> float:
        """Calculate hazard level for terrain"""
        # Base hazard from height (steepness)
        hazard = max(0.0, height - 0.5) * 0.5
        
        # Add terrain type hazard
        hazard_modifiers = {
            # Physical
            TerrainType.PLAINS: 0.0,
            TerrainType.MOUNTAINS: 0.4,
            TerrainType.FOREST: 0.2,
            TerrainType.WATER: 0.3,
            
            # Ethereal
            TerrainType.MIST_FIELDS: 0.2,
            TerrainType.CRYSTAL_FORMATIONS: 0.3,
            TerrainType.SPIRIT_GROVES: 0.1,
            TerrainType.VOID_POOLS: 0.5,
            
            # Celestial
            TerrainType.STARDUST_FIELDS: 0.3,
            TerrainType.ASTRAL_PEAKS: 0.5,
            TerrainType.CONSTELLATION_FORESTS: 0.2,
            TerrainType.NEBULA_SEAS: 0.6,
            
            # Void
            TerrainType.SHADOW_WASTES: 0.4,
            TerrainType.CHAOS_SPIRES: 0.7,
            TerrainType.ENTROPY_FIELDS: 0.5,
            TerrainType.DARK_MATTER_POOLS: 0.8,
            
            # Primordial
            TerrainType.REALITY_FRACTURES: 0.6,
            TerrainType.ESSENCE_CRYSTALS: 0.5,
            TerrainType.PRIMAL_STORMS: 0.9,
            TerrainType.TIME_DISTORTIONS: 0.7
        }
        
        hazard += hazard_modifiers[terrain_type]
        
        # Scale with region difficulty
        hazard *= (0.5 + region_difficulty * 0.5)
        
        return min(1.0, hazard)
        
    def _calculate_stability_modifier(
        self,
        height: float,
        terrain_type: TerrainType,
        layer: DimensionalLayer
    ) -> float:
        """Calculate stability modifier for terrain"""
        # Base stability from height
        stability = 0.0
        
        # Add terrain type modifier
        stability_modifiers = {
            # Physical
            TerrainType.PLAINS: 0.2,
            TerrainType.MOUNTAINS: -0.1,
            TerrainType.FOREST: 0.1,
            TerrainType.WATER: 0.0,
            
            # Ethereal
            TerrainType.MIST_FIELDS: 0.1,
            TerrainType.CRYSTAL_FORMATIONS: 0.2,
            TerrainType.SPIRIT_GROVES: 0.3,
            TerrainType.VOID_POOLS: -0.2,
            
            # Celestial
            TerrainType.STARDUST_FIELDS: 0.2,
            TerrainType.ASTRAL_PEAKS: 0.3,
            TerrainType.CONSTELLATION_FORESTS: 0.2,
            TerrainType.NEBULA_SEAS: -0.1,
            
            # Void
            TerrainType.SHADOW_WASTES: -0.2,
            TerrainType.CHAOS_SPIRES: -0.3,
            TerrainType.ENTROPY_FIELDS: -0.4,
            TerrainType.DARK_MATTER_POOLS: -0.5,
            
            # Primordial
            TerrainType.REALITY_FRACTURES: -0.4,
            TerrainType.ESSENCE_CRYSTALS: 0.3,
            TerrainType.PRIMAL_STORMS: -0.6,
            TerrainType.TIME_DISTORTIONS: -0.5
        }
        
        stability += stability_modifiers[terrain_type]
        
        # Scale based on dimension
        dimension_scale = {
            DimensionalLayer.PHYSICAL: 1.0,
            DimensionalLayer.ETHEREAL: 0.8,
            DimensionalLayer.CELESTIAL: 0.6,
            DimensionalLayer.VOID: 0.4,
            DimensionalLayer.PRIMORDIAL: 0.2
        }
        
        stability *= dimension_scale[layer]
        
        return max(-1.0, min(1.0, stability))
        
    def _apply_landmark_effect(
        self,
        cell: TerrainCell,
        landmark: Landmark,
        influence: float
    ) -> TerrainCell:
        """Apply landmark-specific effects to terrain"""
        # Modify height based on landmark type
        height_modifiers = {
            LandmarkType.NEXUS: 0.0,
            LandmarkType.SANCTUARY: -0.2,
            LandmarkType.VOID_RIFT: 0.3,
            LandmarkType.POWER_NODE: 0.2,
            LandmarkType.ANCIENT_RUIN: 0.1,
            LandmarkType.RESONANCE_WELL: -0.1,
            LandmarkType.DISTORTION_FIELD: 0.4
        }
        
        height_mod = height_modifiers[landmark.type] * influence
        new_height = cell.height + height_mod
        
        # Modify hazard level
        hazard_mod = landmark.difficulty_rating * influence
        new_hazard = max(0.0, min(1.0, cell.hazard_level + hazard_mod))
        
        # Modify stability
        stability_mod = landmark.stability_modifier * influence
        new_stability = max(-1.0, min(1.0,
            cell.stability_modifier + stability_mod
        ))
        
        return TerrainCell(
            position=Position(
                x=cell.position.x,
                y=cell.position.y,
                z=new_height * 10.0,
                dimensional_layer=cell.position.dimensional_layer
            ),
            height=new_height,
            terrain_type=cell.terrain_type,
            traversable=cell.traversable,
            hazard_level=new_hazard,
            stability_modifier=new_stability
        )
        
    def _initialize_terrain_thresholds(
        self
    ) -> Dict[DimensionalLayer, List[Tuple[TerrainType, float]]]:
        """Initialize terrain type thresholds for each dimension"""
        return {
            DimensionalLayer.PHYSICAL: [
                (TerrainType.WATER, 0.3),
                (TerrainType.PLAINS, 0.6),
                (TerrainType.FOREST, 0.8),
                (TerrainType.MOUNTAINS, 1.0)
            ],
            DimensionalLayer.ETHEREAL: [
                (TerrainType.VOID_POOLS, 0.25),
                (TerrainType.MIST_FIELDS, 0.5),
                (TerrainType.SPIRIT_GROVES, 0.75),
                (TerrainType.CRYSTAL_FORMATIONS, 1.0)
            ],
            DimensionalLayer.CELESTIAL: [
                (TerrainType.NEBULA_SEAS, 0.3),
                (TerrainType.STARDUST_FIELDS, 0.6),
                (TerrainType.CONSTELLATION_FORESTS, 0.8),
                (TerrainType.ASTRAL_PEAKS, 1.0)
            ],
            DimensionalLayer.VOID: [
                (TerrainType.DARK_MATTER_POOLS, 0.25),
                (TerrainType.SHADOW_WASTES, 0.5),
                (TerrainType.ENTROPY_FIELDS, 0.75),
                (TerrainType.CHAOS_SPIRES, 1.0)
            ],
            DimensionalLayer.PRIMORDIAL: [
                (TerrainType.TIME_DISTORTIONS, 0.2),
                (TerrainType.REALITY_FRACTURES, 0.4),
                (TerrainType.PRIMAL_STORMS, 0.7),
                (TerrainType.ESSENCE_CRYSTALS, 1.0)
            ]
        } 