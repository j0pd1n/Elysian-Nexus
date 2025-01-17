import pygame
from typing import Dict, List, Optional, Tuple
from ..combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect, Position
from ..combat_system.dimensional_abilities import DimensionalAbility, DimensionalAbilityManager

class DimensionalCombatUI:
    """UI manager for dimensional combat"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 32)
        
        # Colors for different dimensions
        self.dimension_colors = {
            DimensionalLayer.PHYSICAL: (200, 200, 200),    # Gray
            DimensionalLayer.ETHEREAL: (150, 200, 255),    # Light Blue
            DimensionalLayer.VOID: (100, 0, 100),          # Dark Purple
            DimensionalLayer.CELESTIAL: (255, 215, 0),     # Gold
            DimensionalLayer.PRIMORDIAL: (255, 50, 50)     # Red
        }
        
        # Colors for different effects
        self.effect_colors = {
            DimensionalEffect.RESONANCE: (0, 255, 0),      # Green
            DimensionalEffect.DISSONANCE: (255, 0, 0),     # Red
            DimensionalEffect.PHASING: (0, 255, 255),      # Cyan
            DimensionalEffect.ANCHORING: (128, 128, 128),  # Gray
            DimensionalEffect.WARPING: (255, 0, 255)       # Magenta
        }
        
        # UI element positions
        self.stability_bar_rect = pygame.Rect(10, 10, 200, 20)
        self.effects_start_pos = (10, 40)
        self.abilities_start_pos = (screen_width - 210, 10)
        self.dimension_indicator_pos = (screen_width // 2, 10)
        
    def draw_stability_bar(self, 
                         surface: pygame.Surface,
                         current_stability: float,
                         dimension: DimensionalLayer):
        """Draw the dimensional stability bar"""
        # Background
        pygame.draw.rect(surface, (50, 50, 50), self.stability_bar_rect)
        
        # Stability fill
        fill_width = int(self.stability_bar_rect.width * current_stability)
        fill_rect = pygame.Rect(
            self.stability_bar_rect.left,
            self.stability_bar_rect.top,
            fill_width,
            self.stability_bar_rect.height
        )
        pygame.draw.rect(surface, self.dimension_colors[dimension], fill_rect)
        
        # Stability text
        stability_text = f"Stability: {int(current_stability * 100)}%"
        text_surface = self.font.render(stability_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            centerx=self.stability_bar_rect.centerx,
            centery=self.stability_bar_rect.centery
        )
        surface.blit(text_surface, text_rect)
        
    def draw_active_effects(self,
                          surface: pygame.Surface,
                          effects: Set[DimensionalEffect]):
        """Draw active dimensional effects"""
        current_y = self.effects_start_pos[1]
        
        for effect in effects:
            effect_color = self.effect_colors[effect]
            
            # Effect icon (circle)
            pygame.draw.circle(
                surface,
                effect_color,
                (self.effects_start_pos[0] + 10, current_y + 10),
                8
            )
            
            # Effect name
            text_surface = self.font.render(effect.name, True, effect_color)
            surface.blit(
                text_surface,
                (self.effects_start_pos[0] + 25, current_y)
            )
            
            current_y += 25
            
    def draw_ability_list(self,
                         surface: pygame.Surface,
                         abilities: List[DimensionalAbility],
                         cooldowns: Dict[str, Dict[DimensionalLayer, float]]):
        """Draw the list of available abilities"""
        current_y = self.abilities_start_pos[1]
        
        for ability in abilities:
            # Ability background
            ability_rect = pygame.Rect(
                self.abilities_start_pos[0],
                current_y,
                200,
                50
            )
            pygame.draw.rect(surface, (40, 40, 40), ability_rect)
            
            # Ability name
            name_surface = self.font.render(ability.name, True, (255, 255, 255))
            surface.blit(
                name_surface,
                (ability_rect.left + 5, current_y + 5)
            )
            
            # Cooldown overlay
            max_cooldown = max(cooldowns[ability.name].values())
            if max_cooldown > 0:
                cooldown_text = f"{max_cooldown:.1f}s"
                cooldown_surface = self.font.render(cooldown_text, True, (255, 0, 0))
                surface.blit(
                    cooldown_surface,
                    (ability_rect.right - 45, current_y + 5)
                )
                
                # Darken ability if on cooldown
                cooldown_overlay = pygame.Surface(ability_rect.size, pygame.SRCALPHA)
                cooldown_overlay.fill((0, 0, 0, 128))
                surface.blit(cooldown_overlay, ability_rect)
            
            current_y += 60
            
    def draw_dimension_indicator(self,
                               surface: pygame.Surface,
                               current_dimension: DimensionalLayer,
                               connected_dimensions: Set[DimensionalLayer]):
        """Draw the current dimension and available transitions"""
        # Current dimension
        dimension_color = self.dimension_colors[current_dimension]
        center_x = self.dimension_indicator_pos[0]
        center_y = self.dimension_indicator_pos[1] + 30
        
        # Main dimension circle
        pygame.draw.circle(surface, dimension_color, (center_x, center_y), 20)
        
        # Connected dimensions
        angle_step = 2 * math.pi / len(DimensionalLayer)
        current_angle = 0
        radius = 60
        
        for dimension in DimensionalLayer:
            if dimension != current_dimension:
                x = center_x + radius * math.cos(current_angle)
                y = center_y + radius * math.sin(current_angle)
                
                # Draw connection line if connected
                if dimension in connected_dimensions:
                    pygame.draw.line(
                        surface,
                        (100, 100, 100),
                        (center_x, center_y),
                        (x, y),
                        2
                    )
                
                # Draw dimension circle
                pygame.draw.circle(
                    surface,
                    self.dimension_colors[dimension],
                    (int(x), int(y)),
                    15
                )
                
                current_angle += angle_step
                
    def draw_dimensional_effects(self,
                               surface: pygame.Surface,
                               position: Position,
                               effects: Set[DimensionalEffect]):
        """Draw visual effects for dimensional abilities"""
        for effect in effects:
            if effect == DimensionalEffect.RESONANCE:
                self._draw_resonance_effect(surface, position)
            elif effect == DimensionalEffect.WARPING:
                self._draw_warping_effect(surface, position)
            elif effect == DimensionalEffect.PHASING:
                self._draw_phasing_effect(surface, position)
                
    def _draw_resonance_effect(self, surface: pygame.Surface, position: Position):
        """Draw resonance visual effect"""
        current_time = pygame.time.get_ticks() / 1000.0
        radius = 20 + 10 * math.sin(current_time * 4)
        
        for i in range(3):
            alpha = int(255 * (1 - i/3))
            effect_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(
                effect_surface,
                (*self.effect_colors[DimensionalEffect.RESONANCE], alpha),
                (radius, radius),
                radius - i*5
            )
            surface.blit(
                effect_surface,
                (position.x - radius, position.y - radius)
            )
            
    def _draw_warping_effect(self, surface: pygame.Surface, position: Position):
        """Draw warping visual effect"""
        current_time = pygame.time.get_ticks() / 1000.0
        points = []
        
        for i in range(8):
            angle = i * math.pi / 4 + current_time
            radius = 20 + 5 * math.sin(angle * 2)
            x = position.x + radius * math.cos(angle)
            y = position.y + radius * math.sin(angle)
            points.append((x, y))
            
        pygame.draw.polygon(
            surface,
            self.effect_colors[DimensionalEffect.WARPING],
            points
        )
            
    def _draw_phasing_effect(self, surface: pygame.Surface, position: Position):
        """Draw phasing visual effect"""
        current_time = pygame.time.get_ticks() / 1000.0
        alpha = int(128 + 127 * math.sin(current_time * 3))
        
        effect_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(
            effect_surface,
            (*self.effect_colors[DimensionalEffect.PHASING], alpha),
            (20, 20),
            20
        )
        surface.blit(
            effect_surface,
            (position.x - 20, position.y - 20)
        )
        
    def draw_stability_warning(self,
                             surface: pygame.Surface,
                             stability: float):
        """Draw warning when dimensional stability is low"""
        if stability < 0.3:
            warning_color = (255, 0, 0) if pygame.time.get_ticks() % 1000 < 500 else (200, 0, 0)
            warning_text = "! LOW STABILITY !"
            text_surface = self.large_font.render(warning_text, True, warning_color)
            text_rect = text_surface.get_rect(
                center=(self.screen_width // 2, 50)
            )
            surface.blit(text_surface, text_rect)
            
    def draw_dimension_transition(self,
                                surface: pygame.Surface,
                                from_dim: DimensionalLayer,
                                to_dim: DimensionalLayer,
                                progress: float):
        """Draw dimension transition effect"""
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        # Interpolate between dimension colors
        from_color = self.dimension_colors[from_dim]
        to_color = self.dimension_colors[to_dim]
        
        current_color = tuple(
            int(from_color[i] * (1 - progress) + to_color[i] * progress)
            for i in range(3)
        )
        
        # Create transition effect
        alpha = int(128 * math.sin(progress * math.pi))
        overlay.fill((*current_color, alpha))
        
        # Add ripple effect
        ripple_radius = int(progress * max(self.screen_width, self.screen_height))
        pygame.draw.circle(
            overlay,
            (*current_color, 0),
            (self.screen_width // 2, self.screen_height // 2),
            ripple_radius,
            5
        )
        
        surface.blit(overlay, (0, 0))
        
    def update(self, delta_time: float):
        """Update any animated UI elements"""
        # Add any animation updates here
        pass 