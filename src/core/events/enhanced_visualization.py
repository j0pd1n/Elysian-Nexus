from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
from .event_manager import Event, EventType
from .event_visualization import EventIcon, EventNode
from ..ui_system import UIComponent, TextStyle, ColorScheme

class VisualizationMode(Enum):
    COMPACT = "compact"
    DETAILED = "detailed"
    TIMELINE = "timeline"
    NETWORK = "network"

class EventCategory(Enum):
    MAIN = "main"
    SIDE = "side"
    HIDDEN = "hidden"
    COMPLETED = "completed"
    ACTIVE = "active"
    BLOCKED = "blocked"

@dataclass
class VisualTheme:
    background_color: str
    text_color: str
    border_color: str
    highlight_color: str
    connection_color: str
    node_colors: Dict[EventCategory, str]

class EnhancedEventVisualization:
    def __init__(self):
        self.event_nodes: Dict[str, EventNode] = {}
        self.grid_size = (30, 30)  # Increased grid size
        self.occupied_positions: Set[Tuple[int, int]] = set()
        self.ui_components: Dict[str, UIComponent] = {}
        self.current_mode = VisualizationMode.DETAILED
        self.selected_event: Optional[str] = None
        self.visible_categories: Set[EventCategory] = {
            EventCategory.MAIN,
            EventCategory.ACTIVE,
            EventCategory.COMPLETED
        }
        self.theme = self._create_default_theme()

    def _create_default_theme(self) -> VisualTheme:
        """Create default visual theme"""
        return VisualTheme(
            background_color="#1E1E1E",
            text_color="#FFFFFF",
            border_color="#404040",
            highlight_color="#007ACC",
            connection_color="#606060",
            node_colors={
                EventCategory.MAIN: "#4CAF50",      # Green
                EventCategory.SIDE: "#FFA726",      # Orange
                EventCategory.HIDDEN: "#757575",    # Gray
                EventCategory.COMPLETED: "#2196F3",  # Blue
                EventCategory.ACTIVE: "#F44336",    # Red
                EventCategory.BLOCKED: "#9C27B0"    # Purple
            }
        )

    def add_event_node(self, event: Event, description: str, effects: List[str], 
                      category: EventCategory = EventCategory.MAIN) -> bool:
        """Add a new event node with enhanced visualization"""
        if event.event_id in self.event_nodes:
            return False
            
        position = self._find_optimal_position(event)
        if not position:
            return False
            
        icon = self._get_event_icon(event.event_type)
        
        node = EventNode(
            event=event,
            position=position,
            connections=[],
            status="pending",
            icon=icon,
            description=description,
            effects=effects
        )
        
        self.event_nodes[event.event_id] = node
        self.occupied_positions.add(position)
        
        # Create enhanced UI component
        self._create_enhanced_ui_component(event.event_id, node, category)
        
        return True

    def _find_optimal_position(self, event: Event) -> Optional[Tuple[int, int]]:
        """Find optimal position based on event type and relationships"""
        if not self.event_nodes:
            return (self.grid_size[0] // 2, self.grid_size[1] // 2)
            
        # Try to group similar event types together
        similar_events = [
            node for node in self.event_nodes.values()
            if node.event.event_type == event.event_type
        ]
        
        if similar_events:
            # Find center of similar events
            center_x = sum(node.position[0] for node in similar_events) // len(similar_events)
            center_y = sum(node.position[1] for node in similar_events) // len(similar_events)
            
            # Search for nearest unoccupied position
            for radius in range(1, max(self.grid_size)):
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        pos = (center_x + dx, center_y + dy)
                        if self._is_valid_position(pos):
                            return pos
        
        # Fallback to simple search
        return self._find_available_position()

    def _is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is valid"""
        x, y = pos
        return (
            0 <= x < self.grid_size[0] and
            0 <= y < self.grid_size[1] and
            pos not in self.occupied_positions
        )

    def _find_available_position(self) -> Optional[Tuple[int, int]]:
        """Find any available position"""
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                pos = (x, y)
                if pos not in self.occupied_positions:
                    return pos
        return None

    def _create_enhanced_ui_component(self, event_id: str, node: EventNode, category: EventCategory):
        """Create enhanced UI component with interactive features"""
        position = self._grid_to_screen_position(node.position)
        
        component = UIComponent(
            id=f"event_{event_id}",
            position=position,
            size=(200, 150),  # Larger size for more detail
            style=TextStyle.NORMAL,
            color_scheme=ColorScheme.DEFAULT
        )
        
        # Add interactive elements
        component.add_click_handler(lambda: self.select_event(event_id))
        component.add_hover_handler(lambda: self.highlight_connections(event_id))
        
        # Set visual properties based on category
        component.background_color = self.theme.node_colors[category]
        component.border_color = self.theme.border_color
        
        self.ui_components[event_id] = component

    def select_event(self, event_id: str):
        """Handle event selection"""
        self.selected_event = event_id
        self._update_visualization()

    def highlight_connections(self, event_id: str):
        """Highlight connected events"""
        if event_id in self.event_nodes:
            node = self.event_nodes[event_id]
            for connected_id in node.connections:
                if connected_id in self.ui_components:
                    self.ui_components[connected_id].border_color = self.theme.highlight_color

    def set_visualization_mode(self, mode: VisualizationMode):
        """Change visualization mode"""
        self.current_mode = mode
        self._update_visualization()

    def _update_visualization(self):
        """Update visualization based on current mode and selection"""
        if self.current_mode == VisualizationMode.COMPACT:
            self._apply_compact_layout()
        elif self.current_mode == VisualizationMode.TIMELINE:
            self._apply_timeline_layout()
        elif self.current_mode == VisualizationMode.NETWORK:
            self._apply_network_layout()
            
        self._update_ui_components()

    def _apply_compact_layout(self):
        """Apply compact visualization layout"""
        visible_nodes = [
            node for node in self.event_nodes.values()
            if self._should_show_node(node)
        ]
        
        # Arrange nodes in a grid
        grid_width = int(len(visible_nodes) ** 0.5) + 1
        for i, node in enumerate(visible_nodes):
            x = i % grid_width
            y = i // grid_width
            node.position = (x * 2, y * 2)

    def _apply_timeline_layout(self):
        """Apply timeline visualization layout"""
        visible_nodes = [
            node for node in self.event_nodes.values()
            if self._should_show_node(node)
        ]
        
        # Sort nodes by event chain and timing
        visible_nodes.sort(key=lambda n: (n.event.chain_id or "", n.event.duration))
        
        # Arrange in timeline
        current_y = 0
        current_chain = None
        for node in visible_nodes:
            if node.event.chain_id != current_chain:
                current_y += 2
                current_chain = node.event.chain_id
            node.position = (current_y, len(node.connections))

    def _apply_network_layout(self):
        """Apply network visualization layout"""
        # Implement force-directed graph layout
        iterations = 100
        k = 1.0  # Spring constant
        
        # Initialize random positions
        import random
        for node in self.event_nodes.values():
            node.position = (
                random.randint(0, self.grid_size[0] - 1),
                random.randint(0, self.grid_size[1] - 1)
            )
            
        # Apply force-directed algorithm
        for _ in range(iterations):
            self._apply_force_iteration(k)

    def _apply_force_iteration(self, k: float):
        """Apply one iteration of force-directed layout"""
        forces = {event_id: [0, 0] for event_id in self.event_nodes}
        
        # Calculate repulsive forces
        for node1_id, node1 in self.event_nodes.items():
            for node2_id, node2 in self.event_nodes.items():
                if node1_id != node2_id:
                    dx = node1.position[0] - node2.position[0]
                    dy = node1.position[1] - node2.position[1]
                    distance = max(0.1, (dx * dx + dy * dy) ** 0.5)
                    force = k * k / distance
                    forces[node1_id][0] += force * dx / distance
                    forces[node1_id][1] += force * dy / distance
                    
        # Calculate attractive forces
        for node_id, node in self.event_nodes.items():
            for connected_id in node.connections:
                if connected_id in self.event_nodes:
                    connected = self.event_nodes[connected_id]
                    dx = node.position[0] - connected.position[0]
                    dy = node.position[1] - connected.position[1]
                    distance = max(0.1, (dx * dx + dy * dy) ** 0.5)
                    force = distance * distance / k
                    forces[node_id][0] -= force * dx / distance
                    forces[node_id][1] -= force * dy / distance
                    
        # Apply forces
        for node_id, force in forces.items():
            node = self.event_nodes[node_id]
            new_x = max(0, min(self.grid_size[0] - 1, node.position[0] + force[0]))
            new_y = max(0, min(self.grid_size[1] - 1, node.position[1] + force[1]))
            node.position = (int(new_x), int(new_y))

    def _should_show_node(self, node: EventNode) -> bool:
        """Determine if a node should be visible"""
        if self.selected_event:
            # Show selected node and its connections
            return (
                node.event.event_id == self.selected_event or
                node.event.event_id in self.event_nodes[self.selected_event].connections
            )
        return True

    def _update_ui_components(self):
        """Update UI components based on current layout"""
        for event_id, node in self.event_nodes.items():
            if event_id in self.ui_components:
                component = self.ui_components[event_id]
                component.position = self._grid_to_screen_position(node.position)
                component.visible = self._should_show_node(node)

    def render_event_details(self, event_id: str) -> str:
        """Render detailed information about an event"""
        if event_id not in self.event_nodes:
            return "Event not found"
            
        node = self.event_nodes[event_id]
        event = node.event
        
        details = [
            f"Event: {event.name}",
            f"Status: {node.status}",
            f"Type: {event.event_type.value}",
            f"Duration: {event.duration // 3600}h {(event.duration % 3600) // 60}m",
            "",
            "Description:",
            node.description,
            "",
            "Effects:",
            *[f"- {effect}" for effect in node.effects],
            "",
            "Connected Events:",
            *[f"- {self.event_nodes[conn].event.name}" for conn in node.connections if conn in self.event_nodes]
        ]
        
        return "\n".join(details)

    def export_visualization(self, format: str = "ascii") -> str:
        """Export visualization in specified format"""
        if format == "ascii":
            return self._export_ascii()
        elif format == "json":
            return self._export_json()
        return "Unsupported format"

    def _export_ascii(self) -> str:
        """Export visualization as ASCII art"""
        grid = [[" " for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
        
        # Draw connections
        for node in self.event_nodes.values():
            if self._should_show_node(node):
                for connected_id in node.connections:
                    if connected_id in self.event_nodes:
                        connected = self.event_nodes[connected_id]
                        if self._should_show_node(connected):
                            self._draw_connection(grid, node.position, connected.position)
                            
        # Draw nodes
        for node in self.event_nodes.values():
            if self._should_show_node(node):
                x, y = node.position
                grid[y][x] = node.icon.value
                
        return "\n".join("".join(row) for row in grid)

    def _export_json(self) -> str:
        """Export visualization as JSON"""
        import json
        
        data = {
            "nodes": [
                {
                    "id": event_id,
                    "name": node.event.name,
                    "type": node.event.event_type.value,
                    "status": node.status,
                    "position": node.position,
                    "connections": node.connections
                }
                for event_id, node in self.event_nodes.items()
                if self._should_show_node(node)
            ]
        }
        
        return json.dumps(data, indent=2) 