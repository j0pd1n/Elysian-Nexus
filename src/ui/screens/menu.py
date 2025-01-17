import pygame
from ui import UIManager, UIComponent, UIButton

class Menu(UIManager):
    def __init__(self):
        super().__init__()
        self.components = []

        # Create menu buttons with vibrant colors
        self.start_button = UIButton(100, 100, 200, 50, "Start Game", bg_color=(0, 128, 255), hover_color=(51, 153, 255))
        self.options_button = UIButton(100, 200, 200, 50, "Options", bg_color=(34, 177, 76), hover_color=(77, 210, 123))
        self.quit_button = UIButton(100, 300, 200, 50, "Quit Game", bg_color=(237, 28, 36), hover_color=(255, 77, 77))

        # Add buttons to menu
        self.add_component(self.start_button)
        self.add_component(self.options_button)
        self.add_component(self.quit_button)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_hovered():
                print("Start game clicked")
                # Start game logic here
            elif self.options_button.is_hovered():
                print("Options clicked")
                # Options logic here
            elif self.quit_button.is_hovered():
                print("Quit game clicked")
                # Quit game logic here

    def render(self, screen):
        super().render(screen)
        for button in [self.start_button, self.options_button, self.quit_button]:
            button.render(screen)


class OptionsMenu(UIManager):
    def __init__(self):
        super().__init__()
        self.components = []

        # Create options buttons with vibrant colors
        self.sound_button = UIButton(100, 100, 200, 50, "Sound Settings", bg_color=(0, 128, 255), hover_color=(51, 153, 255))
        self.graphics_button = UIButton(100, 200, 200, 50, "Graphics Settings", bg_color=(34, 177, 76), hover_color=(77, 210, 123))
        self.back_button = UIButton(100, 300, 200, 50, "Back", bg_color=(237, 28, 36), hover_color=(255, 77, 77))

        # Add buttons to options menu
        self.add_component(self.sound_button)
        self.add_component(self.graphics_button)
        self.add_component(self.back_button)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.sound_button.is_hovered():
                print("Sound settings clicked")
                # Sound settings logic here
            elif self.graphics_button.is_hovered():
                print("Graphics settings clicked")
                # Graphics settings logic here
            elif self.back_button.is_hovered():
                print("Back clicked")
                # Back logic here

    def render(self, screen):
        super().render(screen)
        for button in [self.sound_button, self.graphics_button, self.back_button]:
            button.render(screen)