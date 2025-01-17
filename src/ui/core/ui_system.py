from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from enum import Enum
import time
import logging
from datetime import datetime, timedelta
import os

class UIStyle(Enum):
    HEADER = "\033[95m"
    INFO = "\033[94m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    DANGER = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

class MenuIcons:
    # Main menu icons
    PLAY = "▶️"
    SETTINGS = "⚙️"
    EXIT = "🚪"
    SAVE = "💾"
    LOAD = "📂"
    
    # Character menu icons
    STATS = "📊"
    SKILLS = "⚔️"
    EQUIPMENT = "🛡️"
    INVENTORY = "🎒"
    QUESTS = "📜"
    MAP = "🗺️"
    
    # Status icons
    HEALTH = "❤️"
    MANA = "🔮"
    STAMINA = "⚡"
    EXPERIENCE = "✨"
    GOLD = "💰"
    
    # Faction icons
    CELESTIAL = "🌟"
    VOID = "🌌"
    PRIMAL = "🌋"
    TEMPORAL = "⌛"
    REALITY = "🎭"
    ESSENCE = "💫"
    CHAOS = "🌀"
    ORDER = "⚖️"
    
    # System icons
    NOTIFICATION = "📢"
    WARNING = "⚠️"
    ERROR = "❌"
    SUCCESS = "✅"
    INFO = "ℹ️"
    
    # Ritual icons
    RITUAL_START = "🕯️"
    RITUAL_ACTIVE = "🔮"
    RITUAL_COMPLETE = "✨"
    RITUAL_FAILED = "💨"

class MenuType(Enum):
    MAIN = "main"
    PAUSE = "pause"
    INVENTORY = "inventory"
    CHARACTER = "character"
    QUEST = "quest"
    MAP = "map"
    SETTINGS = "settings"
    HELP = "help"

class UITheme(Enum):
    COSMIC = "cosmic"
    VOID = "void"
    CELESTIAL = "celestial"
    SHADOW = "shadow"
    CRYSTAL = "crystal"
    ETHEREAL = "ethereal"

@dataclass
class UIElement:
    content: str
    style: UIStyle
    width: int = 80
    alignment: str = "left"
    icon: Optional[str] = None

