import unittest
from unittest.mock import Mock, patch
import time
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum
import io
import sys

from faction_territory_system import FactionTerritorySystem, TerritoryType
from faction_alliance_system import FactionAllianceSystem, AllianceType
from dialogue_system import DialogueSystem

class UIStyle(Enum):
    HEADER = "\033[95m"
    INFO = "\033[94m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    DANGER = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

@dataclass
class UIElement:
    content: str
    style: UIStyle
    width: int = 80
    alignment: str = "left"

class UISystemTest(unittest.TestCase):
    def setUp(self):
        self.territory_system = FactionTerritorySystem()
        self.alliance_system = FactionAllianceSystem()
        self.dialogue_system = DialogueSystem()
        
        # Capture stdout for testing
        self.held_output = io.StringIO()
        sys.stdout = self.held_output
        
        # Initialize test data
        self.celestial_order = "Celestial Order"
        self.void_seekers = "Void Seekers"
        self.active_quests = {}
        self.notifications = []
        self.faction_reputations = {
            self.celestial_order: 75,
            self.void_seekers: 50
        }
        
    def tearDown(self):
        sys.stdout = sys.__stdout__
        
    def test_quest_tracking_display(self):
        """Test the quest tracking interface"""
        # Create test quest
        test_quest = {
            'id': 'ritual_mastery',
            'name': 'Path to Mastery',
            'type': 'RITUAL',
            'description': 'Master the art of ritual magic',
            'objectives': [
                {'description': 'Complete minor rituals', 'progress': 2, 'required': 3},
                {'description': 'Study ritual texts', 'progress': 5, 'required': 5}
            ]
        }
        self.active_quests[test_quest['id']] = test_quest
        
        # Display quest tracker
        self._display_quest_tracker()
        
        # Verify output
        output = self.held_output.getvalue()
        self.assertIn('Path to Mastery', output)
        self.assertIn('2/3', output)  # Progress display
        self.assertIn('5/5', output)  # Completed objective
        
    def test_ritual_casting_visualization(self):
        """Test ritual casting visualization"""
        # Create test ritual
        ritual_data = {
            'name': 'Celestial Convergence',
            'power_level': 0.8,
            'duration': 60,
            'participants': 3,
            'phase': 'channeling'
        }
        
        # Display ritual visualization
        self._display_ritual_casting(ritual_data)
        
        # Verify output
        output = self.held_output.getvalue()
        self.assertIn('Celestial Convergence', output)
        self.assertIn('Power Level: 80%', output)
        self.assertIn('Phase: CHANNELING', output)
        
    def test_celestial_event_notification(self):
        """Test celestial event notification system"""
        # Create test event
        event = {
            'type': 'CELESTIAL_CONVERGENCE',
            'intensity': 0.9,
            'duration': 3600,
            'effects': ['increased_magic', 'planar_weakness']
        }
        
        # Add notification
        self._add_notification(event)
        
        # Display notifications
        self._display_notifications()
        
        # Verify output
        output = self.held_output.getvalue()
        self.assertIn('CELESTIAL_CONVERGENCE', output)
        self.assertIn('90% Intensity', output)
        self.assertIn('Effects:', output)
        
    def test_faction_reputation_display(self):
        """Test faction reputation display"""
        # Display faction reputations
        self._display_faction_reputations()
        
        # Verify output
        output = self.held_output.getvalue()
        self.assertIn('Celestial Order', output)
        self.assertIn('75', output)  # Reputation value
        self.assertIn('Friendly', output)  # Reputation status
        
    def _display_quest_tracker(self):
        """Display active quests and their progress"""
        self._print_ui_element(UIElement(
            "Active Quests",
            UIStyle.HEADER
        ))
        
        for quest in self.active_quests.values():
            # Quest header
            self._print_ui_element(UIElement(
                f"{quest['name']} - {quest['type']}",
                UIStyle.BOLD
            ))
            
            # Quest description
            self._print_ui_element(UIElement(
                quest['description'],
                UIStyle.INFO
            ))
            
            # Objectives
            for obj in quest['objectives']:
                status = "✓" if obj['progress'] >= obj['required'] else " "
                progress = f"[{obj['progress']}/{obj['required']}]"
                self._print_ui_element(UIElement(
                    f"{status} {obj['description']} {progress}",
                    UIStyle.SUCCESS if status == "✓" else UIStyle.INFO
                ))
                
    def _display_ritual_casting(self, ritual_data: Dict):
        """Display ritual casting visualization"""
        # Ritual header
        self._print_ui_element(UIElement(
            f"Ritual: {ritual_data['name']}",
            UIStyle.HEADER
        ))
        
        # Ritual stats
        stats = [
            f"Power Level: {int(ritual_data['power_level'] * 100)}%",
            f"Duration: {ritual_data['duration']}s",
            f"Participants: {ritual_data['participants']}",
            f"Phase: {ritual_data['phase'].upper()}"
        ]
        
        for stat in stats:
            self._print_ui_element(UIElement(
                stat,
                UIStyle.INFO
            ))
            
        # Power bar
        power_bar = self._generate_power_bar(ritual_data['power_level'])
        self._print_ui_element(UIElement(
            power_bar,
            UIStyle.SUCCESS
        ))
        
    def _display_notifications(self):
        """Display celestial event notifications"""
        self._print_ui_element(UIElement(
            "Celestial Events",
            UIStyle.HEADER
        ))
        
        for notif in self.notifications:
            # Event header
            self._print_ui_element(UIElement(
                f"{notif['type']} - {int(notif['intensity'] * 100)}% Intensity",
                UIStyle.WARNING
            ))
            
            # Duration
            duration_hrs = notif['duration'] / 3600
            self._print_ui_element(UIElement(
                f"Duration: {duration_hrs:.1f} hours",
                UIStyle.INFO
            ))
            
            # Effects
            self._print_ui_element(UIElement(
                "Effects:",
                UIStyle.BOLD
            ))
            for effect in notif['effects']:
                self._print_ui_element(UIElement(
                    f"• {effect}",
                    UIStyle.INFO
                ))
                
    def _display_faction_reputations(self):
        """Display faction reputations"""
        self._print_ui_element(UIElement(
            "Faction Reputations",
            UIStyle.HEADER
        ))
        
        for faction, rep in self.faction_reputations.items():
            # Get reputation status
            status = self._get_reputation_status(rep)
            
            # Create reputation bar
            rep_bar = self._generate_reputation_bar(rep)
            
            # Display faction info
            self._print_ui_element(UIElement(
                f"{faction} - {status}",
                UIStyle.BOLD
            ))
            self._print_ui_element(UIElement(
                rep_bar,
                UIStyle.INFO
            ))
            
    def _print_ui_element(self, element: UIElement):
        """Print a UI element with styling"""
        content = element.content
        if element.alignment == "center":
            content = content.center(element.width)
        elif element.alignment == "right":
            content = content.rjust(element.width)
            
        print(f"{element.style.value}{content}{UIStyle.END.value}")
        
    def _generate_power_bar(self, power: float, width: int = 40) -> str:
        """Generate a visual power bar"""
        filled = int(power * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {int(power * 100)}%"
        
    def _generate_reputation_bar(self, reputation: int, width: int = 40) -> str:
        """Generate a visual reputation bar"""
        filled = int((reputation / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {reputation}/100"
        
    def _get_reputation_status(self, reputation: int) -> str:
        """Get reputation status text"""
        if reputation >= 90:
            return "Exalted"
        elif reputation >= 75:
            return "Friendly"
        elif reputation >= 50:
            return "Neutral"
        elif reputation >= 25:
            return "Unfriendly"
        else:
            return "Hostile"
            
    def _add_notification(self, event: Dict):
        """Add a new notification"""
        self.notifications.append(event) 