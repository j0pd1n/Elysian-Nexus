import logging
import logging.handlers
import os
import time
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from enum import Enum, auto
from datetime import datetime

class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

class LogCategory(Enum):
    SYSTEM = auto()
    GAMEPLAY = auto()
    COMBAT = auto()
    DIMENSIONAL = auto()
    PERFORMANCE = auto()
    NETWORK = auto()
    AI = auto()

@dataclass
class GameEvent:
    """Represents a game event for logging"""
    timestamp: float
    category: LogCategory
    event_type: str
    details: Dict[str, Any]
    player_id: Optional[str] = None
    dimension: Optional[str] = None
    position: Optional[Dict[str, float]] = None

class GameLogger:
    """Manages game logging across different categories"""
    
    def __init__(self, log_directory: str = "logs"):
        self.log_directory = log_directory
        os.makedirs(log_directory, exist_ok=True)
        
        # Initialize different log files
        self.loggers = {}
        self._setup_loggers()
        
        # Performance monitoring
        self.performance_metrics = {}
        self.last_performance_update = time.time()
        
    def _setup_loggers(self) -> None:
        """Set up different loggers for each category"""
        for category in LogCategory:
            logger = logging.getLogger(category.name)
            logger.setLevel(logging.DEBUG)
            
            # File handler
            file_handler = logging.handlers.RotatingFileHandler(
                os.path.join(self.log_directory, f"{category.name.lower()}.log"),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(file_handler)
            
            # Console handler for important messages
            if category in {LogCategory.SYSTEM, LogCategory.ERROR}:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)
                console_handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))
                logger.addHandler(console_handler)
            
            self.loggers[category] = logger
            
    def log_event(
        self,
        category: LogCategory,
        event_type: str,
        details: Dict[str, Any],
        level: LogLevel = LogLevel.INFO,
        player_id: Optional[str] = None,
        dimension: Optional[str] = None,
        position: Optional[Dict[str, float]] = None
    ) -> None:
        """Log a game event"""
        event = GameEvent(
            timestamp=time.time(),
            category=category,
            event_type=event_type,
            details=details,
            player_id=player_id,
            dimension=dimension,
            position=position
        )
        
        # Convert to JSON-serializable format
        event_dict = asdict(event)
        event_json = json.dumps(event_dict)
        
        # Log to appropriate category
        logger = self.loggers[category]
        log_method = getattr(logger, level.name.lower())
        log_method(event_json)
        
        # Special handling for critical events
        if level == LogLevel.CRITICAL:
            self._handle_critical_event(event)
            
    def start_performance_monitoring(self, metric_name: str) -> None:
        """Start monitoring performance for a metric"""
        self.performance_metrics[metric_name] = {
            'start_time': time.time(),
            'samples': [],
            'min': float('inf'),
            'max': float('-inf'),
            'total': 0.0,
            'count': 0
        }
        
    def end_performance_monitoring(self, metric_name: str) -> None:
        """End monitoring performance for a metric"""
        if metric_name not in self.performance_metrics:
            return
            
        end_time = time.time()
        duration = end_time - self.performance_metrics[metric_name]['start_time']
        
        metrics = self.performance_metrics[metric_name]
        metrics['samples'].append(duration)
        metrics['min'] = min(metrics['min'], duration)
        metrics['max'] = max(metrics['max'], duration)
        metrics['total'] += duration
        metrics['count'] += 1
        
        # Log if significant time has passed
        current_time = time.time()
        if current_time - self.last_performance_update >= 60:  # Log every minute
            self._log_performance_metrics()
            self.last_performance_update = current_time
            
    def _log_performance_metrics(self) -> None:
        """Log current performance metrics"""
        for metric_name, metrics in self.performance_metrics.items():
            if metrics['count'] == 0:
                continue
                
            avg_duration = metrics['total'] / metrics['count']
            self.log_event(
                category=LogCategory.PERFORMANCE,
                event_type='performance_metrics',
                details={
                    'metric_name': metric_name,
                    'average_duration': avg_duration,
                    'min_duration': metrics['min'],
                    'max_duration': metrics['max'],
                    'sample_count': metrics['count']
                }
            )
            
            # Reset metrics
            metrics['samples'] = []
            metrics['min'] = float('inf')
            metrics['max'] = float('-inf')
            metrics['total'] = 0.0
            metrics['count'] = 0
            
    def _handle_critical_event(self, event: GameEvent) -> None:
        """Handle critical events"""
        # Log to separate critical events file
        critical_log_path = os.path.join(self.log_directory, 'critical_events.log')
        with open(critical_log_path, 'a') as f:
            f.write(f"{datetime.fromtimestamp(event.timestamp).isoformat()} - ")
            f.write(f"Category: {event.category.name} - ")
            f.write(f"Type: {event.event_type}\n")
            f.write(f"Details: {json.dumps(event.details, indent=2)}\n")
            f.write("-" * 80 + "\n")
            
        # Notify system administrators (placeholder)
        print(f"CRITICAL EVENT: {event.event_type} in {event.category.name}")
        
    def cleanup_old_logs(self, days_to_keep: int = 30) -> None:
        """Clean up old log files"""
        current_time = time.time()
        for filename in os.listdir(self.log_directory):
            file_path = os.path.join(self.log_directory, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > days_to_keep * 86400:  # Convert days to seconds
                    try:
                        os.remove(file_path)
                    except OSError:
                        pass 