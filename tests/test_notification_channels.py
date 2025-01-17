import unittest
import os
import json
import logging
from datetime import datetime
from unittest.mock import MagicMock, patch
from maintenance.monitoring.notification_system import NotificationPriority
from maintenance.monitoring.notification_channels import (
    TelegramNotifier,
    WebhookNotifier,
    TeamsNotifier,
    PushoverNotifier,
    MatrixNotifier
)

class TestNotificationChannels(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Disable logging for tests
        logging.disable(logging.CRITICAL)
        
        # Test message
        self.test_message = "Test notification message"
        
        # Test configuration
        self.telegram_config = {
            "bot_token": "test_bot_token",
            "chat_id": "test_chat_id"
        }
        
        self.webhook_config = {
            "webhook_url": "https://test-webhook.com",
            "custom_headers": {"Authorization": "Bearer test-token"}
        }
        
        self.teams_config = {
            "webhook_url": "https://test-teams-webhook.com"
        }
        
        self.pushover_config = {
            "app_token": "test_app_token",
            "user_key": "test_user_key"
        }
        
        self.matrix_config = {
            "homeserver_url": "https://test-matrix.org",
            "access_token": "test_access_token",
            "room_id": "!test_room:matrix.org"
        }

    def tearDown(self):
        """Clean up after tests."""
        # Re-enable logging
        logging.disable(logging.NOTSET)

    @patch('requests.post')
    def test_telegram_notifications(self, mock_post):
        """Test Telegram notification channel."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Create notifier
        notifier = TelegramNotifier(
            bot_token=self.telegram_config["bot_token"],
            chat_id=self.telegram_config["chat_id"]
        )
        
        # Test all priority levels
        for priority in NotificationPriority:
            notifier.send(self.test_message, priority)
            
            # Verify API call
            mock_post.assert_called()
            args, kwargs = mock_post.call_args
            
            # Verify URL
            self.assertIn(self.telegram_config["bot_token"], args[0])
            
            # Verify payload
            payload = kwargs["json"]
            self.assertEqual(payload["chat_id"], self.telegram_config["chat_id"])
            self.assertIn(self.test_message, payload["text"])
            self.assertIn(priority.value.upper(), payload["text"])
            
            mock_post.reset_mock()

    @patch('requests.post')
    def test_webhook_notifications(self, mock_post):
        """Test webhook notification channel."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Create notifier
        notifier = WebhookNotifier(
            webhook_url=self.webhook_config["webhook_url"],
            custom_headers=self.webhook_config["custom_headers"]
        )
        
        # Test all priority levels
        for priority in NotificationPriority:
            notifier.send(self.test_message, priority)
            
            # Verify API call
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            
            # Verify headers
            self.assertDictEqual(
                kwargs["headers"],
                {
                    "Content-Type": "application/json",
                    **self.webhook_config["custom_headers"]
                }
            )
            
            # Verify payload
            payload = kwargs["json"]
            self.assertEqual(payload["message"], self.test_message)
            self.assertEqual(payload["priority"], priority.value)
            self.assertEqual(payload["source"], "Elysian Nexus")
            
            mock_post.reset_mock()

    @patch('requests.post')
    def test_teams_notifications(self, mock_post):
        """Test Microsoft Teams notification channel."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Create notifier
        notifier = TeamsNotifier(webhook_url=self.teams_config["webhook_url"])
        
        # Test all priority levels
        for priority in NotificationPriority:
            notifier.send(self.test_message, priority)
            
            # Verify API call
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            
            # Verify payload
            payload = kwargs["json"]
            self.assertEqual(payload["@type"], "MessageCard")
            self.assertIn(priority.value.upper(), payload["summary"])
            self.assertEqual(payload["sections"][0]["text"], self.test_message)
            
            mock_post.reset_mock()

    @patch('requests.post')
    def test_pushover_notifications(self, mock_post):
        """Test Pushover notification channel."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Create notifier
        notifier = PushoverNotifier(
            app_token=self.pushover_config["app_token"],
            user_key=self.pushover_config["user_key"]
        )
        
        # Test all priority levels
        for priority in NotificationPriority:
            notifier.send(self.test_message, priority)
            
            # Verify API call
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            
            # Verify payload
            payload = kwargs["data"]
            self.assertEqual(payload["token"], self.pushover_config["app_token"])
            self.assertEqual(payload["user"], self.pushover_config["user_key"])
            self.assertEqual(payload["message"], self.test_message)
            self.assertIn(priority.value.upper(), payload["title"])
            
            # Verify critical priority settings
            if priority == NotificationPriority.CRITICAL:
                self.assertEqual(payload["retry"], 30)
                self.assertEqual(payload["expire"], 3600)
            
            mock_post.reset_mock()

    @patch('requests.post')
    def test_matrix_notifications(self, mock_post):
        """Test Matrix notification channel."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Create notifier
        notifier = MatrixNotifier(
            homeserver_url=self.matrix_config["homeserver_url"],
            access_token=self.matrix_config["access_token"],
            room_id=self.matrix_config["room_id"]
        )
        
        # Test all priority levels
        for priority in NotificationPriority:
            notifier.send(self.test_message, priority)
            
            # Verify API call
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            
            # Verify URL
            self.assertIn(self.matrix_config["homeserver_url"], args[0])
            self.assertIn(self.matrix_config["room_id"], args[0])
            
            # Verify headers
            self.assertEqual(
                kwargs["headers"]["Authorization"],
                f"Bearer {self.matrix_config['access_token']}"
            )
            
            # Verify payload
            payload = kwargs["json"]
            self.assertEqual(payload["msgtype"], "m.text")
            self.assertIn(self.test_message, payload["body"])
            self.assertIn(priority.value.upper(), payload["body"])
            
            mock_post.reset_mock()

    def test_notification_error_handling(self):
        """Test error handling in notification channels."""
        # Create notifiers with invalid configurations
        telegram = TelegramNotifier("invalid_token", "invalid_chat_id")
        webhook = WebhookNotifier("https://invalid-webhook.com")
        teams = TeamsNotifier("https://invalid-teams-webhook.com")
        pushover = PushoverNotifier("invalid_token", "invalid_key")
        matrix = MatrixNotifier("https://invalid-matrix.org", "invalid_token", "invalid_room")
        
        # Test error handling for each channel
        for notifier in [telegram, webhook, teams, pushover, matrix]:
            try:
                notifier.send(self.test_message, NotificationPriority.HIGH)
            except Exception as e:
                self.fail(f"Notifier {type(notifier).__name__} raised unexpected exception: {str(e)}")

if __name__ == '__main__':
    unittest.main() 