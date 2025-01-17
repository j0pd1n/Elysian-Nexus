import pygame
import sys
from elysian_map import (
    TerrainType, LocationCategory, FactionInfluence,
    MapTheme, MapLocation, ElysianMapRenderer
)

class WorldMap:
    """Test world map class"""
    def __init__(self):
        self.locations = {}
        self.connections = {}
        self._init_test_locations()
        
    def _init_test_locations(self):
        # Create some test locations
        self.locations[(5, 5)] = MapLocation(
            name="Mystic Haven",
            position=(5, 5),
            category=LocationCategory.CITY,
            terrain=TerrainType.PLAINS,
            description="A city of magical learning",
            faction_influence={
                FactionInfluence.MYSTIC_ORDER: 0.8,
                FactionInfluence.TECH_SYNDICATE: 0.2
            },
            discovered=True,
            points_of_interest=[
                "Grand Library",
                "Mage's Tower",
                "Enchanted Market"
            ],
            danger_level=1
        )
        
        self.locations[(7, 4)] = MapLocation(
            name="Shadow Keep",
            position=(7, 4),
            category=LocationCategory.DUNGEON,
            terrain=TerrainType.MOUNTAIN,
            description="An ancient fortress corrupted by dark forces",
            faction_influence={
                FactionInfluence.SHADOW_LEGION: 0.9
            },
            discovered=True,
            points_of_interest=[
                "Dark Altar",
                "Corrupted Halls"
            ],
            danger_level=4
        )
        
        self.locations[(3, 6)] = MapLocation(
            name="Nature's Sanctuary",
            position=(3, 6),
            category=LocationCategory.SHRINE,
            terrain=TerrainType.FOREST,
            description="A sacred grove of the Nature Pact",
            faction_influence={
                FactionInfluence.NATURE_PACT: 0.7,
                FactionInfluence.ASTRAL_COUNCIL: 0.3
            },
            discovered=True,
            points_of_interest=[
                "Ancient Tree",
                "Healing Springs"
            ],
            danger_level=2
        )
        
        self.locations[(6, 7)] = MapLocation(
            name="Tech Haven",
            position=(6, 7),
            category=LocationCategory.MERCHANT,
            terrain=TerrainType.CITY,
            description="A hub of technological innovation",
            faction_influence={
                FactionInfluence.TECH_SYNDICATE: 0.9
            },
            discovered=True,
            points_of_interest=[
                "Gadget Market",
                "Innovation Labs"
            ],
            danger_level=1
        )
        
        self.locations[(4, 3)] = MapLocation(
            name="Astral Nexus",
            position=(4, 3),
            category=LocationCategory.QUEST_HUB,
            terrain=TerrainType.ASTRAL,
            description="A convergence of celestial energies",
            faction_influence={
                FactionInfluence.ASTRAL_COUNCIL: 0.8
            },
            discovered=True,
            points_of_interest=[
                "Star Chamber",
                "Prophet's Sanctum"
            ],
            danger_level=3
        )
        
        # Add connections between locations
        self.connections[(5, 5)] = [(7, 4), (3, 6), (6, 7)]
        self.connections[(7, 4)] = [(5, 5), (6, 7)]
        self.connections[(3, 6)] = [(5, 5), (4, 3)]
        self.connections[(6, 7)] = [(5, 5), (7, 4)]
        self.connections[(4, 3)] = [(3, 6)]

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up display
    size = (1024, 768)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Elysian Nexus - World Map")
    
    # Create map objects
    world_map = WorldMap()
    map_renderer = ElysianMapRenderer(size)
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # Update hover location
                mouse_pos = pygame.mouse.get_pos()
                # Convert mouse position to grid coordinates and find nearest location
                # This is a simplified version - you'd want proper hit detection
                for pos, location in world_map.locations.items():
                    screen_pos = map_renderer._transform_point(*pos)
                    distance = ((mouse_pos[0] - screen_pos[0])**2 + 
                              (mouse_pos[1] - screen_pos[1])**2)**0.5
                    if distance < map_renderer.theme.node_size:
                        map_renderer.hover_location = location
                        break
                else:
                    map_renderer.hover_location = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Update selected location
                if map_renderer.hover_location:
                    map_renderer.selected_location = map_renderer.hover_location
        
        # Clear screen
        screen.fill(pygame.Color(map_renderer.theme.background_color))
        
        # Render map
        map_surface = map_renderer.render(world_map)
        screen.blit(map_surface, (0, 0))
        
        # Update display
        pygame.display.flip()
        
        # Cap framerate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 