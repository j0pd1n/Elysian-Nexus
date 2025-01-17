from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass

class TextSize(Enum):
    SMALL = "Small"      # 📝
    MEDIUM = "Medium"    # 📄
    LARGE = "Large"      # 📜
    EXTRA_LARGE = "Extra Large" # 📋

class ColorScheme(Enum):
    DEFAULT = "Default"          # 🎨
    HIGH_CONTRAST = "High Contrast" # 🔲
    COLORBLIND = "Colorblind"    # 👁️
    DARK_MODE = "Dark Mode"      # 🌙
    LIGHT_MODE = "Light Mode"    # ☀️

class InputMode(Enum):
    KEYBOARD = "Keyboard"     # ⌨️
    TEXT_ONLY = "Text Only"   # 📝
    NUMBERS = "Numbers Only"  # 🔢
    VOICE = "Voice"          # 🎤

class TextStyle(Enum):
    NORMAL = "Normal"          # 📄
    BOLD = "Bold"             # 📝
    SPACED = "Spaced"         # 📏
    SIMPLIFIED = "Simplified"  # 📋

class FontFamily(Enum):
    DEFAULT = "Default"        # 🔤
    DYSLEXIC = "Dyslexic"     # 📖
    MONOSPACE = "Monospace"   # ⌨️
    SANS_SERIF = "Sans Serif" # 📱

class AnimationSpeed(Enum):
    OFF = "Off"               # ⏹️
    SLOW = "Slow"            # ⏲️
    NORMAL = "Normal"        # ⏱️
    FAST = "Fast"           # ⚡

@dataclass
class KeyBinding:
    key: str
    description: str
    action: str
    category: str

@dataclass
class AccessibilityProfile:
    name: str
    text_size: TextSize
    color_scheme: ColorScheme
    text_style: TextStyle
    font_family: FontFamily
    animation_speed: AnimationSpeed
    screen_reader: bool
    auto_progress: bool
    input_mode: InputMode

