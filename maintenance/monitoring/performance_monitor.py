import time
import psutil
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from threading import Thread, Lock
import json
import os
from datetime import datetime

@dataclass
class MetricThreshold:
    threshold: float
    warning_threshold: float
    critical_threshold: float

@dataclass
class GameMetric:
    target: float
    warning: float
    critical: float

class PerformanceMonitor:
    def __init__(self):
        self.system_metrics = {
            'cpu_usage': MetricThreshold(0.80, 0.70, 0.90),
            'memory_usage': MetricThreshold(0.85, 0.75, 0.95),
            'io_operations': MetricThreshold(1000, 800, 1200),
            'thread_count': MetricThreshold(100, 80, 120),
            'disk_usage': MetricThreshold(0.90, 0.80, 0.95),
            'network_latency': MetricThreshold(100, 50, 150)  # in milliseconds
        }
        
        self.game_metrics = {
            'frame_time': GameMetric(0.033, 0.040, 0.050),
            'update_time': GameMetric(0.016, 0.020, 0.030),
            'load_time': GameMetric(2.0, 3.0, 5.0),
            'magic_system_load': GameMetric(0.7, 0.8, 0.9),
            'combat_system_load': GameMetric(0.7, 0.8, 0.9),
            'world_system_load': GameMetric(0.7, 0.8, 0.9),
            'npc_system_load': GameMetric(0.7, 0.8, 0.9),
            'event_queue_size': GameMetric(100, 200, 300),
            'active_entities': GameMetric(1000, 2000, 3000),
            'memory_pool_usage': GameMetric(0.7, 0.8, 0.9)
        }
        
        self.monitoring_active = False
        self.monitoring_thread = None
        self.monitoring_lock = Lock()
        self.metrics_history: List[Dict[str, Any]] = []
        self.alert_callbacks = []
        
        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        log_dir = "logs/performance"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            filename=f"{log_dir}/performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def start_monitoring(self, interval: float = 1.0):
        """Start the performance monitoring thread."""
        with self.monitoring_lock:
            if not self.monitoring_active:
                self.monitoring_active = True
                self.monitoring_thread = Thread(target=self._monitoring_loop, args=(interval,))
                self.monitoring_thread.daemon = True
                self.monitoring_thread.start()
                logging.info("Performance monitoring started")

    def stop_monitoring(self):
        """Stop the performance monitoring thread."""
        with self.monitoring_lock:
            if self.monitoring_active:
                self.monitoring_active = False
                if self.monitoring_thread:
                    self.monitoring_thread.join()
                logging.info("Performance monitoring stopped")

    def _monitoring_loop(self, interval: float):
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                metrics = self._collect_metrics()
                self._analyze_metrics(metrics)
                self._store_metrics(metrics)
                time.sleep(interval)
            except Exception as e:
                logging.error(f"Error in monitoring loop: {str(e)}")

    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect current system and game metrics."""
        metrics = {
            'timestamp': time.time(),
            'system': {
                'cpu_usage': psutil.cpu_percent() / 100.0,
                'memory_usage': psutil.virtual_memory().percent / 100.0,
                'io_operations': len(psutil.Process().open_files()),
                'thread_count': psutil.Process().num_threads(),
                'disk_usage': psutil.disk_usage('/').percent / 100.0,
                'network_latency': self._measure_network_latency()
            },
            'game': {
                'frame_time': self._measure_frame_time(),
                'update_time': self._measure_update_time(),
                'load_time': self._measure_load_time(),
                'magic_system_load': self._measure_magic_system_load(),
                'combat_system_load': self._measure_combat_system_load(),
                'world_system_load': self._measure_world_system_load(),
                'npc_system_load': self._measure_npc_system_load(),
                'event_queue_size': self._measure_event_queue_size(),
                'active_entities': self._measure_active_entities(),
                'memory_pool_usage': self._measure_memory_pool_usage()
            },
            'subsystems': {
                'magic': self._collect_magic_metrics(),
                'combat': self._collect_combat_metrics(),
                'world': self._collect_world_metrics()
            }
        }
        return metrics

    def _analyze_metrics(self, metrics: Dict[str, Any]):
        """Analyze metrics and trigger alerts if necessary."""
        # Check system metrics
        for metric_name, value in metrics['system'].items():
            threshold = self.system_metrics.get(metric_name)
            if threshold:
                if value >= threshold.critical_threshold:
                    self._trigger_alert('CRITICAL', metric_name, value)
                elif value >= threshold.warning_threshold:
                    self._trigger_alert('WARNING', metric_name, value)

        # Check game metrics
        for metric_name, value in metrics['game'].items():
            threshold = self.game_metrics.get(metric_name)
            if threshold:
                if value >= threshold.critical:
                    self._trigger_alert('CRITICAL', metric_name, value)
                elif value >= threshold.warning:
                    self._trigger_alert('WARNING', metric_name, value)

    def _trigger_alert(self, level: str, metric_name: str, value: float):
        """Trigger an alert for a metric exceeding its threshold."""
        message = f"{level} Alert: {metric_name} = {value}"
        logging.warning(message)
        
        # Execute alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(level, metric_name, value)
            except Exception as e:
                logging.error(f"Error in alert callback: {str(e)}")

    def _store_metrics(self, metrics: Dict[str, Any]):
        """Store metrics in history and potentially persist to disk."""
        self.metrics_history.append(metrics)
        
        # Keep only last hour of metrics (assuming 1-second intervals)
        if len(self.metrics_history) > 3600:
            self.metrics_history = self.metrics_history[-3600:]
            
        # Periodically save metrics to disk
        if len(self.metrics_history) % 300 == 0:  # Every 5 minutes
            self._save_metrics_to_disk()

    def _save_metrics_to_disk(self):
        """Save current metrics to disk."""
        try:
            metrics_dir = "logs/metrics"
            os.makedirs(metrics_dir, exist_ok=True)
            
            filename = f"{metrics_dir}/metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.metrics_history[-300:], f)  # Save last 5 minutes
        except Exception as e:
            logging.error(f"Error saving metrics to disk: {str(e)}")

    def add_alert_callback(self, callback):
        """Add a callback function to be called when alerts are triggered."""
        self.alert_callbacks.append(callback)

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get the most recent metrics."""
        if self.metrics_history:
            return self.metrics_history[-1]
        return {}

    def get_metrics_history(self, duration: int = 3600) -> List[Dict[str, Any]]:
        """Get metrics history for the specified duration (in seconds)."""
        return self.metrics_history[-duration:]

    # Measurement methods (to be implemented based on game engine)
    def _measure_frame_time(self) -> float:
        """Measure the current frame time."""
        # TODO: Implement actual frame time measurement
        return 0.016  # Placeholder

    def _measure_update_time(self) -> float:
        """Measure the current update time."""
        # TODO: Implement actual update time measurement
        return 0.008  # Placeholder

    def _measure_load_time(self) -> float:
        """Measure the current load time."""
        # TODO: Implement actual load time measurement
        return 1.0  # Placeholder

    def _measure_network_latency(self) -> float:
        """Measure current network latency."""
        # TODO: Implement actual network latency measurement
        return 20.0  # Placeholder: 20ms

    def _measure_magic_system_load(self) -> float:
        """Measure magical system load."""
        # TODO: Implement actual magic system load measurement
        return 0.5  # Placeholder: 50% load

    def _measure_combat_system_load(self) -> float:
        """Measure combat system load."""
        # TODO: Implement actual combat system load measurement
        return 0.4  # Placeholder: 40% load

    def _measure_world_system_load(self) -> float:
        """Measure world system load."""
        # TODO: Implement actual world system load measurement
        return 0.6  # Placeholder: 60% load

    def _measure_npc_system_load(self) -> float:
        """Measure NPC system load."""
        # TODO: Implement actual NPC system load measurement
        return 0.3  # Placeholder: 30% load

    def _measure_event_queue_size(self) -> int:
        """Measure current event queue size."""
        # TODO: Implement actual event queue size measurement
        return 50  # Placeholder: 50 events

    def _measure_active_entities(self) -> int:
        """Measure number of active entities."""
        # TODO: Implement actual active entities measurement
        return 500  # Placeholder: 500 entities

    def _measure_memory_pool_usage(self) -> float:
        """Measure memory pool usage.
        
        Returns:
            float: Memory pool usage as a ratio between 0 and 1
        """
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            # Calculate memory pool usage based on RSS (Resident Set Size)
            # and available system memory
            total_memory = psutil.virtual_memory().total
            memory_pool_usage = memory_info.rss / total_memory
            
            # Ensure the value is between 0 and 1
            return min(max(memory_pool_usage, 0.0), 1.0)
        except Exception as e:
            logging.error(f"Error measuring memory pool usage: {str(e)}")
            return 0.0  # Return 0 on error

    def _collect_magic_metrics(self) -> Dict[str, Any]:
        """Collect detailed magic system metrics."""
        return {
            'active_spells': 25,  # Placeholder
            'magical_energy_level': 0.7,
            'spell_cache_size': 100,
            'enchantment_count': 50
        }

    def _collect_combat_metrics(self) -> Dict[str, Any]:
        """Collect detailed combat system metrics."""
        return {
            'active_battles': 5,  # Placeholder
            'entities_in_combat': 20,
            'ability_cache_hits': 0.8,
            'damage_calculations_per_second': 100
        }

    def _collect_world_metrics(self) -> Dict[str, Any]:
        """Collect detailed world system metrics."""
        return {
            'active_regions': 10,  # Placeholder
            'loaded_npcs': 100,
            'active_quests': 25,
            'weather_calculations_per_second': 10
        }

# Example usage
if __name__ == "__main__":
    def alert_callback(level: str, metric_name: str, value: float):
        print(f"Alert: {level} - {metric_name} = {value}")

    monitor = PerformanceMonitor()
    monitor.add_alert_callback(alert_callback)
    monitor.start_monitoring()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop_monitoring() 