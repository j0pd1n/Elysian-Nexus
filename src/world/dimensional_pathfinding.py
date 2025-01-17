from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional
from queue import PriorityQueue
import math
from src.combat_system.dimensional_combat import (
    DimensionalLayer,
    DimensionalEffect,
    Position,
    DimensionalCombat
)

@dataclass
class PathNode:
    """Represents a node in the dimensional pathfinding graph"""
    position: Position
    g_cost: float = float('inf')  # Cost from start to this node
    h_cost: float = 0.0          # Heuristic cost to goal
    parent: Optional['PathNode'] = None
    
    @property
    def f_cost(self) -> float:
        """Total estimated cost through this node"""
        return self.g_cost + self.h_cost
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

class DimensionalPathfinder:
    """Handles pathfinding across dimensional spaces"""
    
    def __init__(self, combat_system: DimensionalCombat):
        self.combat_system = combat_system
        self.dimensional_cost_multipliers = {
            DimensionalLayer.PHYSICAL: 1.0,
            DimensionalLayer.ETHEREAL: 1.2,
            DimensionalLayer.CELESTIAL: 1.5,
            DimensionalLayer.VOID: 2.0,
            DimensionalLayer.PRIMORDIAL: 3.0
        }
        
    def find_path(
        self,
        start: Position,
        goal: Position,
        max_dimensional_shifts: int = 3
    ) -> Optional[List[Position]]:
        """Find a path from start to goal position across dimensions"""
        start_node = PathNode(position=start)
        start_node.g_cost = 0
        start_node.h_cost = self._calculate_heuristic(start, goal)
        
        open_set = PriorityQueue()
        open_set.put(start_node)
        closed_set: Set[Tuple[float, float, float, int]] = set()
        
        dimensional_shifts = 0
        
        while not open_set.empty():
            current = open_set.get()
            
            # Convert position to tuple for closed set checking
            pos_tuple = (
                current.position.x,
                current.position.y,
                current.position.z,
                current.position.dimensional_layer
            )
            
            if pos_tuple in closed_set:
                continue
                
            closed_set.add(pos_tuple)
            
            # Check if we've reached the goal
            if self._is_goal(current.position, goal):
                return self._reconstruct_path(current)
                
            # Generate neighbors including dimensional shifts
            neighbors = self._get_neighbors(current.position)
            
            for neighbor_pos in neighbors:
                # Check if this is a dimensional shift
                is_shift = (
                    neighbor_pos.dimensional_layer != 
                    current.position.dimensional_layer
                )
                
                if is_shift:
                    if dimensional_shifts >= max_dimensional_shifts:
                        continue
                    if not self._can_shift_dimensions(
                        current.position,
                        neighbor_pos
                    ):
                        continue
                        
                neighbor = PathNode(position=neighbor_pos)
                
                # Calculate costs
                movement_cost = self._calculate_movement_cost(
                    current.position,
                    neighbor_pos
                )
                
                tentative_g_cost = current.g_cost + movement_cost
                
                if tentative_g_cost < neighbor.g_cost:
                    neighbor.g_cost = tentative_g_cost
                    neighbor.h_cost = self._calculate_heuristic(
                        neighbor_pos,
                        goal
                    )
                    neighbor.parent = current
                    
                    if is_shift:
                        dimensional_shifts += 1
                        
                    open_set.put(neighbor)
                    
        return None
        
    def _calculate_heuristic(self, pos: Position, goal: Position) -> float:
        """Calculate heuristic cost estimate between positions"""
        # Euclidean distance
        distance = math.sqrt(
            (pos.x - goal.x) ** 2 +
            (pos.y - goal.y) ** 2 +
            (pos.z - goal.z) ** 2
        )
        
        # Add dimensional distance penalty
        if pos.dimensional_layer != goal.dimensional_layer:
            dimensional_cost = self._calculate_dimensional_cost(
                pos.dimensional_layer,
                goal.dimensional_layer
            )
            distance *= dimensional_cost
            
        return distance
        
    def _calculate_movement_cost(
        self,
        current: Position,
        next_pos: Position
    ) -> float:
        """Calculate the cost of moving between positions"""
        # Base movement cost (Euclidean distance)
        cost = math.sqrt(
            (next_pos.x - current.x) ** 2 +
            (next_pos.y - current.y) ** 2 +
            (next_pos.z - current.z) ** 2
        )
        
        # Apply dimensional cost multiplier
        cost *= self.dimensional_cost_multipliers[
            DimensionalLayer(next_pos.dimensional_layer)
        ]
        
        # Add stability cost
        stability = self.combat_system.dimensional_states[
            DimensionalLayer(next_pos.dimensional_layer)
        ].stability
        stability_multiplier = 1.0 + (1.0 - stability) * 2.0
        cost *= stability_multiplier
        
        # Add effect penalties
        state = self.combat_system.dimensional_states[
            DimensionalLayer(next_pos.dimensional_layer)
        ]
        if DimensionalEffect.WARPING in state.active_effects:
            cost *= 1.5
        if DimensionalEffect.ANCHORING in state.active_effects:
            cost *= 2.0
            
        return cost
        
    def _calculate_dimensional_cost(
        self,
        source: int,
        target: int
    ) -> float:
        """Calculate the cost multiplier for crossing dimensions"""
        source_layer = DimensionalLayer(source)
        target_layer = DimensionalLayer(target)
        
        # Direct connection cost
        if self.combat_system.can_traverse_dimensions(source_layer, target_layer):
            return 1.5
            
        # Indirect connection cost (through intermediate dimensions)
        return 3.0
        
    def _can_shift_dimensions(
        self,
        current: Position,
        next_pos: Position
    ) -> bool:
        """Check if dimensional shift is possible"""
        current_layer = DimensionalLayer(current.dimensional_layer)
        next_layer = DimensionalLayer(next_pos.dimensional_layer)
        
        # Check if dimensions are connected
        if not self.combat_system.can_traverse_dimensions(
            current_layer,
            next_layer
        ):
            return False
            
        # Check stability requirements
        current_stability = self.combat_system.dimensional_states[
            current_layer
        ].stability
        next_stability = self.combat_system.dimensional_states[
            next_layer
        ].stability
        
        if current_stability < 0.2 or next_stability < 0.2:
            return False
            
        # Check for blocking effects
        current_state = self.combat_system.dimensional_states[current_layer]
        next_state = self.combat_system.dimensional_states[next_layer]
        
        if (DimensionalEffect.ANCHORING in current_state.active_effects or
            DimensionalEffect.ANCHORING in next_state.active_effects):
            return False
            
        return True
        
    def _get_neighbors(self, pos: Position) -> List[Position]:
        """Get neighboring positions including dimensional shifts"""
        neighbors = []
        
        # Cardinal directions in current dimension
        directions = [
            (1, 0, 0), (-1, 0, 0),  # X axis
            (0, 1, 0), (0, -1, 0),  # Y axis
            (0, 0, 1), (0, 0, -1)   # Z axis
        ]
        
        for dx, dy, dz in directions:
            neighbors.append(Position(
                x=pos.x + dx,
                y=pos.y + dy,
                z=pos.z + dz,
                dimensional_layer=pos.dimensional_layer
            ))
            
        # Dimensional neighbors (connected dimensions)
        current_layer = DimensionalLayer(pos.dimensional_layer)
        for layer in DimensionalLayer:
            if layer.value != current_layer.value:
                if self.combat_system.can_traverse_dimensions(
                    current_layer,
                    layer
                ):
                    neighbors.append(Position(
                        x=pos.x,
                        y=pos.y,
                        z=pos.z,
                        dimensional_layer=layer.value
                    ))
                    
        return neighbors
        
    def _is_goal(self, current: Position, goal: Position) -> bool:
        """Check if current position matches the goal"""
        distance_threshold = 0.1
        
        distance = math.sqrt(
            (current.x - goal.x) ** 2 +
            (current.y - goal.y) ** 2 +
            (current.z - goal.z) ** 2
        )
        
        return (
            distance <= distance_threshold and
            current.dimensional_layer == goal.dimensional_layer
        )
        
    def _reconstruct_path(self, end_node: PathNode) -> List[Position]:
        """Reconstruct the path from end node to start"""
        path = []
        current = end_node
        
        while current is not None:
            path.append(current.position)
            current = current.parent
            
        return list(reversed(path)) 