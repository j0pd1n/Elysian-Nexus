import random
import math
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

# ASCII Art Constants
TITLE_ART = """
███████╗██╗  ██╗   ██╗███████╗██╗ █████╗ ███╗   ██╗
██╔════╝██║  ╚██╗ ██╔╝██╔════╝██║██╔══██╗████╗  ██║
█████╗  ██║   ╚████╔╝ ███████╗██║███████║██╔██╗ ██║
██╔══╝  ██║    ╚██╔╝  ╚════██║██║██╔══██║██║╚██╗██║
███████╗███████╗██║   ███████║██║██║  ██║██║ ╚████║
╚══════╝╚══════╝╚═╝   ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                 ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
                 ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
                 ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
                 ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
                 ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
                 ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"""

MENU_BORDER = """╔════════════════════════╗
{}
╚════════════════════════╝"""

# Core Enums
class ArtStyle(Enum):
    BLOCK = "block"
    SHADOW = "shadow"
    OUTLINE = "outline"
    GRADIENT = "gradient"
    NEON = "neon"
    PIXEL = "pixel"
    DECORATIVE = "decorative"
    MINIMAL = "minimal"

class VisualTheme(Enum):
    DEFAULT = "default"
    MYSTICAL = "mystical"
    DARK = "dark"
    NATURE = "nature"
    CELESTIAL = "celestial"
    ARCANE = "arcane"
    ETHEREAL = "ethereal"
    ELEMENTAL = "elemental"

class EnvironmentMood(Enum):
    PEACEFUL = "peaceful"
    TENSE = "tense"
    DANGEROUS = "dangerous"
    MYSTICAL = "mystical"
    CORRUPTED = "corrupted"

class AnimationType(Enum):
    FADE = "fade"
    SLIDE = "slide"
    GLITCH = "glitch"
    RIPPLE = "ripple"
    MATRIX = "matrix"
    WAVE = "wave"
    PULSE = "pulse"
    TYPEWRITER = "typewriter"

# Core Data Classes
@dataclass
class ArtConfig:
    style: ArtStyle
    theme: VisualTheme = VisualTheme.DEFAULT
    mood: EnvironmentMood = EnvironmentMood.PEACEFUL
    width: int = 80
    height: int = 24
    animation_type: Optional[AnimationType] = None
    animation_frames: int = 1
    animation_speed: float = 1.0
    particle_effects: bool = False
    use_color: bool = True

@dataclass
class Frame:
    content: List[str]
    delay: float = 0.1
    effects: List[str] = field(default_factory=list)
    color_map: Dict[str, str] = field(default_factory=dict)

@dataclass
class Animation:
    frames: List[Frame]
    loop: bool = False
    total_duration: float = 1.0
    current_frame: int = 0

