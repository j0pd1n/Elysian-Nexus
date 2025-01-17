from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

class NotificationType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    QUEST = "quest"
    ACHIEVEMENT = "achievement"

class NotificationPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3

@dataclass
class Notification:
    message: str
    type: NotificationType
    priority: NotificationPriority
    timestamp: datetime
    duration: Optional[int] = None  # Duration in seconds, None for persistent
    icon: Optional[str] = None
    sound: Optional[str] = None
    action: Optional[str] = None
    is_read: bool = False

class NotificationSystem:
    def __init__(self):
        self.notifications: List[Notification] = []
        self.max_notifications = 100
        self.default_duration = 5  # seconds
        self.type_icons = {
            NotificationType.INFO: "ℹ️",
            NotificationType.WARNING: "⚠️",
            NotificationType.ERROR: "❌",
            NotificationType.SUCCESS: "✅",
            NotificationType.QUEST: "⚔️",
            NotificationType.ACHIEVEMENT: "🏆"
        }
        self.type_sounds = {
            NotificationType.INFO: "info_sound",
            NotificationType.WARNING: "warning_sound",
            NotificationType.ERROR: "error_sound",
            NotificationType.SUCCESS: "success_sound",
            NotificationType.QUEST: "quest_sound",
            NotificationType.ACHIEVEMENT: "achievement_sound"
        }

    def add_notification(self, message: str, type: NotificationType = NotificationType.INFO,
                        priority: NotificationPriority = NotificationPriority.NORMAL,
                        duration: Optional[int] = None, icon: Optional[str] = None,
                        sound: Optional[str] = None, action: Optional[str] = None):
        """Add a new notification"""
        notification = Notification(
            message=message,
            type=type,
            priority=priority,
            timestamp=datetime.now(),
            duration=duration or self.default_duration,
            icon=icon or self.type_icons.get(type),
            sound=sound or self.type_sounds.get(type),
            action=action
        )
        
        self.notifications.append(notification)
        self._trim_notifications()
        self._play_notification_sound(notification)
        self._display_notification(notification)

    def get_active_notifications(self) -> List[Notification]:
        """Get all active (non-expired) notifications"""
        current_time = datetime.now()
        return [
            n for n in self.notifications
            if n.duration is None or
            current_time - n.timestamp < timedelta(seconds=n.duration)
        ]

    def get_notifications_by_type(self, type: NotificationType) -> List[Notification]:
        """Get all notifications of a specific type"""
        return [n for n in self.notifications if n.type == type]

    def get_notifications_by_priority(self, priority: NotificationPriority) -> List[Notification]:
        """Get all notifications of a specific priority"""
        return [n for n in self.notifications if n.priority == priority]

    def mark_as_read(self, notification: Notification):
        """Mark a notification as read"""
        notification.is_read = True

    def clear_notifications(self, type: Optional[NotificationType] = None):
        """Clear notifications, optionally of a specific type"""
        if type:
            self.notifications = [n for n in self.notifications if n.type != type]
        else:
            self.notifications.clear()

    def _trim_notifications(self):
        """Trim notifications list if it exceeds max size"""
        if len(self.notifications) > self.max_notifications:
            self.notifications = sorted(
                self.notifications,
                key=lambda n: (n.is_read, -n.priority.value, n.timestamp)
            )[:self.max_notifications]

    def _play_notification_sound(self, notification: Notification):
        """Play the notification sound"""
        if notification.sound:
            print(f"Playing sound: {notification.sound}")

    def _display_notification(self, notification: Notification):
        """Display the notification"""
        icon = notification.icon or ""
        print(f"{icon} {notification.message}")
        if notification.action:
            print(f"Action: {notification.action}")

    def update(self):
        """Update notification system, removing expired notifications"""
        current_time = datetime.now()
        self.notifications = [
            n for n in self.notifications
            if n.duration is None or
            current_time - n.timestamp < timedelta(seconds=n.duration)
        ]

    def get_unread_count(self) -> Dict[NotificationType, int]:
        """Get count of unread notifications by type"""
        unread_counts = {type: 0 for type in NotificationType}
        for notification in self.notifications:
            if not notification.is_read:
                unread_counts[notification.type] += 1
        return unread_counts

    def mark_all_as_read(self, type: Optional[NotificationType] = None):
        """Mark all notifications as read, optionally of a specific type"""
        for notification in self.notifications:
            if type is None or notification.type == type:
                notification.is_read = True

    def get_notification_history(self) -> List[Notification]:
        """Get complete notification history"""
        return sorted(self.notifications, key=lambda n: n.timestamp, reverse=True)

    def set_max_notifications(self, max_count: int):
        """Set maximum number of notifications to keep"""
        self.max_notifications = max_count
        self._trim_notifications()

    def set_default_duration(self, duration: int):
        """Set default notification duration"""
        self.default_duration = duration 