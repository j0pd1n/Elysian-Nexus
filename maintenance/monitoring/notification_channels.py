from typing import Dict, Any, Optional
import logging
import requests
import json
from datetime import datetime
from maintenance.monitoring.notification_system import NotificationChannel, NotificationPriority

class TelegramNotifier(NotificationChannel):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send(self, message: str, priority: NotificationPriority):
        try:
            emoji = {
                NotificationPriority.LOW: "ℹ️",
                NotificationPriority.MEDIUM: "⚠️",
                NotificationPriority.HIGH: "🚨",
                NotificationPriority.CRITICAL: "🔥"
            }[priority]
            
            payload = {
                "chat_id": self.chat_id,
                "text": f"{emoji} *Elysian Nexus Alert*\nPriority: {priority.value.upper()}\n\n{message}",
                "parse_mode": "Markdown"
            }
            
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            logging.info(f"Telegram notification sent: {priority.value}")
        except Exception as e:
            logging.error(f"Failed to send Telegram notification: {str(e)}")

class WebhookNotifier(NotificationChannel):
    def __init__(self, webhook_url: str, custom_headers: Optional[Dict[str, str]] = None):
        self.webhook_url = webhook_url
        self.custom_headers = custom_headers or {}

    def send(self, message: str, priority: NotificationPriority):
        try:
            headers = {
                "Content-Type": "application/json",
                **self.custom_headers
            }
            
            payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "priority": priority.value,
                "message": message,
                "source": "Elysian Nexus",
                "alert_type": "system_notification"
            }
            
            response = requests.post(self.webhook_url, headers=headers, json=payload)
            response.raise_for_status()
            
            logging.info(f"Webhook notification sent: {priority.value}")
        except Exception as e:
            logging.error(f"Failed to send webhook notification: {str(e)}")

class TeamsNotifier(NotificationChannel):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: str, priority: NotificationPriority):
        try:
            color = {
                NotificationPriority.LOW: "00ff00",
                NotificationPriority.MEDIUM: "ffff00",
                NotificationPriority.HIGH: "ff9900",
                NotificationPriority.CRITICAL: "ff0000"
            }[priority]
            
            payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": color,
                "summary": f"Elysian Nexus Alert - {priority.value.upper()}",
                "sections": [{
                    "activityTitle": "Elysian Nexus Alert System",
                    "activitySubtitle": f"Priority: {priority.value.upper()}",
                    "text": message,
                    "facts": [
                        {
                            "name": "Timestamp",
                            "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                        },
                        {
                            "name": "Alert Level",
                            "value": priority.value.upper()
                        }
                    ]
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            
            logging.info(f"Teams notification sent: {priority.value}")
        except Exception as e:
            logging.error(f"Failed to send Teams notification: {str(e)}")

class PushoverNotifier(NotificationChannel):
    def __init__(self, app_token: str, user_key: str):
        self.app_token = app_token
        self.user_key = user_key
        self.api_url = "https://api.pushover.net/1/messages.json"

    def send(self, message: str, priority: NotificationPriority):
        try:
            priority_map = {
                NotificationPriority.LOW: -1,
                NotificationPriority.MEDIUM: 0,
                NotificationPriority.HIGH: 1,
                NotificationPriority.CRITICAL: 2
            }
            
            payload = {
                "token": self.app_token,
                "user": self.user_key,
                "message": message,
                "title": f"Elysian Nexus - {priority.value.upper()}",
                "priority": priority_map[priority],
                "sound": "cosmic" if priority == NotificationPriority.CRITICAL else "magic"
            }
            
            # Add emergency parameters for critical alerts
            if priority == NotificationPriority.CRITICAL:
                payload.update({
                    "retry": 30,  # Retry every 30 seconds
                    "expire": 3600  # Expire after 1 hour
                })
            
            response = requests.post(self.api_url, data=payload)
            response.raise_for_status()
            
            logging.info(f"Pushover notification sent: {priority.value}")
        except Exception as e:
            logging.error(f"Failed to send Pushover notification: {str(e)}")

class MatrixNotifier(NotificationChannel):
    def __init__(self, homeserver_url: str, access_token: str, room_id: str):
        self.homeserver_url = homeserver_url
        self.access_token = access_token
        self.room_id = room_id

    def send(self, message: str, priority: NotificationPriority):
        try:
            emoji = {
                NotificationPriority.LOW: "ℹ️",
                NotificationPriority.MEDIUM: "⚠️",
                NotificationPriority.HIGH: "🚨",
                NotificationPriority.CRITICAL: "🔥"
            }[priority]
            
            formatted_message = f"{emoji} **Elysian Nexus Alert**\n\n" \
                              f"Priority: {priority.value.upper()}\n\n" \
                              f"{message}"
            
            payload = {
                "msgtype": "m.text",
                "body": formatted_message,
                "format": "org.matrix.custom.html",
                "formatted_body": formatted_message.replace("\n", "<br>")
            }
            
            url = f"{self.homeserver_url}/_matrix/client/r0/rooms/{self.room_id}/send/m.room.message"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            logging.info(f"Matrix notification sent: {priority.value}")
        except Exception as e:
            logging.error(f"Failed to send Matrix notification: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Example Telegram notifier
    telegram = TelegramNotifier(
        bot_token="your_bot_token",
        chat_id="your_chat_id"
    )
    
    # Example webhook notifier
    webhook = WebhookNotifier(
        webhook_url="https://your-webhook-url",
        custom_headers={"Authorization": "Bearer your-token"}
    )
    
    # Example Teams notifier
    teams = TeamsNotifier(
        webhook_url="https://your-teams-webhook-url"
    )
    
    # Example Pushover notifier
    pushover = PushoverNotifier(
        app_token="your_app_token",
        user_key="your_user_key"
    )
    
    # Example Matrix notifier
    matrix = MatrixNotifier(
        homeserver_url="https://matrix.org",
        access_token="your_access_token",
        room_id="!your_room_id:matrix.org"
    )
    
    # Test notifications
    test_message = "This is a test notification from Elysian Nexus"
    for priority in NotificationPriority:
        telegram.send(test_message, priority)
        webhook.send(test_message, priority)
        teams.send(test_message, priority)
        pushover.send(test_message, priority)
        matrix.send(test_message, priority) 