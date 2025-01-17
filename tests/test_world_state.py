import unittest
import time
from typing import Dict, Set, List
from src.infrastructure.test_framework import TestDecorators, TestType, TestPriority
from src.infrastructure.performance_monitor import MetricType
from src.world.world_state import (
    WorldState,
    DimensionalZone,
    DimensionalAnomaly,
    AnomalyType,
    Position,
    StateSnapshot
)

class TestWorldState(unittest.TestCase):
    """Test cases for world state management system"""
    
    def setUp(self):
        """Set up test environment"""
        self.world_state = WorldState()
        self.test_zones = {
            "sanctuary": DimensionalZone(
                name="Sanctuary",
                dimension="Physical",
                stability=1.0,
                anomaly_resistance=0.8
            ),
            "void_breach": DimensionalZone(
                name="Void Breach",
                dimension="Void",
                stability=0.4,
                anomaly_resistance=0.2
            ),
            "nexus": DimensionalZone(
                name="Dimensional Nexus",
                dimension="Ethereal",
                stability=0.7,
                anomaly_resistance=0.5
            )
        }
        
    @TestDecorators.test_type(TestType.UNIT)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_zone_management(self):
        """Test zone creation and management"""
        # Add zones
        for zone in self.test_zones.values():
            self.world_state.add_zone(zone)
            
        # Verify zone count and properties
        zones = self.world_state.get_zones()
        self.assertEqual(len(zones), 3)
        
        # Test zone connections
        self.world_state.connect_zones(
            "Sanctuary",
            "Dimensional Nexus",
            stability_threshold=0.6
        )
        
        connections = self.world_state.get_zone_connections("Sanctuary")
        self.assertIn("Dimensional Nexus", connections)
        
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    def test_anomaly_propagation(self):
        """Test anomaly creation and propagation"""
        # Setup zones
        for zone in self.test_zones.values():
            self.world_state.add_zone(zone)
            
        # Create anomaly
        void_anomaly = DimensionalAnomaly(
            type=AnomalyType.VOID_RIFT,
            power=50,
            position=Position(x=0, y=0, z=0),
            radius=10.0
        )
        
        # Add anomaly and check propagation
        self.world_state.add_anomaly(
            zone_name="Void Breach",
            anomaly=void_anomaly
        )
        
        # Check affected zones
        affected_zones = self.world_state.get_affected_zones(void_anomaly)
        self.assertGreater(len(affected_zones), 0)
        
        # Verify stability changes
        for zone in affected_zones:
            current_stability = self.world_state.get_zone_stability(zone)
            original_stability = self.test_zones[zone].stability
            self.assertLess(current_stability, original_stability)
            
    @TestDecorators.test_type(TestType.PERFORMANCE)
    @TestDecorators.test_priority(TestPriority.HIGH)
    @TestDecorators.performance_threshold(MetricType.DIMENSION_TRANSITIONS, 15.0)
    def test_state_update_performance(self):
        """Test performance of world state updates"""
        # Setup large world state
        for i in range(100):
            zone = DimensionalZone(
                name=f"Zone_{i}",
                dimension="Physical" if i % 3 == 0 else "Ethereal" if i % 3 == 1 else "Void",
                stability=0.5 + (i % 5) * 0.1,
                anomaly_resistance=0.3 + (i % 3) * 0.2
            )
            self.world_state.add_zone(zone)
            
        start_time = time.time()
        
        # Perform state update
        self.world_state.update_world_state(time_delta=1.0)
        
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to ms
        
        # Verify performance
        self.assertLess(duration, 15.0)  # Should update within 15ms
        
    @TestDecorators.test_type(TestType.STRESS)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_state_under_load(self):
        """Test world state under heavy load"""
        # Create many zones and anomalies
        for i in range(50):
            zone = DimensionalZone(
                name=f"Zone_{i}",
                dimension="Physical" if i % 5 == 0 else "Ethereal" if i % 5 == 1 else "Void",
                stability=0.5 + (i % 5) * 0.1,
                anomaly_resistance=0.3 + (i % 3) * 0.2
            )
            self.world_state.add_zone(zone)
            
            if i % 3 == 0:  # Add anomaly to every third zone
                anomaly = DimensionalAnomaly(
                    type=AnomalyType.VOID_RIFT if i % 2 == 0 else AnomalyType.RESONANCE,
                    power=30 + i,
                    position=Position(x=i, y=i, z=0),
                    radius=5.0
                )
                self.world_state.add_anomaly(f"Zone_{i}", anomaly)
                
        # Perform multiple updates
        for _ in range(100):
            self.world_state.update_world_state(time_delta=0.1)
            
        # Verify system stability
        for i in range(50):
            zone_name = f"Zone_{i}"
            stability = self.world_state.get_zone_stability(zone_name)
            self.assertGreaterEqual(stability, 0.1)  # Minimum stability threshold
            
    @TestDecorators.test_type(TestType.INTEGRATION)
    @TestDecorators.test_priority(TestPriority.HIGH)
    def test_state_persistence(self):
        """Test state saving and loading"""
        # Setup initial state
        for zone in self.test_zones.values():
            self.world_state.add_zone(zone)
            
        # Add some anomalies
        anomalies = [
            DimensionalAnomaly(
                type=AnomalyType.VOID_RIFT,
                power=50,
                position=Position(x=0, y=0, z=0),
                radius=10.0
            ),
            DimensionalAnomaly(
                type=AnomalyType.RESONANCE,
                power=30,
                position=Position(x=10, y=10, z=0),
                radius=5.0
            )
        ]
        
        for i, anomaly in enumerate(anomalies):
            self.world_state.add_anomaly(
                list(self.test_zones.keys())[i],
                anomaly
            )
            
        # Save state
        snapshot = self.world_state.create_snapshot()
        
        # Modify current state
        self.world_state.update_world_state(time_delta=5.0)
        
        # Load saved state
        self.world_state.load_snapshot(snapshot)
        
        # Verify state restoration
        for zone_name, original_zone in self.test_zones.items():
            current_stability = self.world_state.get_zone_stability(zone_name)
            self.assertEqual(current_stability, original_zone.stability)
            
    @TestDecorators.test_type(TestType.DIMENSION)
    @TestDecorators.test_priority(TestPriority.CRITICAL)
    def test_dimensional_boundaries(self):
        """Test dimensional boundary management"""
        # Setup zones in different dimensions
        for zone in self.test_zones.values():
            self.world_state.add_zone(zone)
            
        # Create boundary anomaly
        boundary_anomaly = DimensionalAnomaly(
            type=AnomalyType.DIMENSIONAL_TEAR,
            power=75,
            position=Position(x=5, y=5, z=0),
            radius=15.0
        )
        
        # Add anomaly at dimensional boundary
        self.world_state.add_anomaly("Dimensional Nexus", boundary_anomaly)
        
        # Test boundary stability
        boundary_stability = self.world_state.get_boundary_stability(
            "Physical",
            "Ethereal"
        )
        
        self.assertLess(boundary_stability, 1.0)
        self.assertGreater(boundary_stability, 0.0)
        
        # Test boundary crossing requirements
        requirements = self.world_state.get_boundary_crossing_requirements(
            "Physical",
            "Ethereal"
        )
        
        self.assertGreater(requirements.power_requirement, 0)
        self.assertGreater(requirements.stability_threshold, 0)

if __name__ == '__main__':
    unittest.main() 