class UISystem:
    def __init__(self):
        self.active_quests: Dict[str, Dict] = {}
        self.notifications: List[Dict] = []
        self.faction_reputations: Dict[str, int] = {}
        self.active_rituals: Dict[str, Dict] = {}
        self.current_theme = UITheme.COSMIC
        self.menu_history: List[MenuType] = []
        
        # Border styles for different themes
        self.borders = {
            UITheme.COSMIC: {
                "top_left": "╔", "top_right": "╗",
                "bottom_left": "╚", "bottom_right": "╝",
                "horizontal": "═", "vertical": "║",
                "separator": "─"
            },
            UITheme.VOID: {
                "top_left": "┌", "top_right": "┐",
                "bottom_left": "└", "bottom_right": "┘",
                "horizontal": "─", "vertical": "│",
                "separator": "·"
            },
            UITheme.CELESTIAL: {
                "top_left": "🌟", "top_right": "🌟",
                "bottom_left": "🌟", "bottom_right": "🌟",
                "horizontal": "✨", "vertical": "✨",
                "separator": "·"
            },
            UITheme.SHADOW: {
                "top_left": "▓", "top_right": "▓",
                "bottom_left": "▓", "bottom_right": "▓",
                "horizontal": "▀", "vertical": "█",
                "separator": "░"
            },
            UITheme.CRYSTAL: {
                "top_left": "💎", "top_right": "💎",
                "bottom_left": "💎", "bottom_right": "💎",
                "horizontal": "✧", "vertical": "✦",
                "separator": "·"
            },
            UITheme.ETHEREAL: {
                "top_left": "🌸", "top_right": "🌸",
                "bottom_left": "🌸", "bottom_right": "🌸",
                "horizontal": "❀", "vertical": "❀",
                "separator": "·"
            }
        }
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('UISystem')
        
    def update_quest(self, quest_id: str, quest_data: Dict):
        """Update or add a quest to the tracking system"""
        self.active_quests[quest_id] = quest_data
        self.logger.info(f"{MenuIcons.QUESTS} Updated quest: {quest_data['name']}")
        
    def remove_quest(self, quest_id: str):
        """Remove a completed quest from tracking"""
        if quest_id in self.active_quests:
            quest = self.active_quests.pop(quest_id)
            self.logger.info(f"{MenuIcons.SUCCESS} Removed quest: {quest['name']}")
            
    def update_ritual_status(self, ritual_id: str, ritual_data: Dict):
        """Update or add a ritual's casting status"""
        self.active_rituals[ritual_id] = ritual_data
        self.logger.info(f"Updated ritual status: {ritual_data['name']}")
        
    def add_notification(self, event: Dict):
        """Add a new celestial event notification"""
        self.notifications.append({
            **event,
            'timestamp': datetime.now()
        })
        self.logger.info(f"New celestial event: {event['type']}")
        
    def update_faction_reputation(self, faction: str, reputation: int):
        """Update a faction's reputation value"""
        self.faction_reputations[faction] = max(0, min(100, reputation))
        self.logger.info(f"Updated {faction} reputation to {reputation}")
        
    def display_quest_tracker(self):
        """Display active quests and their progress"""
        self._print_ui_element(UIElement(
            "Active Quests",
            UIStyle.HEADER
        ))
        
        if not self.active_quests:
            self._print_ui_element(UIElement(
                "No active quests",
                UIStyle.INFO
            ))
            return
            
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
                
    def display_ritual_casting(self, ritual_id: str):
        """Display ritual casting visualization"""
        if ritual_id not in self.active_rituals:
            self._print_ui_element(UIElement(
                f"No active ritual found with ID: {ritual_id}",
                UIStyle.WARNING
            ))
            return
            
        ritual_data = self.active_rituals[ritual_id]
        
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
        
        # Additional effects if any
        if 'effects' in ritual_data:
            self._print_ui_element(UIElement(
                "Active Effects:",
                UIStyle.BOLD
            ))
            for effect in ritual_data['effects']:
                self._print_ui_element(UIElement(
                    f"• {effect}",
                    UIStyle.INFO
                ))
                
    def display_notifications(self, max_age: Optional[timedelta] = None):
        """Display celestial event notifications"""
        self._print_ui_element(UIElement(
            "Celestial Events",
            UIStyle.HEADER
        ))
        
        current_time = datetime.now()
        active_notifications = [
            n for n in self.notifications
            if not max_age or (current_time - n['timestamp']) <= max_age
        ]
        
        if not active_notifications:
            self._print_ui_element(UIElement(
                "No active celestial events",
                UIStyle.INFO
            ))
            return
            
        for notif in active_notifications:
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
            if 'effects' in notif:
                self._print_ui_element(UIElement(
                    "Effects:",
                    UIStyle.BOLD
                ))
                for effect in notif['effects']:
                    self._print_ui_element(UIElement(
                        f"• {effect}",
                        UIStyle.INFO
                    ))
                    
    def display_faction_reputations(self):
        """Display faction reputations"""
        # ASCII Art
        for line in self._get_faction_ascii().split('\n'):
            self._print_ui_element(UIElement(
                line,
                UIStyle.HEADER,
                alignment="center"
            ))

        self._print_ui_element(UIElement(
            "\n╔═══════════《 FACTIONS 》═══════════╗",
            UIStyle.HEADER,
            alignment="center"
        ))
        self._print_ui_element(UIElement(
            "║      ✧  Alliances and Rivalries  ✧      ║",
            UIStyle.INFO,
            alignment="center"
        ))
        self._print_ui_element(UIElement(
            "╠══════════════════════════════════════╣",
            UIStyle.HEADER,
            alignment="center"
        ))
        
        if not self.faction_reputations:
            self._print_ui_element(UIElement(
                "  No faction reputations tracked",
                UIStyle.INFO
            ))
            return
            
        for faction, rep in self.faction_reputations.items():
            # Get reputation status
            status = self._get_reputation_status(rep)
            
            # Get faction symbol
            symbol = {
                "Celestial Order": "✨",
                "Void Seekers": "🌌",
                "Primal Circle": "🌿"
            }.get(faction, "⚔")
            
            # Create reputation bar
            rep_bar = self._generate_reputation_bar(rep)
            
            # Display faction info with symbol
            self._print_ui_element(UIElement(
                f"\n  {symbol} {faction}",
                UIStyle.BOLD
            ))
            self._print_ui_element(UIElement(
                f"    Status: {status}",
                self._get_reputation_style(rep)
            ))
            self._print_ui_element(UIElement(
                f"    {rep_bar}",
                UIStyle.INFO
            ))
        
        self._print_ui_element(UIElement(
            "\n╚══════════════════════════════════════╝",
            UIStyle.HEADER,
            alignment="center"
        ))

    def display_main_menu(self):
        """Display the main game menu"""
        self.clear_screen()
        print("""
        ╔══════════════════════════════════════╗
        ║           ELYSIAN NEXUS              ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║    1. 🚀 Begin Cosmic Voyage         ║
        ║    2. 🔄 Continue Orbit              ║
        ║    3. 🗺️ Star Charts                 ║
        ║    4. ⚙️ Nebula Settings             ║
        ║    5. 🌍 Return to Earth             ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """)
    
    def display_pause_menu(self):
        """Display the pause menu"""
        self.clear_screen()
        print("""
        ╔══════════════════════════════════════╗
        ║             PAUSED                   ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║    1. ▶️ Resume Journey              ║
        ║    2. 💾 Save Progress               ║
        ║    3. ⚙️ Adjust Settings             ║
        ║    4. 📖 View Help                   ║
        ║    5. 🚪 Exit to Main Menu           ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """)
    
    def display_inventory_menu(self):
        """Display the inventory menu"""
        self.clear_screen()
        print("""
        ╔══════════════════════════════════════╗
        ║            INVENTORY                 ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║    1. 🎒 View Items                  ║
        ║    2. 💎 View Equipment              ║
        ║    3. 🧪 Use Item                    ║
        ║    4. 🔄 Sort Inventory              ║
        ║    5. ⬅️ Back                        ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """)
    
    def display_character_menu(self):
        """Display the character menu"""
        self.clear_screen()
        print("""
        ╔══════════════════════════════════════╗
        ║           CHARACTER                  ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║    1. 📊 View Stats                  ║
        ║    2. 🎯 Skills & Abilities          ║
        ║    3. 🏆 Achievements                ║
        ║    4. 👥 Faction Standing            ║
        ║    5. ⬅️ Back                        ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """)
    
    def display_quest_menu(self):
        """Display the quest menu"""
        self.clear_screen()
        print("""
        ╔══════════════════════════════════════╗
        ║             QUESTS                   ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║    1. 📜 Active Quests               ║
        ║    2. ✨ Available Quests             ║
        ║    3. ✅ Completed Quests             ║
        ║    4. 🎯 Track Quest                 ║
        ║    5. ⬅️ Back                        ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """)
    
    def display_map_menu(self):
        """Display the map menu"""
        self.clear_screen()
        print("""
        ╔══════════════════════════════════════╗
        ║              MAP                     ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║    1. 🗺️ View World Map              ║
        ║    2. 📍 View Current Region         ║
        ║    3. ⭐ View Points of Interest     ║
        ║    4. 🚀 Fast Travel                 ║
        ║    5. ⬅️ Back                        ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """)
    
    def display_settings_menu(self):
        """Display the settings menu"""
        self.clear_screen()
        print("""
        ╔══════════════════════════════════════╗
        ║            SETTINGS                  ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║    1. 🎮 Game Settings               ║
        ║    2. 🔊 Sound Settings              ║
        ║    3. 🎨 Visual Settings             ║
        ║    4. ⌨️ Controls                    ║
        ║    5. ⬅️ Back                        ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """)
    
    def display_help_menu(self):
        """Display the help menu"""
        self.clear_screen()
        print("""
        ╔══════════════════════════════════════╗
        ║              HELP                    ║
        ╠══════════════════════════════════════╣
        ║                                      ║
        ║    1. 📖 Game Guide                  ║
        ║    2. ⚔️ Combat Tutorial             ║
        ║    3. 🎮 Controls                    ║
        ║    4. ❓ FAQ                         ║
        ║    5. ⬅️ Back                        ║
        ║                                      ║
        ╚══════════════════════════════════════╝
        """)
    
    def go_back(self) -> Optional[MenuType]:
        """Go back to the previous menu"""
        if len(self.menu_history) > 1:
            self.menu_history.pop()  # Remove current menu
            return self.menu_history[-1]  # Return previous menu
        return None
    
    def display_notification(self, message: str, duration: int = 3):
        """Display a notification message"""
        print(f"\n📢 {message}")
        # In a real implementation, this would handle the duration and fade effects
    
    def display_progress_bar(self, progress: float, width: int = 20) -> str:
        """Create a progress bar"""
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {int(progress * 100)}%"
    
    def display_stats_table(self, stats: Dict[str, int], width: int = 30) -> str:
        """Create a formatted stats table"""
        table = []
        style = self.borders[self.current_theme]
        
        # Create header
        table.append(style["top_left"] + style["horizontal"] * width + style["top_right"])
        
        # Add stats
        for stat, value in stats.items():
            padding = width - len(stat) - len(str(value)) - 2
            table.append(f"{style['vertical']} {stat}{' ' * padding}{value} {style['vertical']}")
        
        # Add footer
        table.append(style["bottom_left"] + style["horizontal"] * width + style["bottom_right"])
        
        return "\n".join(table)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def set_theme(self, theme: UITheme):
        """Set the UI theme"""
        self.current_theme = theme
    
    def create_border(self, width: int, height: int) -> str:
        """Create a border with the current theme"""
        style = self.borders[self.current_theme]
        
        # Create top border
        border = [style["top_left"] + style["horizontal"] * width + style["top_right"]]
        
        # Create middle section
        for _ in range(height):
            border.append(style["vertical"] + " " * width + style["vertical"])
        
        # Create bottom border
        border.append(style["bottom_left"] + style["horizontal"] * width + style["bottom_right"])
        
        return "\n".join(border)
    
    def create_separator(self, width: int) -> str:
        """Create a separator line with the current theme"""
        style = self.borders[self.current_theme]
        return style["separator"] * width
    
    def display_title_screen(self, theme: str = "cosmic"):
        """Display the game's title screen"""
        self.clear_screen()
        
        if theme == "cosmic":
            print("""
            ╔══════════════════════════════════════╗
            ║     E L Y S I A N   N E X U S        ║
            ║                                      ║
            ║        A Journey Through the         ║
            ║          Cosmic Void                 ║
            ╚══════════════════════════════════════╝
            """)
        elif theme == "void":
            print("""
            ┌──────────────────────────────────────┐
            │     E L Y S I A N   N E X U S        │
            │                                      │
            │        Whispers of the               │
            │          V O I D                     │
            └──────────────────────────────────────┘
            """)
        elif theme == "celestial":
            print("""
            🌟✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨🌟
            ✨     E L Y S I A N   N E X U S        ✨
            ✨                                      ✨
            ✨        Celestial Dreams              ✨
            ✨          Await                       ✨
            🌟✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨🌟
            """)
    
    def display_menu(self, menu_type: MenuType):
        """Display a menu of the specified type"""
        self.menu_history.append(menu_type)
        
        if menu_type == MenuType.MAIN:
            self.display_main_menu()
        elif menu_type == MenuType.PAUSE:
            self.display_pause_menu()
        elif menu_type == MenuType.INVENTORY:
            self.display_inventory_menu()
        elif menu_type == MenuType.CHARACTER:
            self.display_character_menu()
        elif menu_type == MenuType.QUEST:
            self.display_quest_menu()
        elif menu_type == MenuType.MAP:
            self.display_map_menu()
        elif menu_type == MenuType.SETTINGS:
            self.display_settings_menu()
        elif menu_type == MenuType.HELP:
            self.display_help_menu()
    
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

    def _get_main_menu_ascii(self):
        """Get ASCII art for main menu"""
        return """
           /\\
          /  \\
         /    \\
     ___/______\\___
    /   \\      /   \\
   /     \\    /     \\
  /       \\  /       \\
 /__________\\/________\\"""

    def _get_ritual_ascii(self):
        """Get ASCII art for ritual menu"""
        return """
         .    *    .  ✧
      .  *  ✧    *  .
    *    |\\___/|    .
     .   (⚝._.⚝) *    ✧
    ✧  <( ° ° )>  .
         (  T  )    *
        .`-^-'."""

    def _get_character_ascii(self):
        """Get ASCII art for character menu"""
        return """
           /^\\
          /   \\
     ____/  ⚔  \\____
    |    |     |    |
    |____|     |____|
         |  ⚡  |
         \\_____/"""

    def _get_inventory_ascii(self):
        """Get ASCII art for inventory menu"""
        return """
      _____________________
     /\\                    \\
    /  \\    🎁  📦  💎     \\
   /    \\                   \\
  /      \\___________________\\
  \\      /                   /
   \\    /                   /
    \\  /                   /
     \\/_________________  /"""

    def _get_settings_ascii(self):
        """Get ASCII art for settings menu"""
        return """
        ⚙️  ⚙️  ⚙️
     _____________
    /  _________  \\
   /  /         \\  \\
  /  /           \\  \\
  |  |           |  |
  |  |           |  |
  \\  \\_________/  /
   \\             /
    \\_________  /"""

    def _get_faction_ascii(self):
        """Get ASCII art for faction menu"""
        return """
           ⚔️
      _____|_____
     /\\    |    /\\
    /  \\   |   /  \\
   /    \\  |  /    \\
  /      \\ | /      \\
 /_________\\|/_______\\"""

    def _get_reputation_style(self, reputation: int) -> UIStyle:
        """Get UI style based on reputation level"""
        if reputation >= 90:
            return UIStyle.HEADER  # Purple for Exalted
        elif reputation >= 75:
            return UIStyle.SUCCESS  # Green for Friendly
        elif reputation >= 50:
            return UIStyle.INFO  # Blue for Neutral
        elif reputation >= 25:
            return UIStyle.WARNING  # Yellow for Unfriendly
        else:
            return UIStyle.DANGER  # Red for Hostile 

    def _get_celestial_event_ascii(self):
        """ASCII art for celestial events"""
        return """
           *    .  ✧    *    .    ✧ 
      '  .  ✧  *  .  ✧    *   .
    ✧    .    *    .    *    .   ✧
     .    *   .-""-. *    .   *
    *   ✧ .-"  |   "-.  ✧   .
     . ."    .-+-.    ".   ✧  *
    ✧ |     |   |     |  *
     ."     "-+-"    ✧".    .  *
    *   ✧.-"  |   "-. ✧  *
     ..-"   .-+-.   "-.  .   ✧
           "  |  "      *    ."""

    def _get_void_portal_ascii(self):
        """ASCII art for void portals"""
        return """
           ╭──────────╮
        .──┤ VOID GATE├──.
       /   ╰──────────╯   \\
      │   ╭────────────╮   │
      │   │  ▒▒▒▒▒▒▒▒  │   │
      │   │ ▒ 🌌  🌌 ▒ │   │
      │   │▒   VOID   ▒│   │
      │   │ ▒  ▒▒▒  ▒ │   │
      │   │  ▒▒▒▒▒▒▒▒  │   │
      │   ╰────────────╯   │
       \\        ▒▒        /
        `──.    ▒▒    .──'
           `────▒▒────'"""

    def _get_ritual_circle_ascii(self):
        """ASCII art for ritual circles"""
        return """
           ✧     ⚡     ✧
        ╭────────────────╮
        │  ⭕  RITUAL ⭕  │
        │ ╭────────────╮ │
        │ │   ✨🔮✨   │ │
        │ │  ENERGIES  │ │
        │ │   FLOW     │ │
        │ ╰────────────╯ │
        │     ⚡ ⚡      │
        ╰────────────────╯
           ✧     ⚡     ✧"""

    def _get_combat_ascii(self):
        """ASCII art for combat scenes"""
        return """
        ⚔️ COMBAT INITIATED ⚔️
        ╭────────────────────╮
        │    🗡️  VS  🗡️     │
        │  ╭────────────╮   │
        │  │ PREPARE TO │   │
        │  │   FIGHT   │   │
        │  ╰────────────╯   │
        │      ⚔️  ⚔️       │
        ╰────────────────────╯"""

    def _get_level_up_ascii(self):
        """ASCII art for level up celebrations"""
        return """
           ⭐ LEVEL UP! ⭐
        ╭────────────────╮
        │ ✨ CONGRATULATIONS ✨│
        │  ╭────────────╮  │
        │  │   POWER    │  │
        │  │  SURGES    │  │
        │  │  WITHIN    │  │
        │  ╰────────────╯  │
        │    🌟  ⚡  🌟    │
        ╰────────────────╯"""

    def _get_quest_complete_ascii(self):
        """ASCII art for quest completion"""
        return """
        ⭐ QUEST COMPLETE! ⭐
        ╭────────────────────╮
        │   ✨ VICTORY! ✨   │
        │  ╭────────────╮   │
        │  │  DESTINY   │   │
        │  │ FULFILLED  │   │
        │  ╰────────────╯   │
        │   🏆  ⚔️  🏆    │
        ╰────────────────────╯"""

    def _get_treasure_ascii(self):
        """ASCII art for treasure discovery"""
        return """
           💎 TREASURE! 💎
        ╭────────────────╮
        │   DISCOVERED   │
        │  ╭──────────╮  │
        │  │  💰💎💰  │  │
        │  │ RICHES   │  │
        │  │ AWAIT!   │  │
        │  ╰──────────╯  │
        │    ✨  ✨  ✨   │
        ╰────────────────╯"""

    def _get_magic_scroll_ascii(self):
        """ASCII art for magical scrolls"""
        return """
         ╭──────────────╮
         │ ✧  SCROLL  ✧ │
      .──┤──────────────├──.
     /   │  ╭────────╮  │   \\
    │    │  │✨🔮✨│  │    │
    │    │  │  TEXT  │  │    │
    │    │  ╰────────╯  │    │
     \\   │              │   /
      `──┤──────────────├──'
         ╰──────────────╯"""

    def _get_boss_battle_ascii(self):
        """ASCII art for boss battles"""
        return """
           ⚔️ BOSS BATTLE ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤PREPARE!├─╮   │
        │  │ ╰────────╯ │   │
        │  │    ☠️ ☠️    │   │
        │  │  ╭────╮    │   │
        │  ╰──┤BOSS├────╯   │
        │     ╰────╯        │
        ╰────────────────────╯"""

    def _get_meditation_ascii(self):
        """ASCII art for meditation scenes"""
        return """
           ✧ MEDITATION ✧
             ╭─────╮
          .──┤ 🕉️ ├──.
         /   ╰─────╯   \\
        │  ╭─────────╮  │
        │  │  Peace  │  │
        │  │   And   │  │
        │  │ Balance │  │
        │  ╰─────────╯  │
         \\    ✨ ✨    /
          `──.   .──'
             `─'"""

    def _get_achievement_ascii(self):
        """ASCII art for achievements"""
        return """
        🏆 ACHIEVEMENT! 🏆
        ╭────────────────╮
        │  MILESTONE     │
        │  ╭──────────╮  │
        │  │ ⭐⭐⭐  │  │
        │  │UNLOCKED! │  │
        │  │ ⭐⭐⭐  │  │
        │  ╰──────────╯  │
        │   GLORY AWAITS │
        ╰────────────────╯"""

    def _get_shop_ascii(self):
        """ASCII art for the merchant shop"""
        return """
           🏪 MERCHANT 🏪
        ╭────────────────╮
        │  MYSTIC WARES  │
        │  ╭──────────╮  │
        │  │ 💰🎁💰  │  │
        │  │ TRADING  │  │
        │  │  POST    │  │
        │  ╰──────────╯  │
        │  RARE TREASURES │
        ╰────────────────╯"""

    def _get_faction_event_ascii(self):
        """ASCII art for faction events"""
        return """
           ⚔️ FACTION EVENT ⚔️
        ╭────────────────────╮
        │   POWER SHIFTS     │
        │  ╭────────────╮   │
        │  │ ALLIANCES  │   │
        │  │   FORM    │   │
        │  │ AND BREAK │   │
        │  ╰────────────╯   │
        │    🛡️  ⚔️  🛡️    │
        ╰────────────────────╯"""

    def _get_spell_cast_ascii(self):
        """ASCII art for spell casting"""
        return """
           ✨ SPELL CAST ✨
        ╭────────────────────╮
        │   ARCANE POWER    │
        │  ╭────────────╮   │
        │  │  🔮 ⚡ 🔮  │   │
        │  │ CHANNELING │   │
        │  │   MAGIC    │   │
        │  ╰────────────╯   │
        │    ✨  🌟  ✨    │
        ╰────────────────────╯"""

    def _get_dungeon_ascii(self):
        """ASCII art for dungeon entrance"""
        return """
           🏰 DUNGEON 🏰
        ╭────────────────╮
        │  DARK DEPTHS   │
        │  ╭──────────╮  │
        │  │ 🏮  🏮  │  │
        │  │MYSTERIES │  │
        │  │ AWAIT   │  │
        │  ╰──────────╯  │
        │   ENTER IF DARE │
        ╰────────────────╯"""

    def _get_crafting_ascii(self):
        """ASCII art for crafting station"""
        return """
          ⚒️ CRAFTING ⚒️
        ╭────────────────╮
        │  MYSTIC FORGE  │
        │  ╭──────────╮  │
        │  │ 🛠️  ⚡  │  │
        │  │ CREATE   │  │
        │  │ WONDERS  │  │
        │  ╰──────────╯  │
        │  FORGE DESTINY  │
        ╰────────────────╯"""

    def _get_skill_tree_ascii(self):
        """ASCII art for skill tree"""
        return """
           🌟 SKILLS 🌟
        ╭────────────────╮
        │  MYSTIC PATHS  │
        │     ┌─🔮─┐     │
        │   ┌─⚡─┐ │     │
        │   │ │ │ │     │
        │   └─✨─┘ │     │
        │     └─🌟─┘     │
        │  CHOOSE WISELY │
        ╰────────────────╯"""

    def _get_sanctuary_ascii(self):
        """ASCII art for sanctuary/safe zone"""
        return """
          🕊️ SANCTUARY 🕊️
        ╭────────────────╮
        │   SAFE HAVEN   │
        │  ╭──────────╮  │
        │  │ 🌟  ✨  │  │
        │  │  REST    │  │
        │  │ & HEAL   │  │
        │  ╰──────────╯  │
        │  FIND PEACE    │
        ╰────────────────╯"""

    def _get_enchanting_ascii(self):
        """ASCII art for enchanting station"""
        return """
         ✨ ENCHANTING ✨
        ╭────────────────╮
        │  IMBUE POWER   │
        │  ╭──────────╮  │
        │  │ 🔮  ⚡  │  │
        │  │ ENHANCE  │  │
        │  │ ITEMS    │  │
        │  ╰──────────╯  │
        │ ANCIENT MAGIC  │
        ╰────────────────╯"""

    def _get_map_ascii(self):
        """ASCII art for world map"""
        return """
           🗺️ MAP 🗺️
        ╭────────────────╮
        │  REALM CHART   │
        │  ╭──────────╮  │
        │  │ 🌍 🧭 🌟 │  │
        │  │DISCOVER  │  │
        │  │WONDERS   │  │
        │  ╰──────────╯  │
        │ CHART DESTINY  │
        ╰────────────────╯"""

    def _get_portal_hub_ascii(self):
        """ASCII art for portal hub"""
        return """
          🌀 NEXUS 🌀
        ╭────────────────╮
        │ PORTAL NEXUS   │
        │  ╭──────────╮  │
        │  │ 🌌 🚪 🌌 │  │
        │  │TRAVERSE  │  │
        │  │REALMS    │  │
        │  ╰──────────╯  │
        │ CHOOSE PATH    │
        ╰────────────────╯"""

    def _get_library_ascii(self):
        """ASCII art for mystical library"""
        return """
          📚 LIBRARY 📚
        ╭────────────────╮
        │ ANCIENT TOMES  │
        │  ╭──────────╮  │
        │  │ 📖 🔮 📜 │  │
        │  │KNOWLEDGE │  │
        │  │AWAITS    │  │
        │  ╰──────────╯  │
        │ SEEK WISDOM    │
        ╰────────────────╯"""

    def _get_altar_ascii(self):
        """ASCII art for ritual altar"""
        return """
          🕯️ ALTAR 🕯️
        ╭────────────────╮
        │ SACRED SPACE   │
        │  ╭──────────╮  │
        │  │ 🔮 ⭐ 🔮 │  │
        │  │COMMUNE   │  │
        │  │WITH VOID │  │
        │  ╰──────────╯  │
        │ OFFER TRIBUTE  │
        ╰────────────────╯"""

    def _get_void_titan_ascii(self):
        """ASCII art for the Void Titan boss"""
        return """
           ⚔️ VOID TITAN ⚔️
        ╭────────────────────╮
        │      ╭────╮       │
        │    ╭─┤👁️👁️├─╮     │
        │   ╭┤ ╰────╯ ├╮    │
        │   ││  VOID  ││    │
        │   ││ TITAN  ││    │
        │   ╰┤  🌌   ├╯    │
        │    ╰──────╯      │
        │  Ancient Horror   │
        ╰────────────────────╯"""

    def _get_celestial_dragon_ascii(self):
        """ASCII art for the Celestial Dragon boss"""
        return """
         ⚔️ CELESTIAL DRAGON ⚔️
        ╭──────────────────────╮
        │    ><><><><><><      │
        │   ╭──────────╮      │
        │  <│ 🐉  ⚡  │>     │
        │   │DRAGON OF│       │
        │  <│ STARS  │>      │
        │   ╰──────────╯      │
        │    ><><><><><><     │
        │   Cosmic Wyrm       │
        ╰──────────────────────╯"""

    def _get_shadow_queen_ascii(self):
        """ASCII art for the Shadow Queen boss"""
        return """
          ⚔️ SHADOW QUEEN ⚔️
        ╭────────────────────╮
        │     ╭──────╮      │
        │   ╭─┤👑 👑├─╮    │
        │   │ │🌙 🌙│ │    │
        │   │ │QUEEN│ │    │
        │   │ │DARK│ │    │
        │   ╰─┤💀 💀├─╯    │
        │     ╰──────╯      │
        │   Dark Sovereign   │
        ╰────────────────────╯"""

    def _get_time_weaver_ascii(self):
        """ASCII art for the Time Weaver boss"""
        return """
         ⚔️ TIME WEAVER ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤⌛ ⌛├─╮    │
        │  │ │WEAVER│ │    │
        │  │ │ OF   │ │    │
        │  │ │TIME  │ │    │
        │  ╰─┤⚡ ⚡├─╯    │
        │    ╰────────╯     │
        │  Temporal Entity   │
        ╰────────────────────╯"""

    def _get_chaos_lord_ascii(self):
        """ASCII art for the Chaos Lord boss"""
        return """
          ⚔️ CHAOS LORD ⚔️
        ╭────────────────────╮
        │     ╭──────╮      │
        │   ╭─┤🌪️ 🌪️├─╮    │
        │   │ │CHAOS│ │    │
        │   │ │LORD │ │    │
        │   │ │⚔️ ⚔️│ │    │
        │   ╰─┤💥 💥├─╯    │
        │     ╰──────╯      │
        │  Master of Chaos   │
        ╰────────────────────╯"""

    def _get_astral_phoenix_ascii(self):
        """ASCII art for the Astral Phoenix boss"""
        return """
         ⚔️ ASTRAL PHOENIX ⚔️
        ╭────────────────────╮
        │      /\\  /\\       │
        │    ╭┤🔥🔥├╮      │
        │   ╭│PHOENIX│╮     │
        │   ││OF STARS││     │
        │   ╰│✨ ✨│╯     │
        │    ╰──────╯       │
        │  Cosmic Firebird   │
        ╰────────────────────╯"""

    def _get_mind_flayer_ascii(self):
        """ASCII art for the Mind Flayer boss"""
        return """
         ⚔️ MIND FLAYER ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤🧠 🧠├─╮    │
        │  │ │FLAYER│ │    │
        │  │ │OF    │ │    │
        │  │ │MINDS │ │    │
        │  ╰─┤💫 💫├─╯    │
        │    ╰────────╯     │
        │  Psychic Terror    │
        ╰────────────────────╯"""

    def _get_frost_giant_ascii(self):
        """ASCII art for the Frost Giant boss"""
        return """
          ⚔️ FROST GIANT ⚔️
        ╭────────────────────╮
        │     ╭──────╮      │
        │   ╭─┤❄️ ❄️├─╮    │
        │   │ │GIANT│ │    │
        │   │ │OF   │ │    │
        │   │ │FROST│ │    │
        │   ╰─┤☃️ ☃️├─╯    │
        │     ╰──────╯      │
        │   Winter's Wrath   │
        ╰────────────────────╯"""

    def _get_plague_doctor_ascii(self):
        """ASCII art for the Plague Doctor boss"""
        return """
         ⚔️ PLAGUE DOCTOR ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤😷 😷├─╮    │
        │  │ │DOCTOR│ │    │
        │  │ │OF    │ │    │
        │  │ │PLAGUE│ │    │
        │  ╰─┤☠️ ☠️├─╯    │
        │    ╰────────╯     │
        │   Death's Hand     │
        ╰────────────────────╯"""

    def _get_dream_eater_ascii(self):
        """ASCII art for the Dream Eater boss"""
        return """
         ⚔️ DREAM EATER ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤💤 💤├─╮    │
        │  │ │EATER │ │    │
        │  │ │OF    │ │    │
        │  │ │DREAMS│ │    │
        │  ╰─┤🌙 🌙├─╯    │
        │    ╰────────╯     │
        │  Nightmare Lord    │
        ╰────────────────────╯"""

    def _get_star_weaver_ascii(self):
        """ASCII art for the Star Weaver boss"""
        return """
         ⚔️ STAR WEAVER ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤✨ ✨├─╮    │
        │  │ │WEAVER│ │    │
        │  │ │OF    │ │    │
        │  │ │STARS │ │    │
        │  ╰─┤🌟 🌟├─╯    │
        │    ╰────────╯     │
        │ Cosmic Architect  │
        ╰────────────────────╯"""

    def _get_void_serpent_ascii(self):
        """ASCII art for the Void Serpent boss"""
        return """
         ⚔️ VOID SERPENT ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤🐍 🐍├─╮    │
        │  │ │SERPENT│ │    │
        │  │ │OF THE │ │    │
        │  │ │ VOID  │ │    │
        │  ╰─┤🌌 🌌├─╯    │
        │    ╰────────╯     │
        │  Eternal Coil     │
        ╰────────────────────╯"""

    def _get_rune_master_ascii(self):
        """ASCII art for the Rune Master boss"""
        return """
         ⚔️ RUNE MASTER ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤📜 📜├─╮    │
        │  │ │MASTER│ │    │
        │  │ │OF    │ │    │
        │  │ │RUNES │ │    │
        │  ╰─┤⚡ ⚡├─╯    │
        │    ╰────────╯     │
        │  Ancient Scribe   │
        ╰────────────────────╯"""

    def _get_soul_harvester_ascii(self):
        """ASCII art for the Soul Harvester boss"""
        return """
        ⚔️ SOUL HARVESTER ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤👻 👻├─╮    │
        │  │ │REAPER│ │    │
        │  │ │OF    │ │    │
        │  │ │SOULS │ │    │
        │  ╰─┤💀 💀├─╯    │
        │    ╰────────╯     │
        │  Spirit's Bane    │
        ╰────────────────────╯"""

    def _get_storm_lord_ascii(self):
        """ASCII art for the Storm Lord boss"""
        return """
         ⚔️ STORM LORD ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤⚡ ⚡├─╮    │
        │  │ │LORD  │ │    │
        │  │ │OF    │ │    │
        │  │ │STORMS│ │    │
        │  ╰─┤🌩️ 🌩️├─╯    │
        │    ╰────────╯     │
        │ Thunder's Wrath   │
        ╰────────────────────╯"""

    def _get_crystal_sage_ascii(self):
        """ASCII art for the Crystal Sage boss"""
        return """
         ⚔️ CRYSTAL SAGE ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤💎 💎├─╮    │
        │  │ │SAGE  │ │    │
        │  │ │OF    │ │    │
        │  │ │GEMS  │ │    │
        │  ╰─┤✨ ✨├─╯    │
        │    ╰────────╯     │
        │ Prismatic Master  │
        ╰────────────────────╯"""

    def _get_abyss_walker_ascii(self):
        """ASCII art for the Abyss Walker boss"""
        return """
         ⚔️ ABYSS WALKER ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤🕳️ 🕳️├─╮    │
        │  │ │WALKER│ │    │
        │  │ │OF THE│ │    │
        │  │ │ABYSS │ │    │
        │  ╰─┤⚫ ⚫├─╯    │
        │    ╰────────╯     │
        │  Depths Strider   │
        ╰────────────────────╯"""

    def _get_chronolord_ascii(self):
        """ASCII art for the Chronolord boss"""
        return """
         ⚔️ CHRONOLORD ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤⌛ ⌛├─╮    │
        │  │ │LORD  │ │    │
        │  │ │OF    │ │    │
        │  │ │TIME  │ │    │
        │  ╰─┤⚡ ⚡├─╯    │
        │    ╰────────╯     │
        │  Time's Master    │
        ╰────────────────────╯"""

    def _get_elder_wyrm_ascii(self):
        """ASCII art for the Elder Wyrm boss"""
        return """
         ⚔️ ELDER WYRM ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤🐲 🐲├─╮    │
        │  │ │ANCIENT│ │    │
        │  │ │DRAGON │ │    │
        │  │ │KING   │ │    │
        │  ╰─┤🔥 🔥├─╯    │
        │    ╰────────╯     │
        │  Primal Fury      │
        ╰────────────────────╯"""

    def _get_nexus_guardian_ascii(self):
        """ASCII art for the Nexus Guardian boss"""
        return """
        ⚔️ NEXUS GUARDIAN ⚔️
        ╭────────────────────╮
        │    ╭────────╮     │
        │  ╭─┤🌀 🌀├─╮    │
        │  │ │KEEPER│ │    │
        │  │ │OF THE│ │    │
        │  │ │NEXUS │ │    │
        │  ╰─┤💫 💫├─╯    │
        │    ╰────────╯     │
        │  Portal's Ward    │
        ╰────────────────────╯"""

    def _get_title_screen_void_ascii(self):
        """ASCII art for the void-themed title screen"""
        return """
        ╔════════════《 ELYSIAN NEXUS 》════════════╗
        ║     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒      ║
        ║   ▒▒▒    🌌 Into The Void 🌌    ▒▒▒    ║
        ║ ▒▒▒      ╱▔▔▔▔▔▔▔▔▔▔▔▔▔╲       ▒▒▒    ║
        ║ ▒▒     ╱▔╲▂▂▂▂▂▂▂▂▂▂▂▂╱▔╲      ▒▒    ║
        ║ ▒▒    ╱▔╲▂▂▂▂E L Y S I A N▂▂╱▔╲   ▒▒    ║
        ║ ▒▒   ╱▔╲▂▂▂▂▂N E X U S▂▂▂▂╱▔╲  ▒▒    ║
        ║ ▒▒    ╲▁╱▔▔▔▔▔▔▔▔▔▔▔▔▔╲▁╱   ▒▒    ║
        ║  ▒▒▒      ╲▁▁▁▁▁▁▁▁▁▁▁▁╱    ▒▒▒     ║
        ║    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒       ║
        ║                                        ║
        ║        [1] Pierce the Veil            ║
        ║        [2] Continue Journey           ║
        ║        [3] Void Whispers              ║
        ║        [4] Configure Reality          ║
        ║        [5] Return to Light            ║
        ║                                        ║
        ║      ✧ The Void Beckons You ✧         ║
        ╚════════════════════════════════════════╝"""

    def _get_title_screen_celestial_ascii(self):
        """ASCII art for the celestial-themed title screen"""
        return """
        ✧     *    ✧    *     ✧     *    ✧
        ╭──────────《 ELYSIAN NEXUS 》──────────╮
        │           ⭐    ✨    ⭐              │
        │     .─────────────────────────.       │
        │  .─┤  Through Stars We Rise  ├─.    │
        │ /  ╰─────────────────────────╯  \\    │
        │/      ╭─────────────────╮       \\   │
        │   *   │ ELYSIAN NEXUS  │    *    │
        │       │   ✧  ⚔️  ✧    │         │
        │\\      ╰─────────────────╯       /   │
        │ \\  .─────────────────────────.  /    │
        │  `─┤    Choose Your Star    ├─'     │
        │     `─────────────────────────'      │
        │                                      │
        │      [1] Celestial Journey          │
        │      [2] Continue Ascension         │
        │      [3] Stellar Codex             │
        │      [4] Astral Settings           │
        │      [5] Return to Earth           │
        │                                      │
        │    ✧ The Stars Guide Your Path ✧    │
        ╰──────────────────────────────────────╯
        ✧     *    ✧    *     ✧     *    ✧"""

    def _get_title_screen_mystic_ascii(self):
        """ASCII art for the mystic-themed title screen"""
        return """
        🔮──────────《 ELYSIAN NEXUS 》──────────🔮
           ╭────────────────────────────╮
           │    Ancient Powers Stir     │
           │  ╭──────────────────────╮  │
           │  │  🌟 ELYSIAN 🌟   │  │
           │  │     ──●──          │  │
           │  │  ✨  NEXUS  ✨   │  │
           │  ╰──────────────────────╯  │
           │                            │
           │   [1] Begin Ritual         │
           │   [2] Resume Mysteries     │
           │   [3] Arcane Tomes         │
           │   [4] Mystical Settings    │
           │   [5] Break Meditation     │
           │                            │
           │  ~ Mysteries Await You ~   │
           ╰────────────────────────────╯
        🔮───────────────────────────────────🔮"""

    def _get_title_screen_dark_ascii(self):
        """ASCII art for the dark-themed title screen"""
        return """
        ╔═══════════《 ELYSIAN NEXUS 》═══════════╗
        ║     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ║
        ║   ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓    ║
        ║ ▓▓░░      Dark Horizons       ░░▓▓  ║
        ║ ▓░░    ╭────────────────╮     ░░▓  ║
        ║ ▓░░    │ ELYSIAN NEXUS │     ░░▓  ║
        ║ ▓░░    │   🌑  ⚔️  🌑   │     ░░▓  ║
        ║ ▓░░    ╰────────────────╯     ░░▓  ║
        ║ ▓▓░░                         ░░▓▓  ║
        ║   ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓    ║
        ║     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ║
        ║                                      ║
        ║      [1] Enter Darkness             ║
        ║      [2] Continue Shadow Path       ║
        ║      [3] Dark Knowledge             ║
        ║      [4] Shadow Settings            ║
        ║      [5] Return to Light            ║
        ║                                      ║
        ║     ~ Embrace the Darkness ~         ║
        ╚══════════════════════════════════════╝"""

    def _get_title_screen_elemental_ascii(self):
        """ASCII art for the elemental-themed title screen"""
        return """
        🌪️────────《 ELYSIAN NEXUS 》────────🔥
        │    ⚡    ❄️    💧    🌪️    ⚡     │
        ╭──────────────────────────────────╮
        │      Elemental Convergence       │
        │   ╭──────────────────────╮      │
        │   │    E L Y S I A N    │      │
        │   │  ╭──────────────╮   │      │
        │   │  │    NEXUS    │   │      │
        │   │  ╰──────────────╯   │      │
        │   ╰──────────────────────╯      │
        │                                  │
        │      [1] Elemental Journey      │
        │      [2] Continue Mastery       │
        │      [3] Element Codex          │
        │      [4] Natural Settings       │
        │      [5] Return to Balance      │
        │                                  │
        │   ~ Master the Elements ~        │
        ╰──────────────────────────────────╯
        🌊────────────────────────────────🗻"""

    def _get_title_screen_ritual_ascii(self):
        """ASCII art for the ritual-themed title screen"""
        return """
        ✨──────────《 ELYSIAN NEXUS 》──────────✨
        ╭────────────────────────────────────────╮
        │         Sacred Circle Opens             │
        │      ╭────────────────────╮           │
        │    🕯️│    E L Y S I A N  │🕯️        │
        │      │  .-──────────-.   │           │
        │    🕯️│  │   NEXUS   │   │🕯️        │
        │      │  `-──────────-'   │           │
        │    🕯️╰────────────────────╯🕯️        │
        │                                      │
        │        [1] Begin the Ritual          │
        │        [2] Continue Ceremony         │
        │        [3] Ancient Grimoire          │
        │        [4] Sacred Settings           │
        │        [5] Break the Circle          │
        │                                      │
        │     ~ The Ritual Commences ~         │
        ╰────────────────────────────────────────╯
        ✨─────────────────────────────────────✨"""

    def _get_title_screen_cosmic_ascii(self):
        """ASCII art for the cosmic-themed title screen"""
        return """
        🌠═══════《 ELYSIAN NEXUS 》═══════🌠
        ║    *  ⋆｡°✩  ☄️  ✩°｡⋆  *     ║
        ║ ╭────────────────────────╮    ║
        ║ │   Cosmic Resonance    │    ║
        ║ │  ╭────────────────╮   │    ║
        ║ │  │  E L Y S I A N │   │    ║
        ║ │  │     NEXUS      │   │    ║
        ║ │  │    ⊹  ✧  ⊹    │   │    ║
        ║ │  ╰────────────────╯   │    ║
        ║ ╰────────────────────────╯    ║
        ║                               ║
        ║    [1] Cosmic Voyage         ║
        ║    [2] Continue Orbit        ║
        ║    [3] Star Charts           ║
        ║    [4] Nebula Settings       ║
        ║    [5] Return to Earth       ║
        ║                               ║
        ║  ~ Beyond the Cosmos ~        ║
        ╚═══════════════════════════════╝"""

    def _get_title_screen_ancient_ascii(self):
        """ASCII art for the ancient-themed title screen"""
        return """
        📜═══════《 ELYSIAN NEXUS 》═══════📜
        ║     ╔════════════════════╗      ║
        ║     ║  Ancient Wisdom    ║      ║
        ║     ║ ╭──────────────╮  ║      ║
        ║     ║ │ E L Y S I A N│  ║      ║
        ║     ║ │    NEXUS     │  ║      ║
        ║     ║ │  🏺  📿  🏺  │  ║      ║
        ║     ║ ╰──────────────╯  ║      ║
        ║     ╚════════════════════╝      ║
        ║                                 ║
        ║      [1] Ancient Path          ║
        ║      [2] Continue Legacy       ║
        ║      [3] Lost Scrolls          ║
        ║      [4] Relic Settings        ║
        ║      [5] Leave Ruins           ║
        ║                                 ║
        ║    ~ Wisdom of the Ages ~       ║
        ╚═════════════════════════════════╝"""

 