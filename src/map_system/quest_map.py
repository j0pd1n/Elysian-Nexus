import pygame
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

class QuestType(Enum):
    """Types of quests in the game"""
    MAIN = auto()          # Main storyline quests
    FACTION = auto()       # Faction-specific quests
    SIDE = auto()          # Optional side quests
    HIDDEN = auto()        # Secret/hidden quests
    DAILY = auto()         # Daily repeatable quests
    WORLD_EVENT = auto()   # Special world event quests

class QuestStatus(Enum):
    """Status of a quest"""
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()
    LOCKED = auto()

@dataclass
class QuestNode:
    """A node in the quest map representing a quest or quest step"""
    name: str
    position: Tuple[int, int]
    quest_type: QuestType
    description: str
    level_requirement: int
    faction_requirement: Optional[str] = None
    prerequisites: List[str] = None  # List of quest names that must be completed
    status: QuestStatus = QuestStatus.LOCKED
    next_steps: List[str] = None    # List of quest names that follow this one
    alternative_paths: List[str] = None  # List of alternative quest names
    rewards: Dict = None            # Dictionary of rewards
    
    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []
        if self.next_steps is None:
            self.next_steps = []
        if self.alternative_paths is None:
            self.alternative_paths = []
        if self.rewards is None:
            self.rewards = {}

class QuestMap:
    """Development tool for creating and tracking quest lines"""
    def __init__(self):
        self.quests = {}  # Dictionary of quest nodes by name
        self.selected_quest = None
        self.hovered_quest = None
    
    def add_quest(self, quest: QuestNode):
        """Add a quest to the map"""
        self.quests[quest.name] = quest
    
    def get_quest(self, name: str) -> Optional[QuestNode]:
        """Get a quest by name"""
        return self.quests.get(name)
    
    def get_available_quests(self, player_level: int, faction: Optional[str] = None) -> List[QuestNode]:
        """Get all quests available to a player"""
        available = []
        for quest in self.quests.values():
            if (quest.level_requirement <= player_level and
                (not quest.faction_requirement or quest.faction_requirement == faction) and
                all(self.quests[prereq].status == QuestStatus.COMPLETED 
                    for prereq in quest.prerequisites)):
                available.append(quest)
        return available

