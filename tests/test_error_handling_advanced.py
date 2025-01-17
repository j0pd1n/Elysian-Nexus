import unittest
from datetime import datetime
from ..systems.error_handling import (
    ErrorHandler, ErrorCategory, ErrorSeverity, GameError,
    StabilityMetrics, RecoveryStrategy
)

class TestAdvancedErrorHandling(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.error_handler = ErrorHandler()
        
    def test_paradox_manifestation(self):
        """Test handling of paradox manifestation errors"""
        details = {
            "paradox_type": "temporal_loop",
            "severity": 0.8,
            "affected_timeline": "main",
            "causality_damage": 0.6
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.PARADOX_MANIFESTATION,
            ErrorSeverity.CRITICAL,
            "Temporal paradox detected",
            details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        self.assertTrue(
            error.handled or 
            error_id not in self.error_handler.active_errors
        )
        
    def test_thaumic_overload(self):
        """Test handling of thaumic overload errors"""
        details = {
            "overload_type": "spell_matrix",
            "energy_level": 0.9,
            "affected_systems": ["mana_conduits", "spell_anchors"],
            "containment_status": "failing"
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.THAUMIC_OVERLOAD,
            ErrorSeverity.HIGH,
            "Critical thaumic overload detected",
            details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        self.assertTrue(
            error.handled or 
            error_id not in self.error_handler.active_errors
        )
        
    def test_aetheric_instability(self):
        """Test handling of aetheric instability errors"""
        details = {
            "instability_type": "resonance_cascade",
            "affected_area": {"radius": 50, "center": "ritual_circle"},
            "energy_signature": {"chaos": 0.8, "void": 0.4, "aether": 0.9}
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.AETHERIC_INSTABILITY,
            ErrorSeverity.CRITICAL,
            "Aetheric instability detected",
            details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        self.assertTrue(
            error.handled or 
            error_id not in self.error_handler.active_errors
        )
        
    def test_reality_storm(self):
        """Test handling of reality storm errors"""
        details = {
            "storm_type": "reality_flux",
            "intensity": 0.9,
            "affected_dimensions": ["material", "ethereal"],
            "reality_integrity": 0.3
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.REALITY_STORM,
            ErrorSeverity.CATASTROPHIC,
            "Reality storm manifesting",
            details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        self.assertTrue(
            error.handled or 
            error_id not in self.error_handler.active_errors
        )
        
    def test_soul_matrix_disruption(self):
        """Test handling of soul matrix disruption errors"""
        details = {
            "disruption_type": "soul_resonance",
            "affected_entities": ["player", "npc_mage"],
            "matrix_integrity": 0.4,
            "resonance_frequency": 0.8
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.SOUL_MATRIX_DISRUPTION,
            ErrorSeverity.HIGH,
            "Soul matrix disruption detected",
            details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        self.assertTrue(
            error.handled or 
            error_id not in self.error_handler.active_errors
        )
        
    def test_multiple_advanced_errors(self):
        """Test handling of multiple advanced errors simultaneously"""
        error_scenarios = [
            (
                ErrorCategory.PARADOX_MANIFESTATION,
                ErrorSeverity.CRITICAL,
                "Temporal paradox",
                {"paradox_type": "timeline_split", "severity": 0.9}
            ),
            (
                ErrorCategory.REALITY_STORM,
                ErrorSeverity.CATASTROPHIC,
                "Reality destabilization",
                {"storm_type": "reality_tear", "intensity": 0.95}
            ),
            (
                ErrorCategory.SOUL_MATRIX_DISRUPTION,
                ErrorSeverity.HIGH,
                "Soul resonance cascade",
                {"disruption_type": "mass_resonance", "affected_entities": ["multiple"]}
            )
        ]
        
        error_ids = []
        for category, severity, message, details in error_scenarios:
            error_id = self.error_handler.handle_error(category, severity, message, details)
            error_ids.append(error_id)
            
        # Verify all errors were handled
        for error_id in error_ids:
            error = self.error_handler.active_errors.get(error_id)
            if error:
                self.assertTrue(error.handled)
                
    def test_recovery_strategy_fallbacks(self):
        """Test fallback recovery strategies for advanced errors"""
        # Create a severe error that might require fallback strategies
        details = {
            "overload_type": "critical_surge",
            "energy_level": 0.95,
            "containment_status": "critical"
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.THAUMIC_OVERLOAD,
            ErrorSeverity.CATASTROPHIC,
            "Critical thaumic overload",
            details
        )
        
        # Verify the error was handled with either primary or fallback strategy
        error = self.error_handler.active_errors.get(error_id)
        if error:
            self.assertTrue(error.handled)
            
    def test_cascading_error_effects(self):
        """Test handling of errors that trigger other errors"""
        # Create an initial error that might cascade
        primary_error_id = self.error_handler.handle_error(
            ErrorCategory.REALITY_STORM,
            ErrorSeverity.CATASTROPHIC,
            "Primary reality storm",
            {
                "storm_type": "cascading_breach",
                "intensity": 1.0,
                "affected_dimensions": ["material", "ethereal", "astral"]
            }
        )
        
        # Check for additional errors in history that were triggered
        history = self.error_handler.get_error_history(limit=10)
        self.assertGreater(len(history), 1)  # Should have triggered additional errors
        
    def test_error_resolution_stability(self):
        """Test stability of error resolution under stress"""
        # Create multiple high-severity errors in rapid succession
        error_count = 10
        error_ids = []
        
        for i in range(error_count):
            error_id = self.error_handler.handle_error(
                ErrorCategory.AETHERIC_INSTABILITY,
                ErrorSeverity.CRITICAL,
                f"Stress test error {i}",
                {
                    "instability_type": "compound_resonance",
                    "severity": 0.9,
                    "affected_area": {"radius": 100 * i}
                }
            )
            error_ids.append(error_id)
            
        # Verify all errors were handled without system failure
        for error_id in error_ids:
            error = self.error_handler.active_errors.get(error_id)
            if error:
                self.assertTrue(error.handled)
                
    def test_resource_management(self):
        """Test resource management during error handling"""
        # Create an error that requires significant resources
        details = {
            "entity_type": "elder_being",
            "breach_type": "dimensional_tear",
            "power_level": 0.9,
            "affected_area": {"radius": 1000, "type": "city"}
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.SUMMONING_BREACH,
            ErrorSeverity.CATASTROPHIC,
            "Major summoning breach",
            details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        if error:
            self.assertTrue(error.handled)

if __name__ == '__main__':
    unittest.main() 