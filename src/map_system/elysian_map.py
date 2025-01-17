from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple, Union
import pygame
from pygame import Surface, Color
import math
import random

class TerrainType(Enum):
    """Terrain types with associated visual styles"""
    PLAINS = ("Plains", "✧")
    FOREST = ("Forest", "❈")
    MOUNTAIN = ("Mountain", "▲")
    WATER = ("Water", "≈")
    DESERT = ("Desert", "◇")
    VOID = ("Void", "▼")
    ASTRAL = ("Astral", "✦")

class LocationCategory(Enum):
    """Categories of locations with associated icons"""
    CITY = ("City", "🏰")
    DUNGEON = ("Dungeon", "⚔️")
    SHRINE = ("Shrine", "✨")
    QUEST_HUB = ("Quest Hub", "📜")
    MERCHANT = ("Merchant", "💰")
    CRAFTING = ("Crafting", "⚒️")
    UNKNOWN = ("Unknown", "❓")

class FactionInfluence(Enum):
    """Factions with their visual themes"""
    MYSTIC_ORDER = {
        "name": "Mystic Order",
        "primary": "#934FDA",  # Deep purple
        "secondary": "#6A1B9A",
        "accent": "#B39DDB",
        "icon": "✨"
    }
    TECH_SYNDICATE = {
        "name": "Tech Syndicate",
        "primary": "#00BCD4",  # Cyan
        "secondary": "#006064",
        "accent": "#80DEEA",
        "icon": "⚡"
    }
    SHADOW_LEGION = {
        "name": "Shadow Legion",
        "primary": "#D32F2F",  # Red
        "secondary": "#B71C1C",
        "accent": "#EF9A9A",
        "icon": "🌑"
    }
    NATURE_PACT = {
        "name": "Nature Pact",
        "primary": "#4CAF50",  # Green
        "secondary": "#1B5E20",
        "accent": "#A5D6A7",
        "icon": "🌿"
    }
    ASTRAL_COUNCIL = {
        "name": "Astral Council",
        "primary": "#FFD700",  # Gold
        "secondary": "#FFA000",
        "accent": "#FFE082",
        "icon": "⭐"
    }

@dataclass
class MapTheme:
    """Visual theme configuration for the map"""
    background_color: str = "#1A1F3D"  # Deep navy from design system
    grid_color: str = "#2A2F4D"        # Rich purple from design system
    highlight_color: str = "#FFD700"    # Golden accent
    text_color: str = "#FFFFFF"         # Primary text
    secondary_text: str = "#CCCCCC"     # Secondary text
    disabled_text: str = "#666666"      # Disabled text
    
    # Animation timings from design system
    transition_duration: int = 300       # milliseconds
    hover_delay: int = 300              # milliseconds for tooltips
    
    # Fonts from design system
    header_font: str = "Cinzel"
    body_font: str = "Open Sans"
    system_font: str = "Roboto Mono"
    
    # Sizes
    grid_size: int = 60
    node_size: int = 20
    tooltip_max_width: int = 300

@dataclass
class MapLocation:
    """Enhanced location class with visual properties"""
    name: str
    position: Tuple[int, int]
    category: LocationCategory
    terrain: TerrainType
    description: str
    faction_influence: Dict[FactionInfluence, float] = field(default_factory=dict)
    discovered: bool = False
    points_of_interest: List[str] = field(default_factory=list)
    danger_level: int = 1
    resources: List[str] = field(default_factory=list)
    weather_effects: List[str] = field(default_factory=list)
    
    def get_display_icon(self) -> str:
        """Get the appropriate icon based on location properties"""
        if not self.discovered:
            return LocationCategory.UNKNOWN.value[1]
        return self.category.value[1]
    
    def get_influence_color(self) -> str:
        """Get the dominant faction color"""
        if not self.faction_influence:
            return MapTheme.grid_color
        
        dominant_faction = max(
            self.faction_influence.items(),
            key=lambda x: x[1]
        )[0]
        return dominant_faction.value["primary"]

