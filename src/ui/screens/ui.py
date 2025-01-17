import pygame

class UIManager:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def update(self):
        for component in self.components:
            component.update()

    def render(self, screen):
        for component in self.components:
            component.render(screen)

    def handle_event(self, event):
        for component in self.components:
            component.handle_event(event)

class UIComponent:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self):
        pass

    def render(self, screen):
        pass

    def handle_event(self, event):
        pass

class UIButton(UIComponent):
    def __init__(self, x, y, width, height, text, bg_color=(0, 0, 255), hover_color=(51, 153, 255)):
        super().__init__(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.current_color = bg_color

    def is_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height

    def render(self, screen):
        if self.is_hovered():
            self.current_color = self.hover_color
        else:
            self.current_color = self.bg_color
        pygame.draw.rect(screen, self.current_color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered():
                print(f"Button '{self.text}' clicked")

class UIDialogueBox(UIComponent):
    def __init__(self, x, y, width, height, text="", font_size=24):
        super().__init__(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.lines = self.wrap_text(self.text)
        self.visible_lines = []
        self.font = pygame.font.Font(None, font_size)

    def wrap_text(self, text):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            if self.font.size(line + word)[0] < self.width - 10:
                line += f"{word} "
            else:
                lines.append(line.strip())
                line = f"{word} "
        lines.append(line.strip())
        return lines

    def update(self):
        if self.lines:
            self.visible_lines.append(self.lines.pop(0))

    def render(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height), 2)
        for i, line in enumerate(self.visible_lines[-3:]):
            text_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (self.x + 10, self.y + 10 + i * self.font_size))

class UIInventory(UIComponent):
    def __init__(self, x, y, slot_size, rows, columns):
        super().__init__(x, y, slot_size * columns, slot_size * rows)
        self.slot_size = slot_size
        self.rows = rows
        self.columns = columns
        self.items = [[None for _ in range(columns)] for _ in range(rows)]

    def render(self, screen):
        for row in range(self.rows):
            for col in range(self.columns):
                slot_x = self.x + col * self.slot_size
                slot_y = self.y + row * self.slot_size
                pygame.draw.rect(screen, (100, 100, 100), (slot_x, slot_y, self.slot_size, self.slot_size))
                pygame.draw.rect(screen, (200, 200, 200), (slot_x, slot_y, self.slot_size, self.slot_size), 2)
                if self.items[row][col]:
                    item_surface = pygame.font.Font(None, 36).render(self.items[row][col], True, (255, 255, 255))
                    screen.blit(item_surface, (slot_x + 10, slot_y + 10))

class UIQuestLog(UIComponent):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.quests = []

    def add_quest(self, title, description):
        self.quests.append({"title": title, "description": description})

    def render(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)
        for i, quest in enumerate(self.quests):
            title_surface = font.render(f"{i + 1}. {quest['title']}", True, (255, 255, 0))
            screen.blit(title_surface, (self.x + 10, self.y + 10 + i * 30))

class UIStatPanel(UIComponent):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.stats = {"Health": 100, "Mana": 50, "Stamina": 75}

    def render(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)
        y_offset = 10
        for stat, value in self.stats.items():
            text_surface = font.render(f"{stat}: {value}", True, (255, 255, 255))
            screen.blit(text_surface, (self.x + 10, self.y + y_offset))
            y_offset += 30

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.active_scene = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def switch_to(self, name):
        if name in self.scenes:
            self.active_scene = self.scenes[name]

    def render(self, screen):
        if self.active_scene:
            self.active_scene.render(screen)

    def handle_event(self, event):
        if self.active_scene:
            self.active_scene.handle_event(event)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    ui_manager = UIManager()

    dialogue_box = UIDialogueBox(10, 10, 300, 200, "Hello, this is a dialogue box")
    inventory = UIInventory(320, 10, 50, 5, 5)
    quest_log = UIQuestLog(10, 220, 300, 200)
    stat_panel = UIStatPanel(320, 220, 300, 200)

    ui_manager.add_component(dialogue_box)
    ui_manager.add_component(inventory)
    ui_manager.add_component(quest_log)
    ui_manager.add_component(stat_panel)

    start_button = UIButton(10, 450, 100, 50, "Start")
    options_button = UIButton(120, 450, 100, 50, "Options")
    quit_button = UIButton(230, 450, 100, 50, "Quit")

    ui_manager.add_component(start_button)
    ui_manager.add_component(options_button)
    ui_manager.add_component(quit_button)

    scene_manager = SceneManager()
    main_scene = ui_manager
    scene_manager.add_scene("main", main_scene)
    scene_manager.switch_to("main")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene_manager.handle_event(event)

        screen.fill((0, 0, 0))
        scene_manager.render(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()