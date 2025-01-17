import unittest
from datetime import datetime
from ..systems.error_handling import (
    ErrorHandler, ErrorCategory, ErrorSeverity, GameError,
    StabilityMetrics, RecoveryStrategy
)

class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.error_handler = ErrorHandler()
        self.test_error_details = {
            "ritual_type": "summoning",
            "power_level": 0.7,
            "participants": ["mage1", "mage2"],
            "affected_area": {"size": 10, "type": "ritual_chamber"}
        }
        
    def test_error_creation(self):
        """Test creation and registration of new errors"""
        error_id = self.error_handler.handle_error(
            ErrorCategory.RITUAL_INTERRUPTION,
            ErrorSeverity.HIGH,
            "Test ritual interruption",
            self.test_error_details
        )
        
        self.assertIsNotNone(error_id)
        self.assertIn(error_id, self.error_handler.active_errors)
        
        error = self.error_handler.active_errors[error_id]
        self.assertEqual(error.category, ErrorCategory.RITUAL_INTERRUPTION)
        self.assertEqual(error.severity, ErrorSeverity.HIGH)
        self.assertEqual(error.details, self.test_error_details)
        
    def test_error_handling_ritual_interruption(self):
        """Test handling of ritual interruption errors"""
        error_id = self.error_handler.handle_error(
            ErrorCategory.RITUAL_INTERRUPTION,
            ErrorSeverity.HIGH,
            "Ritual interruption during summoning",
            self.test_error_details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        
        # Verify error was handled
        self.assertTrue(
            error.handled or 
            error_id not in self.error_handler.active_errors
        )
        
    def test_error_handling_dimensional_anomaly(self):
        """Test handling of dimensional anomaly errors"""
        anomaly_details = {
            "anomaly_type": "rift",
            "size": 0.8,
            "energy_signature": {"chaos": 0.7, "void": 0.3}
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.DIMENSIONAL_ANOMALY,
            ErrorSeverity.CRITICAL,
            "Dimensional rift detected",
            anomaly_details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        
        # Verify error was handled
        self.assertTrue(
            error.handled or 
            error_id not in self.error_handler.active_errors
        )
        
    def test_error_escalation(self):
        """Test error escalation for unhandled errors"""
        # Create a low severity error
        error_id = self.error_handler.handle_error(
            ErrorCategory.MAGICAL_BACKLASH,
            ErrorSeverity.LOW,
            "Minor magical backlash",
            {"power_level": 0.3}
        )
        
        # Force escalation
        error = self.error_handler.active_errors[error_id]
        self.error_handler._escalate_error(error)
        
        # Check error history for escalated error
        history = self.error_handler.get_error_history(limit=2)
        self.assertTrue(any(
            e.severity == ErrorSeverity.MEDIUM and 
            "Escalated" in e.message 
            for e in history
        ))
        
    def test_recovery_strategies(self):
        """Test recovery strategy initialization and application"""
        strategies = self.error_handler.recovery_strategies
        
        # Check if strategies exist for all error categories
        for category in ErrorCategory:
            self.assertIn(category, strategies)
            category_strategies = strategies[category]
            self.assertGreater(len(category_strategies), 0)
            
            # Verify strategy structure
            for strategy in category_strategies:
                self.assertIsInstance(strategy, RecoveryStrategy)
                self.assertTrue(0 <= strategy.success_chance <= 1)
                self.assertIsInstance(strategy.resource_cost, dict)
                self.assertIsInstance(strategy.side_effects, list)
                
    def test_error_history(self):
        """Test error history tracking"""
        # Create multiple errors
        for _ in range(5):
            self.error_handler.handle_error(
                ErrorCategory.RITUAL_INTERRUPTION,
                ErrorSeverity.MEDIUM,
                "Test error",
                self.test_error_details
            )
            
        history = self.error_handler.get_error_history(limit=10)
        self.assertEqual(len(history), 5)
        self.assertTrue(all(isinstance(e, GameError) for e in history))
        
    def test_stability_metrics(self):
        """Test stability metrics tracking"""
        metrics = StabilityMetrics(
            energy_level=0.8,
            containment_integrity=0.9,
            mana_stability=0.7,
            dimensional_stability=0.6,
            temporal_coherence=0.8
        )
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.CONTAINMENT_BREACH,
            ErrorSeverity.HIGH,
            "Containment breach detected",
            {
                "breach_type": "energy_surge",
                "stability_metrics": metrics
            }
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        self.assertIsNotNone(error.stability_metrics)
        
    def test_cascade_failure_handling(self):
        """Test handling of cascade failures"""
        cascade_details = {
            "severity": 0.8,
            "affected_systems": ["power_core", "containment_field"],
            "failure_points": [
                {"type": "ENERGY_NEXUS", "stability": 0.3},
                {"type": "CONTAINMENT_FIELD", "stability": 0.4}
            ]
        }
        
        error_id = self.error_handler.handle_error(
            ErrorCategory.CASCADE_FAILURE,
            ErrorSeverity.CRITICAL,
            "Critical cascade failure detected",
            cascade_details
        )
        
        error = self.error_handler.active_errors.get(error_id)
        self.assertIsNotNone(error)
        
        # Verify error was handled
        self.assertTrue(
            error.handled or 
            error_id not in self.error_handler.active_errors
        )
        
    def test_multiple_error_handling(self):
        """Test handling of multiple simultaneous errors"""
        error_ids = []
        
        # Create multiple errors of different types
        error_scenarios = [
            (ErrorCategory.RITUAL_INTERRUPTION, ErrorSeverity.HIGH, "Ritual interrupted"),
            (ErrorCategory.DIMENSIONAL_ANOMALY, ErrorSeverity.CRITICAL, "Anomaly detected"),
            (ErrorCategory.MAGICAL_BACKLASH, ErrorSeverity.MEDIUM, "Magical backlash")
        ]
        
        for category, severity, message in error_scenarios:
            error_id = self.error_handler.handle_error(
                category, severity, message, self.test_error_details
            )
            error_ids.append(error_id)
            
        # Verify all errors were handled
        for error_id in error_ids:
            error = self.error_handler.active_errors.get(error_id)
            if error:
                self.assertTrue(error.handled)
                
    def test_error_metrics(self):
        """Test error handling metrics tracking"""
        # Create several errors of the same type
        for _ in range(3):
            self.error_handler.handle_error(
                ErrorCategory.RITUAL_INTERRUPTION,
                ErrorSeverity.MEDIUM,
                "Test error",
                self.test_error_details
            )
            
        metrics = self.error_handler.handler_metrics[ErrorCategory.RITUAL_INTERRUPTION]
        self.assertEqual(metrics.attempts, 3)
        self.assertGreaterEqual(metrics.successes + metrics.failures, 3)

if __name__ == '__main__':
    unittest.main() 