class ElysianMapRenderer:
    """Advanced map renderer with design system integration"""
    
    def __init__(self, size: Tuple[int, int], theme: MapTheme = MapTheme()):
        self.size = size
        self.theme = theme
        self.zoom_level = 1.0
        self.camera_pos = [size[0] // 2, size[1] // 2]
        self.hover_location = None
        self.selected_location = None
        
        # Initialize visual effects
        self._init_effects()
    
    def _init_effects(self):
        """Initialize visual effect parameters"""
        self.particle_systems = {}
        self.glow_surfaces = {}
        self.animation_timers = {}
        
    def render(self, world_map) -> Surface:
        """Main render method"""
        # Create main surface
        surface = Surface(self.size, pygame.SRCALPHA)
        surface.fill(pygame.Color(self.theme.background_color))
        
        # Render layers in order
        self._render_grid(surface)
        self._render_terrain(surface, world_map)
        self._render_connections(surface, world_map)
        self._render_locations(surface, world_map)
        self._render_effects(surface)
        self._render_ui_elements(surface)
        
        return surface
    
    def _render_grid(self, surface):
        """Render the styled grid"""
        grid_color = pygame.Color(self.theme.grid_color)
        alpha = 30  # Subtle grid
        
        for x in range(0, self.size[0], self.theme.grid_size):
            pygame.draw.line(surface, (*grid_color, alpha), 
                           (x, 0), (x, self.size[1]))
        
        for y in range(0, self.size[1], self.theme.grid_size):
            pygame.draw.line(surface, (*grid_color, alpha),
                           (0, y), (self.size[0], y))
    
    def _render_terrain(self, surface, world_map):
        """Render terrain with styled effects"""
        for pos, location in world_map.locations.items():
            if not location.discovered:
                continue
                
            screen_pos = self._transform_point(*pos)
            terrain_icon = location.terrain.value[1]
            
            # Draw terrain marker with glow effect
            self._draw_terrain_marker(surface, screen_pos, terrain_icon, location)
    
    def _render_connections(self, surface, world_map):
        """Render path connections with effects"""
        for start, ends in world_map.connections.items():
            start_pos = self._transform_point(*start)
            
            for end in ends:
                if not world_map.locations[end].discovered:
                    continue
                    
                end_pos = self._transform_point(*end)
                self._draw_connection(surface, start_pos, end_pos,
                                   world_map.locations[start],
                                   world_map.locations[end])
    
    def _render_locations(self, surface, world_map):
        """Render location markers with effects"""
        for pos, location in world_map.locations.items():
            screen_pos = self._transform_point(*pos)
            
            # Draw location marker with appropriate styling
            self._draw_location_marker(surface, screen_pos, location)
            
            # Draw hover effects if applicable
            if location == self.hover_location:
                self._draw_hover_effects(surface, screen_pos, location)
            
            # Draw selection effects if applicable
            if location == self.selected_location:
                self._draw_selection_effects(surface, screen_pos, location)
    
    def _draw_terrain_marker(self, surface, pos, icon, location):
        """Draw styled terrain marker"""
        font = pygame.font.SysFont(self.theme.system_font, 16)
        text = font.render(icon, True, pygame.Color(self.theme.secondary_text))
        text_rect = text.get_rect(center=pos)
        
        # Draw with slight glow effect
        glow_surf = pygame.Surface((text_rect.width + 4, text_rect.height + 4),
                                 pygame.SRCALPHA)
        glow_color = pygame.Color(location.get_influence_color())
        pygame.draw.rect(glow_surf, (*glow_color, 30),
                        glow_surf.get_rect(), border_radius=2)
        
        surface.blit(glow_surf, text_rect.inflate(4, 4))
        surface.blit(text, text_rect)
    
    def _draw_connection(self, surface, start, end, start_loc, end_loc):
        """Draw styled connection between locations"""
        # Calculate connection properties based on faction influence
        color = pygame.Color(self.theme.grid_color)
        width = 2
        
        # Draw main connection line
        pygame.draw.line(surface, color, start, end, width)
        
        # Add particle effects if either location is selected/hovered
        if (start_loc in (self.hover_location, self.selected_location) or
            end_loc in (self.hover_location, self.selected_location)):
            self._add_connection_particles(surface, start, end)
    
    def _draw_location_marker(self, surface, pos, location):
        """Draw styled location marker"""
        icon = location.get_display_icon()
        font = pygame.font.SysFont(self.theme.body_font, 20)
        text = font.render(icon, True, pygame.Color(self.theme.text_color))
        text_rect = text.get_rect(center=pos)
        
        # Draw marker background
        bg_color = pygame.Color(location.get_influence_color())
        pygame.draw.circle(surface, (*bg_color, 50),
                         pos, self.theme.node_size)
        
        # Draw icon
        surface.blit(text, text_rect)
    
    def _draw_hover_effects(self, surface, pos, location):
        """Draw hover effects for location"""
        # Create tooltip
        tooltip_surface = self._create_tooltip(location)
        tooltip_pos = (pos[0] + 20, pos[1] - 20)
        
        # Draw tooltip with fade-in effect
        alpha = min(255, self.animation_timers.get(location, 0))
        tooltip_surface.set_alpha(alpha)
        surface.blit(tooltip_surface, tooltip_pos)
        
        # Update animation timer
        self.animation_timers[location] = min(255,
            self.animation_timers.get(location, 0) + 15)
    
    def _create_tooltip(self, location) -> Surface:
        """Create styled tooltip surface"""
        # Create tooltip content
        lines = [
            f"{location.name} - {location.category.value[0]}",
            f"Terrain: {location.terrain.value[0]}",
            f"Danger Level: {'⚔️' * location.danger_level}",
        ]
        
        if location.points_of_interest:
            lines.append("\nPoints of Interest:")
            lines.extend(f"• {poi}" for poi in location.points_of_interest)
        
        # Create tooltip surface
        font = pygame.font.SysFont(self.theme.body_font, 14)
        line_surfaces = [font.render(line, True,
                                   pygame.Color(self.theme.text_color))
                        for line in lines]
        
        # Calculate tooltip size
        width = max(surf.get_width() for surf in line_surfaces) + 20
        height = sum(surf.get_height() for surf in line_surfaces) + 20
        
        # Create tooltip surface with background
        tooltip = Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(tooltip, (26, 31, 61, 230), tooltip.get_rect(),
                        border_radius=4)
        
        # Draw content
        y = 10
        for surf in line_surfaces:
            tooltip.blit(surf, (10, y))
            y += surf.get_height()
        
        return tooltip
    
    def _transform_point(self, x: int, y: int) -> Tuple[int, int]:
        """Transform grid coordinates to screen coordinates"""
        screen_x = (x * self.theme.grid_size * self.zoom_level +
                   self.camera_pos[0])
        screen_y = (y * self.theme.grid_size * self.zoom_level +
                   self.camera_pos[1])
        return (int(screen_x), int(screen_y)) 
    
    def _render_effects(self, surface):
        """Render visual effects layer"""
        # Render any active particle systems
        for pos, particles in self.particle_systems.items():
            for particle in particles:
                pygame.draw.circle(surface, particle['color'],
                                 particle['position'],
                                 particle['size'])
    
    def _render_ui_elements(self, surface):
        """Render UI elements layer"""
        if self.selected_location:
            self._draw_selection_effects(surface,
                self._transform_point(*self.selected_location.position),
                self.selected_location)
    
    def _draw_selection_effects(self, surface, pos, location):
        """Draw selection effects for location"""
        # Draw pulsing selection ring
        pulse = abs(math.sin(pygame.time.get_ticks() / 500)) * 0.5 + 0.5
        ring_size = self.theme.node_size + 10 * pulse
        
        color = pygame.Color(self.theme.highlight_color)
        pygame.draw.circle(surface, (*color, 100),
                         pos, ring_size, 2)
        
        # Draw additional selection indicators
        self._draw_selection_indicators(surface, pos, location)
    
    def _draw_selection_indicators(self, surface, pos, location):
        """Draw additional selection indicators"""
        angle = pygame.time.get_ticks() / 1000
        for i in range(4):
            indicator_angle = angle + i * math.pi / 2
            indicator_pos = (
                pos[0] + math.cos(indicator_angle) * (self.theme.node_size + 15),
                pos[1] + math.sin(indicator_angle) * (self.theme.node_size + 15)
            )
            
            color = pygame.Color(self.theme.highlight_color)
            pygame.draw.circle(surface, color, 
                             (int(indicator_pos[0]), int(indicator_pos[1])), 3)
    
    def _add_connection_particles(self, surface, start, end):
        """Add particles to connection"""
        if (start, end) not in self.particle_systems:
            self.particle_systems[(start, end)] = []
        
        # Calculate direction vector
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return
            
        dx /= length
        dy /= length
        
        # Add new particles
        particles = self.particle_systems[(start, end)]
        
        if len(particles) < 10:  # Limit number of particles
            particles.append({
                'position': [start[0], start[1]],
                'velocity': [dx * 2, dy * 2],
                'color': pygame.Color(self.theme.highlight_color),
                'size': 2,
                'life': 1.0
            })
        
        # Update existing particles
        for particle in particles[:]:
            # Move particle
            particle['position'][0] += particle['velocity'][0]
            particle['position'][1] += particle['velocity'][1]
            
            # Update life
            particle['life'] -= 0.02
            if particle['life'] <= 0:
                particles.remove(particle)
            else:
                # Draw particle
                pos = (int(particle['position'][0]),
                      int(particle['position'][1]))
                color = particle['color']
                pygame.draw.circle(surface, (*color, int(255 * particle['life'])),
                                 pos, particle['size']) 