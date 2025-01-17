import time
import psutil
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from collections import deque
import threading
import logging

class MetricType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    FPS = "fps"
    LOAD_TIME = "load_time"
    RESPONSE_TIME = "response_time"

@dataclass
class PerformanceMetric:
    metric_type: MetricType
    value: float
    timestamp: float
    context: Dict[str, Any]

class PerformanceMonitor:
    def __init__(self):
        self.metrics_history: Dict[MetricType, deque] = {
            metric_type: deque(maxlen=1000)
            for metric_type in MetricType
        }
        
        self.thresholds = {
            MetricType.CPU: 80.0,  # 80% CPU usage
            MetricType.MEMORY: 85.0,  # 85% memory usage
            MetricType.FPS: 30.0,  # minimum 30 FPS
            MetricType.LOAD_TIME: 2.0,  # 2 seconds max load time
            MetricType.RESPONSE_TIME: 0.1  # 100ms max response time
        }
        
        self.monitoring_active = False
        self.monitor_thread = None
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for performance monitoring"""
        logger = logging.getLogger("PerformanceMonitor")
        logger.setLevel(logging.DEBUG)
        
        # File handler
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        fh = logging.FileHandler("logs/performance.log")
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger

    def start_monitoring(self):
        """Start continuous performance monitoring"""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stop continuous performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()

    def _monitor_loop(self):
        """Continuous monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                self.collect_system_metrics()
                
                # Check for performance issues
                self.check_performance_thresholds()
                
                # Sleep for a short duration
                time.sleep(1.0)
                
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {str(e)}")

    def collect_system_metrics(self):
        """Collect current system performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.record_metric(MetricType.CPU, cpu_percent)
            
            # Memory usage
            memory = psutil.Process(os.getpid()).memory_percent()
            self.record_metric(MetricType.MEMORY, memory)
            
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {str(e)}")

    def record_metric(
        self,
        metric_type: MetricType,
        value: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """Record a performance metric"""
        metric = PerformanceMetric(
            metric_type=metric_type,
            value=value,
            timestamp=time.time(),
            context=context or {}
        )
        
        self.metrics_history[metric_type].append(metric)
        
        # Log if exceeding threshold
        threshold = self.thresholds.get(metric_type)
        if threshold is not None:
            if (metric_type in [MetricType.CPU, MetricType.MEMORY] and value > threshold) or \
               (metric_type in [MetricType.FPS] and value < threshold):
                self.logger.warning(
                    f"{metric_type.value} threshold exceeded: {value:.2f} (threshold: {threshold})"
                )

    def get_metrics(
        self,
        metric_type: Optional[MetricType] = None,
        time_range: Optional[float] = None
    ) -> List[PerformanceMetric]:
        """Get recorded metrics with optional filtering"""
        current_time = time.time()
        
        if metric_type:
            metrics = list(self.metrics_history[metric_type])
        else:
            metrics = [
                metric
                for metric_list in self.metrics_history.values()
                for metric in metric_list
            ]
            
        if time_range:
            metrics = [
                metric for metric in metrics
                if current_time - metric.timestamp <= time_range
            ]
            
        return sorted(metrics, key=lambda x: x.timestamp)

    def check_performance_thresholds(self):
        """Check if any metrics are exceeding thresholds"""
        for metric_type in MetricType:
            if not self.metrics_history[metric_type]:
                continue
                
            recent_metrics = list(self.metrics_history[metric_type])[-10:]
            avg_value = sum(m.value for m in recent_metrics) / len(recent_metrics)
            
            threshold = self.thresholds.get(metric_type)
            if threshold is not None:
                if (metric_type in [MetricType.CPU, MetricType.MEMORY] and avg_value > threshold) or \
                   (metric_type in [MetricType.FPS] and avg_value < threshold):
                    self._handle_threshold_exceeded(metric_type, avg_value, threshold)

    def _handle_threshold_exceeded(
        self,
        metric_type: MetricType,
        value: float,
        threshold: float
    ):
        """Handle a threshold being exceeded"""
        self.logger.warning(
            f"Performance threshold exceeded for {metric_type.value}: "
            f"{value:.2f} (threshold: {threshold})"
        )
        
        # Implement specific handling for different metric types
        if metric_type == MetricType.MEMORY:
            self._handle_high_memory()
        elif metric_type == MetricType.CPU:
            self._handle_high_cpu()
        elif metric_type == MetricType.FPS:
            self._handle_low_fps()

    def _handle_high_memory(self):
        """Handle high memory usage"""
        try:
            # Trigger garbage collection
            import gc
            gc.collect()
            
            # Log memory intensive operations
            process = psutil.Process(os.getpid())
            self.logger.info("Memory intensive operations:")
            for thread in process.threads():
                self.logger.info(f"Thread {thread.id}: CPU: {thread.cpu_times()}")
                
        except Exception as e:
            self.logger.error(f"Error handling high memory: {str(e)}")

    def _handle_high_cpu(self):
        """Handle high CPU usage"""
        try:
            process = psutil.Process(os.getpid())
            
            # Log CPU intensive operations
            self.logger.info("CPU intensive operations:")
            for thread in process.threads():
                self.logger.info(f"Thread {thread.id}: CPU: {thread.cpu_times()}")
                
        except Exception as e:
            self.logger.error(f"Error handling high CPU: {str(e)}")

    def _handle_low_fps(self):
        """Handle low FPS"""
        self.logger.warning("Low FPS detected - consider reducing visual effects")

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report"""
        report = {
            "timestamp": time.time(),
            "metrics": {}
        }
        
        for metric_type in MetricType:
            metrics = self.get_metrics(metric_type, time_range=300)  # Last 5 minutes
            if metrics:
                values = [m.value for m in metrics]
                report["metrics"][metric_type.value] = {
                    "current": values[-1],
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values)
                }
                
        return report

    def export_metrics(self, file_path: str) -> bool:
        """Export performance metrics to file"""
        try:
            metrics_data = {
                metric_type.value: [
                    {
                        "value": metric.value,
                        "timestamp": metric.timestamp,
                        "context": metric.context
                    }
                    for metric in metrics
                ]
                for metric_type, metrics in self.metrics_history.items()
            }
            
            with open(file_path, "w") as f:
                json.dump(metrics_data, f, indent=4)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {str(e)}")
            return False

    def import_metrics(self, file_path: str) -> bool:
        """Import performance metrics from file"""
        try:
            with open(file_path, "r") as f:
                metrics_data = json.load(f)
                
            for metric_type_str, metrics in metrics_data.items():
                try:
                    metric_type = MetricType(metric_type_str)
                    for metric_data in metrics:
                        self.record_metric(
                            metric_type,
                            metric_data["value"],
                            metric_data.get("context")
                        )
                except ValueError:
                    continue
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error importing metrics: {str(e)}")
            return False

    def clear_metrics(self, metric_type: Optional[MetricType] = None):
        """Clear recorded metrics"""
        if metric_type:
            self.metrics_history[metric_type].clear()
        else:
            for metric_queue in self.metrics_history.values():
                metric_queue.clear() 