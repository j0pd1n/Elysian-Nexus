from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Any

class NotificationPriority(Enum):
    """Enum defining notification priority levels"""
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class NotificationChannel(ABC):
    """Abstract base class for notification channels"""
    
    @abstractmethod
    def send(self, message: str, priority: NotificationPriority):
        """Send a notification message with the specified priority
        
        Args:
            message (str): The notification message to send
            priority (NotificationPriority): The priority level of the notification
        """
        pass 