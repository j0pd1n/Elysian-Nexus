from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum, auto
import math
from ..combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect, Position

class DimensionalAnomalyType(Enum):
    """Types of dimensional anomalies that can occur in the world"""
    RIFT = auto()          # Tear between dimensions
    NEXUS = auto()         # Convergence of multiple dimensions
    DISTORTION = auto()    # Area of warped space-time
    RESONANCE = auto()     # Area of amplified dimensional energy
    VOID_POCKET = auto()   # Pocket of dimensional void

@dataclass
class DimensionalAnomaly:
    """Represents a dimensional anomaly in the world"""
    anomaly_type: DimensionalAnomalyType
    position: Position
    radius: float
    intensity: float  # 0.0 to 1.0
    affected_dimensions: Set[DimensionalLayer]
    active_effects: Set[DimensionalEffect]
    duration: Optional[int] = None  # None for permanent anomalies
    pulse_frequency: Optional[float] = None  # For pulsing anomalies

@dataclass
class DimensionalZone:
    """Represents a zone with specific dimensional properties"""
    center: Position
    dimensions: Set[DimensionalLayer]
    base_stability: Dict[DimensionalLayer, float]
    anomalies: List[DimensionalAnomaly]
    connected_zones: Set[int]  # Zone IDs
    background_effects: Set[DimensionalEffect]