class QuestMapWindow:
    """Development window for visualizing and editing quest lines"""
    def __init__(self, size=(1200, 800)):
        pygame.init()
        pygame.font.init()
        
        self.size = size
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Elysian Nexus - Quest Map (Development)")
        
        self.font = pygame.font.SysFont('consolas', 14)
        
        # Colors for different quest types
        self.colors = {
            QuestType.MAIN: (255, 200, 100),      # Gold for main quests
            QuestType.FACTION: (100, 200, 255),   # Blue for faction quests
            QuestType.SIDE: (200, 255, 100),      # Green for side quests
            QuestType.HIDDEN: (200, 100, 255),    # Purple for hidden quests
            QuestType.DAILY: (255, 100, 200),     # Pink for daily quests
            QuestType.WORLD_EVENT: (255, 100, 100) # Red for world events
        }
        
        self.quest_map = QuestMap()
        self.camera_pos = [size[0] // 2, size[1] // 2]
        self.zoom_level = 1.0
        self.dragging = False
        self.drag_start = (0, 0)
    
    def draw(self):
        """Draw the quest map"""
        # Clear screen
        self.screen.fill((5, 5, 15))  # Dark background
        
        # Draw connections between quests
        for quest in self.quest_map.quests.values():
            start_pos = self.world_to_screen(quest.position)
            
            # Draw lines to next quest steps
            for next_quest_name in quest.next_steps:
                if next_quest_name in self.quest_map.quests:
                    next_quest = self.quest_map.quests[next_quest_name]
                    end_pos = self.world_to_screen(next_quest.position)
                    pygame.draw.line(self.screen, (100, 100, 150), start_pos, end_pos, 2)
            
            # Draw dashed lines to alternative paths
            for alt_quest_name in quest.alternative_paths:
                if alt_quest_name in self.quest_map.quests:
                    alt_quest = self.quest_map.quests[alt_quest_name]
                    end_pos = self.world_to_screen(alt_quest.position)
                    self.draw_dashed_line(start_pos, end_pos, (150, 150, 200))
        
        # Draw quest nodes
        for quest in self.quest_map.quests.values():
            self.draw_quest_node(quest)
        
        # Draw UI elements
        if self.quest_map.hovered_quest:
            self.draw_quest_tooltip(self.quest_map.hovered_quest)
        
        pygame.display.flip()
    
    def draw_quest_node(self, quest: QuestNode):
        """Draw a quest node"""
        screen_pos = self.world_to_screen(quest.position)
        color = self.colors[quest.quest_type]
        
        # Draw node
        pygame.draw.circle(self.screen, color, screen_pos, 8)
        
        # Draw status indicator
        if quest.status == QuestStatus.COMPLETED:
            pygame.draw.circle(self.screen, (100, 255, 100), screen_pos, 4)
        elif quest.status == QuestStatus.IN_PROGRESS:
            pygame.draw.circle(self.screen, (255, 255, 100), screen_pos, 4)
        elif quest.status == QuestStatus.FAILED:
            pygame.draw.circle(self.screen, (255, 100, 100), screen_pos, 4)
        
        # Draw quest name if zoomed in enough
        if self.zoom_level > 0.5:
            text = self.font.render(quest.name, True, color)
            text_pos = (screen_pos[0] - text.get_width() // 2,
                       screen_pos[1] + 10)
            self.screen.blit(text, text_pos)
    
    def draw_dashed_line(self, start_pos, end_pos, color, dash_length=10):
        """Draw a dashed line between two points"""
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = (dx * dx + dy * dy) ** 0.5
        dashes = int(distance / dash_length)
        
        for i in range(dashes):
            start = (start_pos[0] + dx * i / dashes,
                    start_pos[1] + dy * i / dashes)
            end = (start_pos[0] + dx * (i + 0.5) / dashes,
                  start_pos[1] + dy * (i + 0.5) / dashes)
            pygame.draw.line(self.screen, color, start, end, 2)
    
    def draw_quest_tooltip(self, quest: QuestNode):
        """Draw tooltip with quest information"""
        lines = [
            quest.name,
            f"Type: {quest.quest_type.name}",
            f"Level: {quest.level_requirement}",
            f"Status: {quest.status.name}"
        ]
        if quest.faction_requirement:
            lines.append(f"Faction: {quest.faction_requirement}")
        
        # Calculate tooltip dimensions
        line_height = 20
        width = max(self.font.size(line)[0] for line in lines) + 20
        height = len(lines) * line_height + 10
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        x = mouse_pos[0] + 15
        y = mouse_pos[1] + 15
        
        # Keep tooltip on screen
        if x + width > self.size[0]:
            x = self.size[0] - width
        if y + height > self.size[1]:
            y = self.size[1] - height
        
        # Draw tooltip
        pygame.draw.rect(self.screen, (10, 20, 30), (x, y, width, height))
        pygame.draw.rect(self.screen, (100, 100, 150), (x, y, width, height), 1)
        
        for i, line in enumerate(lines):
            text = self.font.render(line, True, (200, 200, 255))
            self.screen.blit(text, (x + 10, y + 5 + i * line_height))
    
    def world_to_screen(self, world_pos):
        """Convert world coordinates to screen coordinates"""
        screen_x = (world_pos[0] - self.camera_pos[0]) * self.zoom_level + self.size[0] / 2
        screen_y = (world_pos[1] - self.camera_pos[1]) * self.zoom_level + self.size[1] / 2
        return (int(screen_x), int(screen_y))
    
    def screen_to_world(self, screen_pos):
        """Convert screen coordinates to world coordinates"""
        world_x = (screen_pos[0] - self.size[0] / 2) / self.zoom_level + self.camera_pos[0]
        world_y = (screen_pos[1] - self.size[1] / 2) / self.zoom_level + self.camera_pos[1]
        return (world_x, world_y)
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.QUIT:
            return False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.dragging = True
                self.drag_start = event.pos
            elif event.button == 4:  # Mouse wheel up
                self.zoom_level = min(2.0, self.zoom_level * 1.1)
            elif event.button == 5:  # Mouse wheel down
                self.zoom_level = max(0.5, self.zoom_level / 1.1)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.drag_start[0]
                dy = event.pos[1] - self.drag_start[1]
                self.camera_pos[0] -= dx / self.zoom_level
                self.camera_pos[1] -= dy / self.zoom_level
                self.drag_start = event.pos
        
        return True
    
    def run(self):
        """Main window loop"""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                running = self.handle_event(event)
            
            self.draw()
            clock.tick(60)

def main():
    """Initialize and run the quest map window"""
    try:
        print("Initializing quest map window...")
        window = QuestMapWindow()
        
        # Example quest nodes for testing
        main_quest_1 = QuestNode(
            name="The Awakening",
            position=(0, 0),
            quest_type=QuestType.MAIN,
            description="Discover your destiny as the chosen one",
            level_requirement=1
        )
        
        faction_quest_1 = QuestNode(
            name="Mystic Initiation",
            position=(100, 100),
            quest_type=QuestType.FACTION,
            description="Join the Mystic Order",
            level_requirement=5,
            faction_requirement="Mystic Order",
            prerequisites=["The Awakening"]
        )
        
        # Add quests to the map
        window.quest_map.add_quest(main_quest_1)
        window.quest_map.add_quest(faction_quest_1)
        
        print("Starting quest map window...")
        window.run()
        
    except Exception as e:
        print(f"Error running quest map window: {str(e)}\n")
        print("Traceback:")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main() 