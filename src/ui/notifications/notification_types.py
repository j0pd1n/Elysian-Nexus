from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..core.types import UIElement, UIState

class NotificationType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    QUEST = "quest"
    ACHIEVEMENT = "achievement"

class NotificationPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class Notification(UIElement):
    def __init__(self,
                 id: str,
                 message: str,
                 notification_type: NotificationType = NotificationType.INFO,
                 priority: NotificationPriority = NotificationPriority.NORMAL,
                 duration: Optional[float] = None,  # Duration in seconds, None for persistent
                 icon: Optional[str] = None,
                 actions: Optional[List[Dict[str, Any]]] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            id=id,
            element_type="notification",
            state=UIState.ACTIVE,
            properties={
                "message": message,
                "type": notification_type,
                "priority": priority,
                "duration": duration,
                "icon": icon,
                "actions": actions or [],
                "timestamp": datetime.now().isoformat(),
                **(properties or {})
            }
        )
        self.message = message
        self.notification_type = notification_type
        self.priority = priority
        self.duration = duration
        self.creation_time = datetime.now()
        self.actions = actions or [] 