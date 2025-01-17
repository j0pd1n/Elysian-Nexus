import unittest
import os
import json
import time
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from typing import Dict, Any

# Import maintenance systems
from maintenance.monitoring.performance_monitor import PerformanceMonitor
from maintenance.monitoring.notification_system import NotificationSystem, NotificationPriority
from maintenance.recovery.recovery_system import RecoverySystem, SystemState

class TestMaintenanceSystems(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Create test directories
        os.makedirs("logs/performance", exist_ok=True)
        os.makedirs("logs/notifications", exist_ok=True)
        os.makedirs("logs/recovery", exist_ok=True)
        os.makedirs("config", exist_ok=True)
        
        # Create test notification config
        self.notification_config = {
            'email': {
                'enabled': False
            },
            'discord': {
                'enabled': False
            },
            'slack': {
                'enabled': False
            },
            'cooldown': {
                'low': 5,      # 5 seconds for testing
                'medium': 3,   # 3 seconds for testing
                'high': 1,     # 1 second for testing
                'critical': 0  # No cooldown
            }
        }
        
        with open("config/notifications.json", "w") as f:
            json.dump(self.notification_config, f)
        
        # Initialize systems
        self.performance_monitor = PerformanceMonitor()
        self.notification_system = NotificationSystem()
        self.recovery_system = RecoverySystem()

    def tearDown(self):
        """Clean up after tests."""
        self.performance_monitor.stop_monitoring()

    def test_performance_monitoring_integration(self):
        """Test performance monitoring integration."""
        # Mock alert callback
        alerts = []
        def alert_callback(level: str, metric_name: str, value: float):
            alerts.append((level, metric_name, value))

        # Add callback and start monitoring
        self.performance_monitor.add_alert_callback(alert_callback)
        self.performance_monitor.start_monitoring(interval=0.1)

        # Wait for some metrics to be collected
        time.sleep(1)

        # Stop monitoring
        self.performance_monitor.stop_monitoring()

        # Verify metrics were collected
        metrics = self.performance_monitor.get_metrics_history()
        self.assertGreater(len(metrics), 0)
        
        # Verify metric structure
        latest_metrics = metrics[-1]
        self.assertIn('timestamp', latest_metrics)
        self.assertIn('system', latest_metrics)
        self.assertIn('game', latest_metrics)
        self.assertIn('subsystems', latest_metrics)

    def test_notification_system_integration(self):
        """Test notification system integration."""
        # Mock notification channels
        mock_channel = MagicMock()
        self.notification_system.channels['test'] = mock_channel

        # Send notifications of different priorities
        self.notification_system.notify("Test low priority", NotificationPriority.LOW)
        self.notification_system.notify("Test medium priority", NotificationPriority.MEDIUM)
        self.notification_system.notify("Test high priority", NotificationPriority.HIGH)
        self.notification_system.notify("Test critical priority", NotificationPriority.CRITICAL)

        # Verify notifications were sent
        self.assertEqual(mock_channel.send.call_count, 4)
        
        # Verify cooldown functionality
        self.notification_system.notify("Test cooldown", NotificationPriority.LOW)
        self.assertEqual(mock_channel.send.call_count, 4)  # Should not increase due to cooldown

    def test_recovery_system_integration(self):
        """Test recovery system integration."""
        # Mock recovery handlers
        handlers = {
            SystemState.WARNING: MagicMock(),
            SystemState.CRITICAL: MagicMock(),
            SystemState.EMERGENCY: MagicMock()
        }

        # Register handlers
        for state, handler in handlers.items():
            self.recovery_system.register_recovery_handler(state, handler)

        # Simulate state changes
        self.recovery_system.set_system_state(SystemState.WARNING)
        self.recovery_system.set_system_state(SystemState.CRITICAL)
        self.recovery_system.set_system_state(SystemState.EMERGENCY)

        # Verify handlers were called
        handlers[SystemState.WARNING].assert_called_once()
        handlers[SystemState.CRITICAL].assert_called_once()
        handlers[SystemState.EMERGENCY].assert_called_once()

    def test_full_system_integration(self):
        """Test full integration between all systems."""
        # Mock notification channel
        mock_notifier = MagicMock()
        self.notification_system.channels['test'] = mock_notifier

        # Create performance alert handler
        def performance_alert_handler(level: str, metric_name: str, value: float):
            if level == "CRITICAL":
                self.recovery_system.set_system_state(SystemState.CRITICAL)
                self.notification_system.notify(
                    f"Critical performance alert: {metric_name} = {value}",
                    NotificationPriority.CRITICAL
                )

        # Setup mock system metrics
        def mock_collect_metrics() -> Dict[str, Any]:
            return {
                'timestamp': time.time(),
                'system': {
                    'cpu_usage': 0.95,  # Critical level
                    'memory_usage': 0.90,  # Critical level
                    'io_operations': 100,
                    'thread_count': 50
                },
                'game': {
                    'frame_time': 0.016,
                    'update_time': 0.008,
                    'load_time': 1.0
                }
            }

        # Mock recovery handler
        recovery_handler = MagicMock()
        self.recovery_system.register_recovery_handler(SystemState.CRITICAL, recovery_handler)

        # Start monitoring with mocked metrics
        with patch.object(self.performance_monitor, '_collect_metrics', mock_collect_metrics):
            self.performance_monitor.add_alert_callback(performance_alert_handler)
            self.performance_monitor.start_monitoring(interval=0.1)
            
            # Wait for alerts to be processed
            time.sleep(1)
            
            self.performance_monitor.stop_monitoring()

        # Verify system integration
        recovery_handler.assert_called()  # Recovery handler was triggered
        self.assertGreater(mock_notifier.send.call_count, 0)  # Notifications were sent

    def test_metric_persistence(self):
        """Test metric persistence functionality."""
        # Start monitoring
        self.performance_monitor.start_monitoring(interval=0.1)
        
        # Wait for metrics to be collected
        time.sleep(1)
        
        # Stop monitoring
        self.performance_monitor.stop_monitoring()
        
        # Verify metric files were created
        metric_files = os.listdir("logs/metrics")
        self.assertGreater(len(metric_files), 0)
        
        # Verify metric file content
        latest_file = sorted(metric_files)[-1]
        with open(f"logs/metrics/{latest_file}", 'r') as f:
            metrics = json.load(f)
            self.assertIsInstance(metrics, list)
            self.assertGreater(len(metrics), 0)

    def test_notification_history(self):
        """Test notification history functionality."""
        # Send multiple notifications
        messages = [
            ("Test message 1", NotificationPriority.LOW),
            ("Test message 2", NotificationPriority.MEDIUM),
            ("Test message 3", NotificationPriority.HIGH),
            ("Test message 4", NotificationPriority.CRITICAL)
        ]
        
        for message, priority in messages:
            self.notification_system.notify(message, priority)
        
        # Verify history
        self.assertEqual(len(self.notification_system.notification_history), len(messages))
        
        # Verify history persistence
        history_files = os.listdir("logs/notification_history")
        self.assertGreater(len(history_files), 0)

    def test_recovery_state_logging(self):
        """Test recovery state change logging."""
        # Trigger state changes
        states = [
            SystemState.WARNING,
            SystemState.CRITICAL,
            SystemState.EMERGENCY,
            SystemState.NORMAL
        ]
        
        for state in states:
            self.recovery_system.set_system_state(state)
        
        # Verify state change logs
        log_files = os.listdir("logs/state_changes")
        self.assertGreater(len(log_files), 0)
        
        # Verify log content
        latest_file = sorted(log_files)[-1]
        with open(f"logs/state_changes/{latest_file}", 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), len(states))

if __name__ == '__main__':
    unittest.main() 