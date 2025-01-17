import time
import psutil
import threading
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum, auto
from collections import deque
from src.infrastructure.logging_system import GameLogger, LogCategory, LogLevel

class MetricType(Enum):
    CPU_USAGE = auto()
    MEMORY_USAGE = auto()
    FPS = auto()
    FRAME_TIME = auto()
    PHYSICS_TIME = auto()
    RENDER_TIME = auto()
    AI_TIME = auto()
    NETWORK_LATENCY = auto()
    DIMENSION_TRANSITIONS = auto()
    ABILITY_CALCULATIONS = auto()

@dataclass
class PerformanceMetric:
    """Represents a single performance metric"""
    type: MetricType
    value: float
    timestamp: float
    details: Optional[Dict[str, float]] = None

class PerformanceThreshold:
    """Defines thresholds for performance metrics"""
    def __init__(
        self,
        warning_threshold: float,
        critical_threshold: float,
        metric_type: MetricType
    ):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.metric_type = metric_type
        self.last_warning_time: Optional[float] = None
        self.warning_cooldown = 60.0  # Seconds between warnings

class PerformanceMonitor:
    """Monitors and analyzes game performance metrics"""
    
    def __init__(
        self,
        logger: GameLogger,
        history_size: int = 1000,
        update_interval: float = 1.0
    ):
        self.logger = logger
        self.history_size = history_size
        self.update_interval = update_interval
        
        # Initialize metric histories
        self.metric_histories: Dict[MetricType, deque[PerformanceMetric]] = {
            metric_type: deque(maxlen=history_size)
            for metric_type in MetricType
        }
        
        # Initialize thresholds
        self.thresholds = self._initialize_thresholds()
        
        # Performance monitoring state
        self.frame_count = 0
        self.last_frame_time = time.time()
        self.last_update_time = time.time()
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Resource monitoring
        self.process = psutil.Process()
        
    def _initialize_thresholds(self) -> Dict[MetricType, PerformanceThreshold]:
        """Initialize performance thresholds"""
        return {
            MetricType.CPU_USAGE: PerformanceThreshold(70.0, 90.0, MetricType.CPU_USAGE),
            MetricType.MEMORY_USAGE: PerformanceThreshold(80.0, 95.0, MetricType.MEMORY_USAGE),
            MetricType.FPS: PerformanceThreshold(30.0, 20.0, MetricType.FPS),
            MetricType.FRAME_TIME: PerformanceThreshold(33.3, 50.0, MetricType.FRAME_TIME),
            MetricType.PHYSICS_TIME: PerformanceThreshold(10.0, 16.0, MetricType.PHYSICS_TIME),
            MetricType.RENDER_TIME: PerformanceThreshold(16.0, 25.0, MetricType.RENDER_TIME),
            MetricType.AI_TIME: PerformanceThreshold(8.0, 12.0, MetricType.AI_TIME),
            MetricType.NETWORK_LATENCY: PerformanceThreshold(100.0, 200.0, MetricType.NETWORK_LATENCY)
        }
        
    def start_monitoring(self) -> None:
        """Start performance monitoring"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitor_thread.start()
        
    def stop_monitoring(self) -> None:
        """Stop performance monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
            
    def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while self.is_monitoring:
            current_time = time.time()
            if current_time - self.last_update_time >= self.update_interval:
                self._update_system_metrics()
                self.last_update_time = current_time
            time.sleep(0.1)  # Prevent busy waiting
            
    def _update_system_metrics(self) -> None:
        """Update system performance metrics"""
        # CPU usage
        cpu_percent = self.process.cpu_percent()
        self.record_metric(MetricType.CPU_USAGE, cpu_percent)
        
        # Memory usage
        memory_info = self.process.memory_info()
        memory_percent = memory_info.rss / psutil.virtual_memory().total * 100
        self.record_metric(MetricType.MEMORY_USAGE, memory_percent)
        
        # FPS calculation
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        if elapsed > 0:
            fps = self.frame_count / elapsed
            self.record_metric(MetricType.FPS, fps)
            self.frame_count = 0
            self.last_frame_time = current_time
            
    def record_metric(
        self,
        metric_type: MetricType,
        value: float,
        details: Optional[Dict[str, float]] = None
    ) -> None:
        """Record a performance metric"""
        metric = PerformanceMetric(
            type=metric_type,
            value=value,
            timestamp=time.time(),
            details=details
        )
        
        self.metric_histories[metric_type].append(metric)
        self._check_threshold(metric)
        
    def _check_threshold(self, metric: PerformanceMetric) -> None:
        """Check if metric exceeds thresholds"""
        if metric.type not in self.thresholds:
            return
            
        threshold = self.thresholds[metric.type]
        current_time = time.time()
        
        # Skip if on warning cooldown
        if (threshold.last_warning_time and
            current_time - threshold.last_warning_time < threshold.warning_cooldown):
            return
            
        if metric.value >= threshold.critical_threshold:
            self.logger.log_event(
                category=LogCategory.PERFORMANCE,
                event_type='performance_critical',
                details={
                    'metric_type': metric.type.name,
                    'value': metric.value,
                    'threshold': threshold.critical_threshold,
                    'details': metric.details
                },
                level=LogLevel.CRITICAL
            )
            threshold.last_warning_time = current_time
        elif metric.value >= threshold.warning_threshold:
            self.logger.log_event(
                category=LogCategory.PERFORMANCE,
                event_type='performance_warning',
                details={
                    'metric_type': metric.type.name,
                    'value': metric.value,
                    'threshold': threshold.warning_threshold,
                    'details': metric.details
                },
                level=LogLevel.WARNING
            )
            threshold.last_warning_time = current_time
            
    def get_metric_statistics(
        self,
        metric_type: MetricType,
        time_window: Optional[float] = None
    ) -> Dict[str, float]:
        """Get statistics for a metric type"""
        metrics = list(self.metric_histories[metric_type])
        if not metrics:
            return {
                'min': 0.0,
                'max': 0.0,
                'avg': 0.0,
                'current': 0.0
            }
            
        if time_window:
            current_time = time.time()
            metrics = [
                m for m in metrics
                if current_time - m.timestamp <= time_window
            ]
            
        values = [m.value for m in metrics]
        return {
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'current': metrics[-1].value if metrics else 0.0
        }
        
    def get_performance_report(self) -> Dict[str, Dict[str, float]]:
        """Generate comprehensive performance report"""
        report = {}
        for metric_type in MetricType:
            report[metric_type.name] = self.get_metric_statistics(
                metric_type,
                time_window=300.0  # Last 5 minutes
            )
        return report
        
    def frame_update(self, frame_time: float) -> None:
        """Update frame-related metrics"""
        self.frame_count += 1
        self.record_metric(MetricType.FRAME_TIME, frame_time * 1000.0)  # Convert to ms
        
    def record_timing(
        self,
        metric_type: MetricType,
        start_time: float,
        end_time: float,
        details: Optional[Dict[str, float]] = None
    ) -> None:
        """Record timing for a specific operation"""
        duration = (end_time - start_time) * 1000.0  # Convert to ms
        self.record_metric(metric_type, duration, details) 