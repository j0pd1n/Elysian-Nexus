from enum import Enum
from typing import Dict, List, Optional
import os
import time
import random

class TextColor(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"

class TextStyle(Enum):
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    RESET = "\033[0m"

class VisualEffect(Enum):
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    TYPEWRITER = "typewriter"
    GLITCH = "glitch"
    SHIMMER = "shimmer"
    PULSE = "pulse"

class VisualSystem:
    def __init__(self):
        self.effects_enabled = True
        self.animation_speed = 1.0
        self.current_color = TextColor.WHITE
        self.current_style = TextStyle.RESET
        
        # Special characters for effects
        self.special_chars = {
            "stars": ["✦", "✧", "✨", "⋆", "✯", "✰"],
            "cosmic": ["◈", "◇", "◆", "❖", "❈", "✴"],
            "void": ["▲", "△", "◄", "►", "▼", "▽"],
            "glitch": ["█", "▓", "▒", "░", "■", "□"]
        }
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def set_color(self, color: TextColor):
        """Set the current text color"""
        self.current_color = color
    
    def set_style(self, style: TextStyle):
        """Set the current text style"""
        self.current_style = style
    
    def format_text(self, text: str, color: TextColor = None, style: TextStyle = None) -> str:
        """Format text with color and style"""
        color = color or self.current_color
        style = style or self.current_style
        return f"{color.value}{style.value}{text}{TextStyle.RESET.value}{TextColor.RESET.value}"
    
    def apply_effect(self, text: str, effect: VisualEffect, speed: float = 1.0):
        """Apply a visual effect to text"""
        if not self.effects_enabled:
            print(text)
            return
        
        speed *= self.animation_speed
        
        if effect == VisualEffect.FADE_IN:
            self._fade_in_effect(text, speed)
        elif effect == VisualEffect.FADE_OUT:
            self._fade_out_effect(text, speed)
        elif effect == VisualEffect.TYPEWRITER:
            self._typewriter_effect(text, speed)
        elif effect == VisualEffect.GLITCH:
            self._glitch_effect(text, speed)
        elif effect == VisualEffect.SHIMMER:
            self._shimmer_effect(text, speed)
        elif effect == VisualEffect.PULSE:
            self._pulse_effect(text, speed)
    
    def _fade_in_effect(self, text: str, speed: float):
        """Create a fade-in effect"""
        colors = [
            TextColor.BLACK,
            TextColor.BLUE,
            TextColor.CYAN,
            TextColor.WHITE
        ]
        
        for color in colors:
            self.clear_screen()
            print(self.format_text(text, color))
            time.sleep(0.1 * speed)
    
    def _fade_out_effect(self, text: str, speed: float):
        """Create a fade-out effect"""
        colors = [
            TextColor.WHITE,
            TextColor.CYAN,
            TextColor.BLUE,
            TextColor.BLACK
        ]
        
        for color in colors:
            self.clear_screen()
            print(self.format_text(text, color))
            time.sleep(0.1 * speed)
    
    def _typewriter_effect(self, text: str, speed: float):
        """Create a typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.05 * speed)
        print()
    
    def _glitch_effect(self, text: str, speed: float):
        """Create a glitch effect"""
        glitch_chars = self.special_chars["glitch"]
        original_chars = list(text)
        
        for _ in range(3):  # Number of glitch iterations
            # Create glitch version
            glitch_text = original_chars.copy()
            num_glitches = random.randint(1, len(text) // 3)
            
            for _ in range(num_glitches):
                pos = random.randint(0, len(text) - 1)
                glitch_text[pos] = random.choice(glitch_chars)
            
            self.clear_screen()
            print(''.join(glitch_text))
            time.sleep(0.1 * speed)
            
            # Show original
            self.clear_screen()
            print(text)
            time.sleep(0.2 * speed)
    
    def _shimmer_effect(self, text: str, speed: float):
        """Create a shimmering effect"""
        colors = [
            TextColor.CYAN,
            TextColor.WHITE,
            TextColor.YELLOW,
            TextColor.WHITE
        ]
        
        for _ in range(3):  # Number of shimmer cycles
            for color in colors:
                self.clear_screen()
                print(self.format_text(text, color))
                time.sleep(0.1 * speed)
    
    def _pulse_effect(self, text: str, speed: float):
        """Create a pulsing effect"""
        styles = [
            TextStyle.BOLD,
            TextStyle.RESET,
            TextStyle.DIM,
            TextStyle.RESET
        ]
        
        for _ in range(2):  # Number of pulse cycles
            for style in styles:
                self.clear_screen()
                print(self.format_text(text, style=style))
                time.sleep(0.2 * speed)
    
    def create_loading_bar(self, progress: float, width: int = 20) -> str:
        """Create a cosmic-themed loading bar"""
        filled_width = int(width * progress)
        empty_width = width - filled_width
        
        bar = "█" * filled_width + "░" * empty_width
        percentage = int(progress * 100)
        
        return f"[{bar}] {percentage}%"
    
    def create_starfield(self, width: int, height: int) -> str:
        """Create a random starfield effect"""
        stars = self.special_chars["stars"]
        field = []
        
        for _ in range(height):
            row = []
            for _ in range(width):
                if random.random() < 0.1:  # 10% chance of star
                    row.append(random.choice(stars))
                else:
                    row.append(" ")
            field.append("".join(row))
        
        return "\n".join(field)
    
    def create_border(self, text: str, style: str = "cosmic") -> str:
        """Create a decorated border around text"""
        width = len(max(text.split('\n'), key=len)) + 4
        
        if style == "cosmic":
            chars = self.special_chars["cosmic"]
            top = f"{chars[0]}{'═' * (width-2)}{chars[1]}"
            bottom = f"{chars[2]}{'═' * (width-2)}{chars[3]}"
        else:  # Default style
            top = f"╔{'═' * (width-2)}╗"
            bottom = f"╚{'═' * (width-2)}╝"
        
        bordered = [top]
        for line in text.split('\n'):
            bordered.append(f"║ {line:<{width-4}} ║")
        bordered.append(bottom)
        
        return "\n".join(bordered)
    
    def create_combat_feedback(self, action: str, damage: int, is_critical: bool) -> str:
        """Create formatted combat feedback"""
        if is_critical:
            return self.format_text(
                f"✨ CRITICAL! {action} deals {damage} damage! ✨",
                TextColor.YELLOW,
                TextStyle.BOLD
            )
        return self.format_text(
            f"⚔️ {action} deals {damage} damage",
            TextColor.WHITE
        )
    
    def create_notification(self, message: str, is_important: bool = False) -> str:
        """Create a formatted notification"""
        if is_important:
            return self.format_text(
                f"❗ {message} ❗",
                TextColor.YELLOW,
                TextStyle.BOLD
            )
        return self.format_text(
            f"📢 {message}",
            TextColor.CYAN
        )
    
    def create_quest_update(self, title: str, status: str) -> str:
        """Create a formatted quest update"""
        return self.create_border(
            f"Quest Update: {title}\n{status}",
            "cosmic"
        )
    
    def create_item_pickup(self, item_name: str, quantity: int = 1) -> str:
        """Create a formatted item pickup notification"""
        return self.format_text(
            f"🎁 Obtained {quantity}x {item_name}",
            TextColor.GREEN
        )
    
    def create_level_up(self, level: int, stats: Dict[str, int]) -> str:
        """Create a formatted level up announcement"""
        message = [
            f"✨ LEVEL UP! ✨",
            f"You are now level {level}!",
            "\nStat Increases:"
        ]
        
        for stat, value in stats.items():
            message.append(f"  {stat}: +{value}")
        
        return self.create_border("\n".join(message), "cosmic") 