class AccessibilityManager:
    def __init__(self):
        self.text_size = TextSize.MEDIUM
        self.color_scheme = ColorScheme.DEFAULT
        self.input_mode = InputMode.KEYBOARD
        self.screen_reader_enabled = False
        self.auto_progress = False
        self.key_bindings: Dict[str, KeyBinding] = {}
        self.initialize_key_bindings()
        self.text_style = TextStyle.NORMAL
        self.font_family = FontFamily.DEFAULT
        self.animation_speed = AnimationSpeed.NORMAL
        self.cursor_size = 1.0
        self.line_spacing = 1.0
        self.text_to_speech_speed = 1.0
        self.profiles: Dict[str, AccessibilityProfile] = {}
        self.initialize_profiles()
        
    def initialize_key_bindings(self):
        """Initialize default key bindings"""
        self.key_bindings = {
            # Core Menu Navigation
            "i": KeyBinding("i", "Open Inventory", "show_inventory", "menu"),
            "m": KeyBinding("m", "Open Map", "show_map", "navigation"),
            "c": KeyBinding("c", "Show Character", "show_character", "menu"),
            "j": KeyBinding("j", "Show Journal", "show_journal", "menu"),
            "q": KeyBinding("q", "Show Quests", "show_quests", "menu"),
            "p": KeyBinding("p", "Show Profile", "show_profile", "menu"),
            "h": KeyBinding("h", "Show Help", "show_help", "menu"),
            
            # System Controls
            "esc": KeyBinding("esc", "Back/Menu", "show_menu", "system"),
            "f1": KeyBinding("f1", "Toggle Help Overlay", "toggle_help", "system"),
            "f2": KeyBinding("f2", "Quick Save", "quick_save", "system"),
            "f3": KeyBinding("f3", "Quick Load", "quick_load", "system"),
            "f4": KeyBinding("f4", "Settings Menu", "show_settings", "system"),
            
            # Navigation Controls
            "tab": KeyBinding("tab", "Cycle Options", "cycle_options", "navigation"),
            "shift+tab": KeyBinding("shift+tab", "Cycle Options Reverse", "cycle_options_reverse", "navigation"),
            "space": KeyBinding("space", "Continue/Confirm", "continue_dialogue", "dialogue"),
            "enter": KeyBinding("enter", "Select/Confirm", "select_option", "navigation"),
            "up": KeyBinding("up", "Move Up", "move_up", "navigation"),
            "down": KeyBinding("down", "Move Down", "move_down", "navigation"),
            "left": KeyBinding("left", "Move Left", "move_left", "navigation"),
            "right": KeyBinding("right", "Move Right", "move_right", "navigation"),
            
            # Accessibility Toggles (Alt + key)
            "alt+s": KeyBinding("alt+s", "Toggle Screen Reader", "toggle_screen_reader", "accessibility"),
            "alt+a": KeyBinding("alt+a", "Toggle Auto-Progress", "toggle_auto_progress", "accessibility"),
            "alt+c": KeyBinding("alt+c", "Cycle Color Schemes", "cycle_color_scheme", "accessibility"),
            "alt+t": KeyBinding("alt+t", "Cycle Text Sizes", "cycle_text_size", "accessibility"),
            "alt+f": KeyBinding("alt+f", "Cycle Font Families", "cycle_font_family", "accessibility"),
            "alt+n": KeyBinding("alt+n", "Cycle Animation Speeds", "cycle_animation_speed", "accessibility"),
            
            # Quick Profile Switching (Ctrl + Number)
            "ctrl+1": KeyBinding("ctrl+1", "Default Profile", "apply_default_profile", "profile"),
            "ctrl+2": KeyBinding("ctrl+2", "High Visibility Profile", "apply_high_visibility_profile", "profile"),
            "ctrl+3": KeyBinding("ctrl+3", "Screen Reader Profile", "apply_screen_reader_profile", "profile"),
            "ctrl+4": KeyBinding("ctrl+4", "Dyslexic Friendly Profile", "apply_dyslexic_profile", "profile"),
            "ctrl+5": KeyBinding("ctrl+5", "Motor Friendly Profile", "apply_motor_profile", "profile"),
            
            # Adjustments (Ctrl + Alt + key)
            "ctrl+alt+up": KeyBinding("ctrl+alt+up", "Increase Text Size", "increase_text_size", "adjustment"),
            "ctrl+alt+down": KeyBinding("ctrl+alt+down", "Decrease Text Size", "decrease_text_size", "adjustment"),
            "ctrl+alt+right": KeyBinding("ctrl+alt+right", "Increase Line Spacing", "increase_line_spacing", "adjustment"),
            "ctrl+alt+left": KeyBinding("ctrl+alt+left", "Decrease Line Spacing", "decrease_line_spacing", "adjustment"),
            "ctrl+alt+plus": KeyBinding("ctrl+alt+plus", "Increase Cursor Size", "increase_cursor_size", "adjustment"),
            "ctrl+alt+minus": KeyBinding("ctrl+alt+minus", "Decrease Cursor Size", "decrease_cursor_size", "adjustment"),
        }
        
    def initialize_profiles(self):
        """Initialize accessibility profiles"""
        self.profiles["default"] = AccessibilityProfile(
            name="Default",
            text_size=TextSize.MEDIUM,
            color_scheme=ColorScheme.DEFAULT,
            text_style=TextStyle.NORMAL,
            font_family=FontFamily.DEFAULT,
            animation_speed=AnimationSpeed.NORMAL,
            screen_reader=False,
            auto_progress=False,
            input_mode=InputMode.KEYBOARD
        )
        
        self.profiles["high_visibility"] = AccessibilityProfile(
            name="High Visibility",
            text_size=TextSize.LARGE,
            color_scheme=ColorScheme.HIGH_CONTRAST,
            text_style=TextStyle.BOLD,
            font_family=FontFamily.SANS_SERIF,
            animation_speed=AnimationSpeed.SLOW,
            screen_reader=False,
            auto_progress=True,
            input_mode=InputMode.KEYBOARD
        )
        
        self.profiles["screen_reader"] = AccessibilityProfile(
            name="Screen Reader",
            text_size=TextSize.MEDIUM,
            color_scheme=ColorScheme.DEFAULT,
            text_style=TextStyle.NORMAL,
            font_family=FontFamily.DEFAULT,
            animation_speed=AnimationSpeed.OFF,
            screen_reader=True,
            auto_progress=True,
            input_mode=InputMode.VOICE
        )
        
        # Add new profiles for specific needs
        self.profiles["dyslexic_friendly"] = AccessibilityProfile(
            name="Dyslexic Friendly",
            text_size=TextSize.MEDIUM,
            color_scheme=ColorScheme.LIGHT_MODE,
            text_style=TextStyle.SPACED,
            font_family=FontFamily.DYSLEXIC,
            animation_speed=AnimationSpeed.SLOW,
            screen_reader=False,
            auto_progress=True,
            input_mode=InputMode.KEYBOARD
        )
        
        self.profiles["low_vision"] = AccessibilityProfile(
            name="Low Vision",
            text_size=TextSize.EXTRA_LARGE,
            color_scheme=ColorScheme.HIGH_CONTRAST,
            text_style=TextStyle.BOLD,
            font_family=FontFamily.SANS_SERIF,
            animation_speed=AnimationSpeed.SLOW,
            screen_reader=True,
            auto_progress=True,
            input_mode=InputMode.KEYBOARD
        )
        
        self.profiles["motor_friendly"] = AccessibilityProfile(
            name="Motor Friendly",
            text_size=TextSize.MEDIUM,
            color_scheme=ColorScheme.DEFAULT,
            text_style=TextStyle.NORMAL,
            font_family=FontFamily.DEFAULT,
            animation_speed=AnimationSpeed.SLOW,
            screen_reader=False,
            auto_progress=True,
            input_mode=InputMode.NUMBERS
        )
        
        self.profiles["cognitive_friendly"] = AccessibilityProfile(
            name="Cognitive Friendly",
            text_size=TextSize.MEDIUM,
            color_scheme=ColorScheme.LIGHT_MODE,
            text_style=TextStyle.SIMPLIFIED,
            font_family=FontFamily.SANS_SERIF,
            animation_speed=AnimationSpeed.SLOW,
            screen_reader=False,
            auto_progress=True,
            input_mode=InputMode.TEXT_ONLY
        )
        
        # Add specialized profiles
        self.profiles["adhd_friendly"] = AccessibilityProfile(
            name="ADHD Friendly",
            text_size=TextSize.MEDIUM,
            color_scheme=ColorScheme.LIGHT_MODE,
            text_style=TextStyle.SPACED,
            font_family=FontFamily.SANS_SERIF,
            animation_speed=AnimationSpeed.FAST,
            screen_reader=False,
            auto_progress=False,  # Manual control for better focus
            input_mode=InputMode.KEYBOARD
        )
        
        self.profiles["anxiety_friendly"] = AccessibilityProfile(
            name="Anxiety Friendly",
            text_size=TextSize.MEDIUM,
            color_scheme=ColorScheme.LIGHT_MODE,
            text_style=TextStyle.NORMAL,
            font_family=FontFamily.DEFAULT,
            animation_speed=AnimationSpeed.SLOW,  # Slower animations for reduced stress
            screen_reader=False,
            auto_progress=True,  # Auto-progress to reduce decision fatigue
            input_mode=InputMode.TEXT_ONLY
        )
        
        self.profiles["elderly_friendly"] = AccessibilityProfile(
            name="Senior Friendly",
            text_size=TextSize.LARGE,
            color_scheme=ColorScheme.HIGH_CONTRAST,
            text_style=TextStyle.SPACED,
            font_family=FontFamily.SANS_SERIF,
            animation_speed=AnimationSpeed.SLOW,
            screen_reader=True,
            auto_progress=True,
            input_mode=InputMode.NUMBERS
        )
        
        self.profiles["epilepsy_safe"] = AccessibilityProfile(
            name="Epilepsy Safe",
            text_size=TextSize.MEDIUM,
            color_scheme=ColorScheme.LIGHT_MODE,
            text_style=TextStyle.NORMAL,
            font_family=FontFamily.DEFAULT,
            animation_speed=AnimationSpeed.OFF,  # No animations
            screen_reader=False,
            auto_progress=True,
            input_mode=InputMode.KEYBOARD
        )
        
    def apply_profile(self, profile_name: str):
        """Apply an accessibility profile"""
        if profile_name in self.profiles:
            profile = self.profiles[profile_name]
            self.text_size = profile.text_size
            self.color_scheme = profile.color_scheme
            self.text_style = profile.text_style
            self.font_family = profile.font_family
            self.animation_speed = profile.animation_speed
            self.screen_reader_enabled = profile.screen_reader
            self.auto_progress = profile.auto_progress
            self.input_mode = profile.input_mode
            print(f"Applied {profile_name} profile")
            
    def adjust_cursor_size(self, size: float):
        """Adjust cursor size"""
        self.cursor_size = max(0.5, min(2.0, size))
        print(f"Cursor size set to: {self.cursor_size}x")
        
    def adjust_line_spacing(self, spacing: float):
        """Adjust line spacing"""
        self.line_spacing = max(1.0, min(2.5, spacing))
        print(f"Line spacing set to: {self.line_spacing}x")
        
    def adjust_text_to_speech_speed(self, speed: float):
        """Adjust text-to-speech speed"""
        self.text_to_speech_speed = max(0.5, min(2.0, speed))
        print(f"Text-to-speech speed set to: {self.text_to_speech_speed}x")
        
    def adjust_text_size(self, size: TextSize):
        """Change text size setting"""
        self.text_size = size
        print(f"Text size changed to: {size.value}")
        
    def change_color_scheme(self, scheme: ColorScheme):
        """Change color scheme setting"""
        self.color_scheme = scheme
        print(f"Color scheme changed to: {scheme.value}")
        
    def toggle_screen_reader(self):
        """Toggle screen reader"""
        self.screen_reader_enabled = not self.screen_reader_enabled
        status = "enabled" if self.screen_reader_enabled else "disabled"
        print(f"Screen reader {status}")
        
    def toggle_auto_progress(self):
        """Toggle auto-progress for dialogue"""
        self.auto_progress = not self.auto_progress
        status = "enabled" if self.auto_progress else "disabled"
        print(f"Auto-progress {status}")
        
    def change_input_mode(self, mode: InputMode):
        """Change input mode"""
        self.input_mode = mode
        print(f"Input mode changed to: {mode.value}")
        
    def add_key_binding(self, binding: KeyBinding):
        """Add or update a key binding"""
        self.key_bindings[binding.key] = binding
        
    def remove_key_binding(self, key: str):
        """Remove a key binding"""
        if key in self.key_bindings:
            del self.key_bindings[key]
            
    def get_key_bindings_by_category(self, category: str) -> Dict[str, KeyBinding]:
        """Get all key bindings for a category"""
        return {
            key: binding
            for key, binding in self.key_bindings.items()
            if binding.category == category
        }
        
    def format_text(self, text: str) -> str:
        """Enhanced text formatting based on accessibility settings"""
        # Apply text size
        if self.text_size == TextSize.LARGE:
            text = text.upper()
        elif self.text_size == TextSize.EXTRA_LARGE:
            text = f"\n{text.upper()}\n"
            
        # Apply text style
        if self.text_style == TextStyle.SPACED:
            text = " ".join(text)
        elif self.text_style == TextStyle.SIMPLIFIED:
            text = text.replace(";", ".").replace(",", ".")
            
        # Apply line spacing
        if self.line_spacing > 1.0:
            text = text.replace("\n", "\n" * int(self.line_spacing))
            
        # Screen reader output
        if self.screen_reader_enabled:
            print(f"Screen Reader ({self.text_to_speech_speed}x): {text}")
            
        return text 