class DimensionalWorldManager:
    """Manages dimensional aspects of the game world"""
    
    def __init__(self):
        self.zones: Dict[int, DimensionalZone] = {}
        self.active_anomalies: Dict[int, DimensionalAnomaly] = {}
        self.zone_counter: int = 0
        self.anomaly_counter: int = 0
        
    def create_zone(self, 
                   center: Position,
                   dimensions: Set[DimensionalLayer],
                   base_stability: Dict[DimensionalLayer, float]) -> int:
        """Create a new dimensional zone"""
        zone_id = self.zone_counter
        self.zones[zone_id] = DimensionalZone(
            center=center,
            dimensions=dimensions,
            base_stability=base_stability,
            anomalies=[],
            connected_zones=set(),
            background_effects=set()
        )
        self.zone_counter += 1
        return zone_id
        
    def connect_zones(self, zone1_id: int, zone2_id: int):
        """Create a connection between two zones"""
        if zone1_id in self.zones and zone2_id in self.zones:
            self.zones[zone1_id].connected_zones.add(zone2_id)
            self.zones[zone2_id].connected_zones.add(zone1_id)
            
    def create_anomaly(self,
                      anomaly_type: DimensionalAnomalyType,
                      position: Position,
                      radius: float,
                      intensity: float,
                      affected_dimensions: Set[DimensionalLayer],
                      duration: Optional[int] = None) -> int:
        """Create a new dimensional anomaly"""
        anomaly_id = self.anomaly_counter
        anomaly = DimensionalAnomaly(
            anomaly_type=anomaly_type,
            position=position,
            radius=radius,
            intensity=intensity,
            affected_dimensions=affected_dimensions,
            active_effects=self._get_anomaly_effects(anomaly_type),
            duration=duration,
            pulse_frequency=self._get_pulse_frequency(anomaly_type)
        )
        
        self.active_anomalies[anomaly_id] = anomaly
        
        # Add anomaly to affected zones
        for zone in self.zones.values():
            if self._is_position_in_zone(position, zone):
                zone.anomalies.append(anomaly)
                
        self.anomaly_counter += 1
        return anomaly_id
        
    def _get_anomaly_effects(self, 
                           anomaly_type: DimensionalAnomalyType) -> Set[DimensionalEffect]:
        """Get the effects associated with an anomaly type"""
        effects = {
            DimensionalAnomalyType.RIFT: {
                DimensionalEffect.PHASING,
                DimensionalEffect.DISSONANCE
            },
            DimensionalAnomalyType.NEXUS: {
                DimensionalEffect.RESONANCE,
                DimensionalEffect.WARPING
            },
            DimensionalAnomalyType.DISTORTION: {
                DimensionalEffect.WARPING
            },
            DimensionalAnomalyType.RESONANCE: {
                DimensionalEffect.RESONANCE
            },
            DimensionalAnomalyType.VOID_POCKET: {
                DimensionalEffect.ANCHORING,
                DimensionalEffect.DISSONANCE
            }
        }
        return effects.get(anomaly_type, set())
        
    def _get_pulse_frequency(self, anomaly_type: DimensionalAnomalyType) -> Optional[float]:
        """Get pulse frequency for anomaly types that pulse"""
        frequencies = {
            DimensionalAnomalyType.RIFT: 0.5,      # Pulses every 2 seconds
            DimensionalAnomalyType.NEXUS: 0.25,    # Pulses every 4 seconds
            DimensionalAnomalyType.RESONANCE: 1.0  # Pulses every second
        }
        return frequencies.get(anomaly_type)
        
    def _is_position_in_zone(self, position: Position, zone: DimensionalZone) -> bool:
        """Check if a position is within a zone"""
        # Simple radius check - can be made more complex for non-circular zones
        distance = math.sqrt(
            (position.x - zone.center.x) ** 2 +
            (position.y - zone.center.y) ** 2 +
            (position.z - zone.center.z) ** 2
        )
        return distance <= 100  # Default zone radius
        
    def get_active_effects_at_position(self, position: Position) -> Set[DimensionalEffect]:
        """Get all dimensional effects active at a position"""
        effects = set()
        
        # Check each zone
        for zone in self.zones.values():
            if self._is_position_in_zone(position, zone):
                effects.update(zone.background_effects)
                
                # Check anomalies in the zone
                for anomaly in zone.anomalies:
                    if self._is_position_affected_by_anomaly(position, anomaly):
                        effects.update(anomaly.active_effects)
                        
        return effects
        
    def _is_position_affected_by_anomaly(self, 
                                      position: Position, 
                                      anomaly: DimensionalAnomaly) -> bool:
        """Check if a position is affected by an anomaly"""
        distance = math.sqrt(
            (position.x - anomaly.position.x) ** 2 +
            (position.y - anomaly.position.y) ** 2 +
            (position.z - anomaly.position.z) ** 2
        )
        return distance <= anomaly.radius
        
    def get_dimensional_stability(self, 
                               position: Position,
                               dimension: DimensionalLayer) -> float:
        """Calculate dimensional stability at a position"""
        base_stability = 1.0
        total_influence = 0.0
        
        # Get affecting zone
        for zone in self.zones.values():
            if self._is_position_in_zone(position, zone):
                base_stability = zone.base_stability.get(dimension, 1.0)
                
                # Calculate anomaly influences
                for anomaly in zone.anomalies:
                    if dimension in anomaly.affected_dimensions and \
                       self._is_position_affected_by_anomaly(position, anomaly):
                        distance = math.sqrt(
                            (position.x - anomaly.position.x) ** 2 +
                            (position.y - anomaly.position.y) ** 2 +
                            (position.z - anomaly.position.z) ** 2
                        )
                        # Influence decreases with distance
                        influence = anomaly.intensity * (1 - (distance / anomaly.radius))
                        total_influence += influence
                        
        # Apply influences to base stability
        final_stability = max(0.0, min(1.0, base_stability - total_influence))
        return final_stability
        
    def update(self, delta_time: float):
        """Update dimensional world state"""
        # Update anomalies
        anomalies_to_remove = []
        
        for anomaly_id, anomaly in self.active_anomalies.items():
            if anomaly.duration is not None:
                anomaly.duration -= delta_time
                if anomaly.duration <= 0:
                    anomalies_to_remove.append(anomaly_id)
                    
            # Update pulsing anomalies
            if anomaly.pulse_frequency is not None:
                # Calculate pulse intensity
                pulse = math.sin(delta_time * anomaly.pulse_frequency * 2 * math.pi)
                anomaly.intensity = (pulse + 1) / 2  # Normalize to 0-1
                
        # Remove expired anomalies
        for anomaly_id in anomalies_to_remove:
            self._remove_anomaly(anomaly_id)
            
    def _remove_anomaly(self, anomaly_id: int):
        """Remove an anomaly from the world"""
        if anomaly_id in self.active_anomalies:
            anomaly = self.active_anomalies[anomaly_id]
            
            # Remove from zones
            for zone in self.zones.values():
                if anomaly in zone.anomalies:
                    zone.anomalies.remove(anomaly)
                    
            del self.active_anomalies[anomaly_id]
            
    def get_nearest_anomaly(self, position: Position) -> Optional[Tuple[int, DimensionalAnomaly]]:
        """Find the nearest anomaly to a position"""
        if not self.active_anomalies:
            return None
            
        nearest = min(
            self.active_anomalies.items(),
            key=lambda x: math.sqrt(
                (position.x - x[1].position.x) ** 2 +
                (position.y - x[1].position.y) ** 2 +
                (position.z - x[1].position.z) ** 2
            )
        )
        return nearest
        
    def get_zone_info(self, position: Position) -> Optional[Tuple[int, DimensionalZone]]:
        """Get information about the zone at a position"""
        for zone_id, zone in self.zones.items():
            if self._is_position_in_zone(position, zone):
                return (zone_id, zone)
        return None 