class AsciiArtSystem:
    def __init__(self):
        self.art_cache: Dict[str, Animation] = {}
        self.block_chars = {
            'solid': '█',
            'shades': ['░', '▒', '▓', '█'],
            'box': ['┌', '┐', '└', '┘', '─', '│'],
            'double': ['╔', '╗', '╚', '╝', '═', '║']
        }
        
    def create_text_art(self, text: str, config: ArtConfig) -> Animation:
        """Create ASCII art from text with specified configuration"""
        base_frame = self._generate_base_frame(text, config)
        
        if config.animation_type:
            frames = self._create_animation(base_frame, config)
        else:
            frames = [Frame(content=base_frame)]
            
        animation = Animation(
            frames=frames,
            loop=config.animation_frames > 1,
            total_duration=config.animation_frames * config.animation_speed
        )
        
        return animation
        
    def _generate_base_frame(self, text: str, config: ArtConfig) -> List[str]:
        """Generate the base frame based on style"""
        if config.style == ArtStyle.BLOCK:
            return self._create_block_style(text, config)
        elif config.style == ArtStyle.SHADOW:
            return self._create_shadow_style(text, config)
        elif config.style == ArtStyle.OUTLINE:
            return self._create_outline_style(text, config)
        elif config.style == ArtStyle.NEON:
            return self._create_neon_style(text, config)
        else:
            return self._create_minimal_style(text, config)

    def _create_block_style(self, text: str, config: ArtConfig) -> List[str]:
        """Create block-style ASCII art"""
        block_patterns = {
            'A': [
                "  ▄▄▄  ",
                " █   █ ",
                "█████ ",
                "█   █ ",
                "█   █ "
            ],
            # Add more letters...
        }
        
        result = []
        height = 5  # Standard height for block letters
        
        for i in range(height):
            line = ""
            for char in text.upper():
                if char in block_patterns:
                    line += block_patterns[char][i] + " "
                else:
                    line += " " * 8
            result.append(line)
            
        return self._apply_theme(result, config)

    def _create_shadow_style(self, text: str, config: ArtConfig) -> List[str]:
        """Create shadow-style ASCII art"""
        base = self._create_block_style(text, config)
        result = []
        
        for i, line in enumerate(base):
            result.append(line)
            if i < len(base) - 1:
                shadow = line.replace('█', '▓').replace('▓', '▒').replace('▒', '░')
                result.append(" " + shadow)
                
        return result

    def _create_outline_style(self, text: str, config: ArtConfig) -> List[str]:
        """Create outline-style ASCII art"""
        base = self._create_minimal_style(text, config)
        result = []
        
        width = max(len(line) for line in base)
        result.append("╔" + "═" * width + "╗")
        
        for line in base:
            result.append("║" + line + "║")
            
        result.append("╚" + "═" * width + "╝")
        
        return result

    def _create_neon_style(self, text: str, config: ArtConfig) -> List[str]:
        """Create neon-style ASCII art"""
        base = self._create_block_style(text, config)
        result = []
        
        for line in base:
            glow = line.replace('█', '░')
            result.extend([glow, line, glow])
            
        return result

    def _create_minimal_style(self, text: str, config: ArtConfig) -> List[str]:
        """Create minimal ASCII art"""
        return [text]

    def _create_animation(self, base_frame: List[str], config: ArtConfig) -> List[Frame]:
        """Create animation frames based on animation type"""
        frames = []
        
        if config.animation_type == AnimationType.FADE:
            frames = self._create_fade_animation(base_frame, config)
        elif config.animation_type == AnimationType.GLITCH:
            frames = self._create_glitch_animation(base_frame, config)
        elif config.animation_type == AnimationType.MATRIX:
            frames = self._create_matrix_animation(base_frame, config)
        elif config.animation_type == AnimationType.WAVE:
            frames = self._create_wave_animation(base_frame, config)
            
        return frames

    def _create_fade_animation(self, base_frame: List[str], config: ArtConfig) -> List[Frame]:
        """Create fade in/out animation"""
        frames = []
        fade_chars = " .:-=+*#%@"
        
        for i in range(config.animation_frames):
            progress = i / (config.animation_frames - 1)
            frame_content = []
            
            for line in base_frame:
                new_line = ""
                for char in line:
                    if char != " ":
                        fade_index = int(progress * (len(fade_chars) - 1))
                        new_line += fade_chars[fade_index]
                    else:
                        new_line += " "
                frame_content.append(new_line)
                
            frames.append(Frame(
                content=frame_content,
                delay=config.animation_speed / config.animation_frames
            ))
            
        return frames

    def _create_glitch_animation(self, base_frame: List[str], config: ArtConfig) -> List[Frame]:
        """Create glitch effect animation"""
        frames = []
        
        for _ in range(config.animation_frames):
            frame_content = base_frame.copy()
            
            # Add random glitch effects
            for _ in range(random.randint(1, 3)):
                line_idx = random.randint(0, len(frame_content) - 1)
                glitch_chars = "!@#$%^&*"
                glitch = random.choice(glitch_chars) * random.randint(3, 8)
                
                line = frame_content[line_idx]
                pos = random.randint(0, max(0, len(line) - len(glitch)))
                frame_content[line_idx] = (
                    line[:pos] + glitch + line[pos + len(glitch):]
                )
                
            frames.append(Frame(
                content=frame_content,
                delay=config.animation_speed / config.animation_frames
            ))
            
        return frames

    def _create_matrix_animation(self, base_frame: List[str], config: ArtConfig) -> List[Frame]:
        """Create Matrix-style digital rain animation"""
        frames = []
        matrix_chars = "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ"
        
        for i in range(config.animation_frames):
            frame_content = []
            for line in base_frame:
                new_line = ""
                for char in line:
                    if char != " " and random.random() < i / config.animation_frames:
                        new_line += random.choice(matrix_chars)
                    else:
                        new_line += char
                frame_content.append(new_line)
                
            frames.append(Frame(
                content=frame_content,
                delay=config.animation_speed / config.animation_frames
            ))
            
        return frames

    def _create_wave_animation(self, base_frame: List[str], config: ArtConfig) -> List[Frame]:
        """Create wave effect animation"""
        frames = []
        
        for i in range(config.animation_frames):
            frame_content = []
            phase = (2 * math.pi * i) / config.animation_frames
            
            for y, line in enumerate(base_frame):
                offset = int(math.sin(phase + y/2) * 3)
                frame_content.append(" " * max(0, offset) + line)
                
            frames.append(Frame(
                content=frame_content,
                delay=config.animation_speed / config.animation_frames
            ))
            
        return frames

    def _apply_theme(self, content: List[str], config: ArtConfig) -> List[str]:
        """Apply visual theme to content"""
        if not config.use_color:
            return content
            
        theme_colors = {
            VisualTheme.MYSTICAL: "\033[35m",  # Purple
            VisualTheme.DARK: "\033[30m",      # Black
            VisualTheme.NATURE: "\033[32m",    # Green
            VisualTheme.CELESTIAL: "\033[36m", # Cyan
            VisualTheme.ARCANE: "\033[34m",    # Blue
            VisualTheme.ETHEREAL: "\033[37m",  # White
            VisualTheme.ELEMENTAL: "\033[31m"  # Red
        }
        
        if config.theme in theme_colors:
            color = theme_colors[config.theme]
            reset = "\033[0m"
            return [f"{color}{line}{reset}" for line in content]
            
        return content

    def render_animation(self, animation: Animation) -> None:
        """Render an animation to the console"""
        try:
            while True:
                frame = animation.frames[animation.current_frame]
                
                # Clear screen
                print("\033[H\033[J")
                
                # Print frame
                print("\n".join(frame.content))
                
                # Update frame counter
                animation.current_frame = (animation.current_frame + 1) % len(animation.frames)
                
                # Delay
                time.sleep(frame.delay)
                
                if not animation.loop and animation.current_frame == 0:
                    break
                    
        except KeyboardInterrupt:
            print("\033[H\033[J")  # Clear screen on exit 