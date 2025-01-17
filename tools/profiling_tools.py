import time
import cProfile
import pstats
import io
import logging
import psutil
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class PerformanceMetrics:
    cpu_usage: float
    memory_usage: float
    function_calls: int
    execution_time: float
    event_count: int
    active_quests: int

class SystemProfiler:
    def __init__(self):
        self.profiler = cProfile.Profile()
        self.metrics_history: List[Dict[str, Any]] = []
        self.current_metrics: Optional[PerformanceMetrics] = None
        self.logger = self._setup_logger()
        self.start_time = time.time()
        self.thresholds = {
            "cpu_warning": 80.0,  # 80% CPU usage
            "memory_warning": 85.0,  # 85% memory usage
            "execution_warning": 0.1  # 100ms per frame
        }
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("SystemProfiler")
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler("logs/profiling.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        logger.addHandler(handler)
        return logger
        
    def start_profiling(self):
        """Start profiling session"""
        self.profiler.enable()
        self.start_time = time.time()
        
    def stop_profiling(self):
        """Stop profiling session and collect metrics"""
        self.profiler.disable()
        
    def collect_metrics(self, event_system=None) -> PerformanceMetrics:
        """Collect current system metrics"""
        process = psutil.Process()
        
        # Collect CPU and memory metrics
        cpu_percent = process.cpu_percent()
        memory_percent = process.memory_percent()
        
        # Get profiler statistics
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
        ps.print_stats()
        
        # Parse profiler output
        stats = s.getvalue()
        function_calls = int(stats.split('function calls')[0].strip())
        
        # Calculate execution time
        execution_time = time.time() - self.start_time
        
        # Get event system metrics if available
        event_count = 0
        active_quests = 0
        if event_system:
            event_count = len(event_system.active_events)
            active_quests = len(event_system.active_quests)
        
        metrics = PerformanceMetrics(
            cpu_usage=cpu_percent,
            memory_usage=memory_percent,
            function_calls=function_calls,
            execution_time=execution_time,
            event_count=event_count,
            active_quests=active_quests
        )
        
        self.current_metrics = metrics
        self.metrics_history.append(self._metrics_to_dict(metrics))
        
        self._check_thresholds(metrics)
        
        return metrics
        
    def _metrics_to_dict(self, metrics: PerformanceMetrics) -> Dict[str, Any]:
        """Convert metrics to dictionary for storage"""
        return {
            "timestamp": time.time(),
            "cpu_usage": metrics.cpu_usage,
            "memory_usage": metrics.memory_usage,
            "function_calls": metrics.function_calls,
            "execution_time": metrics.execution_time,
            "event_count": metrics.event_count,
            "active_quests": metrics.active_quests
        }
        
    def _check_thresholds(self, metrics: PerformanceMetrics):
        """Check if metrics exceed warning thresholds"""
        if metrics.cpu_usage > self.thresholds["cpu_warning"]:
            self.logger.warning(
                f"High CPU usage: {metrics.cpu_usage:.1f}% "
                f"(threshold: {self.thresholds['cpu_warning']}%)"
            )
            
        if metrics.memory_usage > self.thresholds["memory_warning"]:
            self.logger.warning(
                f"High memory usage: {metrics.memory_usage:.1f}% "
                f"(threshold: {self.thresholds['memory_warning']}%)"
            )
            
        if metrics.execution_time > self.thresholds["execution_warning"]:
            self.logger.warning(
                f"High execution time: {metrics.execution_time*1000:.1f}ms "
                f"(threshold: {self.thresholds['execution_warning']*1000}ms)"
            )
            
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report from collected metrics"""
        if not self.metrics_history:
            return {"status": "no_data"}
            
        # Calculate averages
        avg_metrics = defaultdict(float)
        for metric in self.metrics_history:
            for key, value in metric.items():
                if key != "timestamp":
                    avg_metrics[key] += value
                    
        for key in avg_metrics:
            avg_metrics[key] /= len(self.metrics_history)
            
        # Find peaks
        peak_metrics = {
            "cpu_usage": max(m["cpu_usage"] for m in self.metrics_history),
            "memory_usage": max(m["memory_usage"] for m in self.metrics_history),
            "execution_time": max(m["execution_time"] for m in self.metrics_history)
        }
        
        return {
            "averages": dict(avg_metrics),
            "peaks": peak_metrics,
            "samples": len(self.metrics_history),
            "total_time": time.time() - self.metrics_history[0]["timestamp"],
            "current": self._metrics_to_dict(self.current_metrics) if self.current_metrics else None
        }
        
    def analyze_bottlenecks(self) -> List[Dict[str, Any]]:
        """Analyze performance bottlenecks"""
        bottlenecks = []
        
        if not self.metrics_history:
            return bottlenecks
            
        # Analyze CPU spikes
        cpu_threshold = self.thresholds["cpu_warning"]
        cpu_spikes = [
            m for m in self.metrics_history
            if m["cpu_usage"] > cpu_threshold
        ]
        
        if cpu_spikes:
            bottlenecks.append({
                "type": "cpu",
                "severity": "high" if len(cpu_spikes) > len(self.metrics_history) * 0.2 else "medium",
                "occurrences": len(cpu_spikes),
                "average_value": sum(s["cpu_usage"] for s in cpu_spikes) / len(cpu_spikes)
            })
            
        # Analyze memory growth
        if len(self.metrics_history) > 1:
            memory_growth = (
                self.metrics_history[-1]["memory_usage"] -
                self.metrics_history[0]["memory_usage"]
            )
            
            if memory_growth > 10:  # More than 10% growth
                bottlenecks.append({
                    "type": "memory_leak",
                    "severity": "high" if memory_growth > 25 else "medium",
                    "growth_percentage": memory_growth,
                    "duration_hours": (
                        self.metrics_history[-1]["timestamp"] -
                        self.metrics_history[0]["timestamp"]
                    ) / 3600
                })
                
        # Analyze execution time spikes
        time_threshold = self.thresholds["execution_warning"]
        time_spikes = [
            m for m in self.metrics_history
            if m["execution_time"] > time_threshold
        ]
        
        if time_spikes:
            bottlenecks.append({
                "type": "performance",
                "severity": "high" if len(time_spikes) > len(self.metrics_history) * 0.1 else "medium",
                "occurrences": len(time_spikes),
                "average_spike": sum(s["execution_time"] for s in time_spikes) / len(time_spikes)
            })
            
        return bottlenecks
        
    def export_metrics(self, file_path: str):
        """Export collected metrics to file"""
        data = {
            "metrics_history": self.metrics_history,
            "thresholds": self.thresholds,
            "bottlenecks": self.analyze_bottlenecks(),
            "summary": self.get_performance_report()
        }
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            
    def import_metrics(self, file_path: str):
        """Import metrics from file"""
        with open(file_path, "r") as f:
            data = json.load(f)
            
        self.metrics_history = data["metrics_history"]
        self.thresholds = data["thresholds"]
        
class FunctionProfiler:
    """Decorator class for profiling specific functions"""
    def __init__(self, logger=None):
        self.stats = defaultdict(list)
        self.logger = logger or logging.getLogger("FunctionProfiler")
        
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            self.stats[func.__name__].append({
                "timestamp": start_time,
                "execution_time": execution_time,
                "args_count": len(args),
                "kwargs_count": len(kwargs)
            })
            
            if execution_time > 0.1:  # Log slow function calls
                self.logger.warning(
                    f"Slow function call: {func.__name__} "
                    f"took {execution_time*1000:.1f}ms"
                )
                
            return result
            
        return wrapper
        
    def get_stats(self, function_name: Optional[str] = None) -> Dict[str, Any]:
        """Get profiling statistics for a function or all functions"""
        if function_name:
            if function_name not in self.stats:
                return {}
                
            calls = self.stats[function_name]
            return {
                "call_count": len(calls),
                "average_time": sum(c["execution_time"] for c in calls) / len(calls),
                "min_time": min(c["execution_time"] for c in calls),
                "max_time": max(c["execution_time"] for c in calls),
                "total_time": sum(c["execution_time"] for c in calls)
            }
            
        return {
            name: self.get_stats(name)
            for name in self.stats
        } 