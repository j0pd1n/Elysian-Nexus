from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from .event_manager import Event, EventType
from ..ui_system import UIComponent, TextStyle, ColorScheme

class EventIcon(Enum):
    FACTION = "⚔️"  # Crossed swords for faction events
    COMBAT = "🛡️"   # Shield for combat events
    RITUAL = "✨"    # Sparkles for ritual events
    CELESTIAL = "🌟" # Star for celestial events
    TERRITORY = "🏰" # Castle for territory events
    ALLIANCE = "🤝"  # Handshake for alliance events
    WARNING = "⚠️"   # Warning for important events
    SUCCESS = "✅"   # Checkmark for successful events
    FAILURE = "❌"   # X for failed events
    NEUTRAL = "📜"   # Scroll for neutral events
    EMERGENCY = "🚨" # Emergency events
    RESONANCE = "🌀" # Combat resonance
    OVERLOAD = "💥"  # Celestial overload
    BREACH = "🌌"    # Dimensional breach
    DISRUPTION = "⭕" # Ritual disruption
    SURGE = "⚡"     # Faction power surge

class EventPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class EventNode:
    event: Event
    position: Tuple[int, int]  # Grid position for visualization
    connections: List[str]     # List of connected event IDs
    status: str               # active, completed, failed, pending
    icon: EventIcon
    description: str
    effects: List[str]
    priority: EventPriority
    timestamp: datetime
    combat_data: Optional[Dict] = None  # Combat-specific data

class EventVisualization:
    def __init__(self):
        self.event_nodes: Dict[str, EventNode] = {}
        self.grid_size = (20, 20)  # Default grid size
        self.occupied_positions: Set[Tuple[int, int]] = set()
        self.ui_components: Dict[str, UIComponent] = {}
        self.emergency_events: Dict[str, EventNode] = {}
        self.active_combat_events: Dict[str, EventNode] = {}
        self.event_history: List[Dict] = []
        self.cell_size = (160, 110)  # Size of each grid cell in pixels
        self.margin = (10, 10)      # Margin between cells
        
    def _grid_to_screen_position(self, grid_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert grid coordinates to screen coordinates"""
        x, y = grid_pos
        screen_x = x * (self.cell_size[0] + self.margin[0]) + self.margin[0]
        screen_y = y * (self.cell_size[1] + self.margin[1]) + self.margin[1]
        return (screen_x, screen_y)

    def add_event_node(self, event: Event, description: str, effects: List[str], 
                      priority: EventPriority = EventPriority.MEDIUM,
                      combat_data: Optional[Dict] = None) -> bool:
        """Add a new event node to the visualization"""
        if event.event_id in self.event_nodes:
            return False
            
        # Find suitable position
        position = self._find_available_position()
        if not position:
            return False
            
        # Determine icon based on event type and combat data
        icon = self._get_event_icon(event.event_type, combat_data)
        
        # Create node
        node = EventNode(
            event=event,
            position=position,
            connections=[],
            status="pending",
            icon=icon,
            description=description,
            effects=effects,
            priority=priority,
            timestamp=datetime.now(),
            combat_data=combat_data
        )
        
        self.event_nodes[event.event_id] = node
        self.occupied_positions.add(position)
        
        # Track special events
        if self._is_emergency_event(node):
            self.emergency_events[event.event_id] = node
        if self._is_combat_event(node):
            self.active_combat_events[event.event_id] = node
            
        # Create UI component
        self._create_ui_component(event.event_id, node)
        
        # Add to history
        self._add_to_history(event.event_id, node)
        
        return True

    def _find_available_position(self) -> Optional[Tuple[int, int]]:
        """Find an available position in the grid for a new event node"""
        # First try to find a position near existing nodes
        if self.event_nodes:
            for x in range(self.grid_size[0]):
                for y in range(self.grid_size[1]):
                    pos = (x, y)
                    if pos not in self.occupied_positions:
                        # Check if position is adjacent to an existing node
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                adj_pos = (x + dx, y + dy)
                                if adj_pos in self.occupied_positions:
                                    return pos
        
        # If no position near existing nodes is found, find any available position
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                pos = (x, y)
                if pos not in self.occupied_positions:
                    return pos
        
        return None  # No available position found

    def _is_emergency_event(self, node: EventNode) -> bool:
        """Check if event is an emergency"""
        if not node.combat_data:
            return False
            
        emergency_types = {
            "combat_resonance", "celestial_overload", 
            "dimensional_breach", "ritual_disruption",
            "faction_surge"
        }
        
        return (
            node.priority == EventPriority.CRITICAL or
            node.combat_data.get("type") in emergency_types
        )

    def _is_combat_event(self, node: EventNode) -> bool:
        """Check if event is combat-related"""
        return (
            node.event.event_type == EventType.COMBAT or
            node.combat_data is not None
        )

    def _get_event_icon(self, event_type: EventType, combat_data: Optional[Dict]) -> EventIcon:
        """Get appropriate icon for event type and combat data"""
        if combat_data:
            combat_type = combat_data.get("type")
            if combat_type == "combat_resonance":
                return EventIcon.RESONANCE
            elif combat_type == "celestial_overload":
                return EventIcon.OVERLOAD
            elif combat_type == "dimensional_breach":
                return EventIcon.BREACH
            elif combat_type == "ritual_disruption":
                return EventIcon.DISRUPTION
            elif combat_type == "faction_surge":
                return EventIcon.SURGE
                
        icon_map = {
            EventType.FACTION: EventIcon.FACTION,
            EventType.COMBAT: EventIcon.COMBAT,
            EventType.RITUAL: EventIcon.RITUAL,
            EventType.CELESTIAL: EventIcon.CELESTIAL,
            EventType.DYNAMIC: EventIcon.NEUTRAL
        }
        return icon_map.get(event_type, EventIcon.NEUTRAL)

    def _create_ui_component(self, event_id: str, node: EventNode):
        """Create UI component for event node"""
        style = self._get_node_style(node)
        color = self._get_node_color(node)
        
        component = UIComponent(
            id=f"event_{event_id}",
            position=self._grid_to_screen_position(node.position),
            size=(150, 100),
            style=style,
            color_scheme=color
        )
        self.ui_components[event_id] = component

    def _get_node_style(self, node: EventNode) -> TextStyle:
        """Get appropriate text style based on node properties"""
        if node.priority == EventPriority.CRITICAL:
            return TextStyle.BOLD
        elif node.priority == EventPriority.HIGH:
            return TextStyle.ITALIC
        return TextStyle.NORMAL

    def _get_node_color(self, node: EventNode) -> ColorScheme:
        """Get appropriate color scheme based on node properties"""
        if node.priority == EventPriority.CRITICAL:
            return ColorScheme.EMERGENCY
        elif node.priority == EventPriority.HIGH:
            return ColorScheme.WARNING
        elif node.status == "completed":
            return ColorScheme.SUCCESS
        elif node.status == "failed":
            return ColorScheme.FAILURE
        return ColorScheme.DEFAULT

    def update_event_status(self, event_id: str, status: str, 
                          combat_data: Optional[Dict] = None):
        """Update the status of an event"""
        if event_id in self.event_nodes:
            node = self.event_nodes[event_id]
            node.status = status
            
            if combat_data:
                node.combat_data = combat_data
            
            # Update icon based on status and combat data
            if status == "completed":
                node.icon = EventIcon.SUCCESS
            elif status == "failed":
                node.icon = EventIcon.FAILURE
            elif status == "active":
                node.icon = self._get_event_icon(node.event.event_type, combat_data)
                
            # Update tracking dictionaries
            self._update_event_tracking(event_id, node)
            
            # Update UI
            self._update_ui_component(event_id, node)
            
            # Add status change to history
            self._add_to_history(event_id, node)

    def _update_event_tracking(self, event_id: str, node: EventNode):
        """Update event tracking based on node status"""
        # Update emergency events
        if self._is_emergency_event(node):
            if node.status in ["completed", "failed"]:
                self.emergency_events.pop(event_id, None)
            else:
                self.emergency_events[event_id] = node
                
        # Update combat events
        if self._is_combat_event(node):
            if node.status in ["completed", "failed"]:
                self.active_combat_events.pop(event_id, None)
            else:
                self.active_combat_events[event_id] = node

    def _update_ui_component(self, event_id: str, node: EventNode):
        """Update UI component for event node"""
        if event_id in self.ui_components:
            component = self.ui_components[event_id]
            component.style = self._get_node_style(node)
            component.color_scheme = self._get_node_color(node)

    def _add_to_history(self, event_id: str, node: EventNode):
        """Add event update to history"""
        self.event_history.append({
            "event_id": event_id,
            "type": node.event.event_type.value,
            "status": node.status,
            "priority": node.priority.value,
            "timestamp": datetime.now(),
            "combat_data": node.combat_data
        })

    def get_active_emergencies(self) -> List[Dict]:
        """Get list of active emergency events"""
        return [
            {
                "event_id": event_id,
                "type": node.event.event_type.value,
                "description": node.description,
                "priority": node.priority.value,
                "combat_data": node.combat_data,
                "duration": (datetime.now() - node.timestamp).total_seconds()
            }
            for event_id, node in self.emergency_events.items()
        ]

    def get_combat_events(self) -> List[Dict]:
        """Get list of active combat events"""
        return [
            {
                "event_id": event_id,
                "type": node.event.event_type.value,
                "description": node.description,
                "status": node.status,
                "combat_data": node.combat_data,
                "duration": (datetime.now() - node.timestamp).total_seconds()
            }
            for event_id, node in self.active_combat_events.items()
        ]

    def get_event_chain_metrics(self, chain_id: str) -> Dict:
        """Get metrics for an event chain"""
        chain_events = [
            node for node in self.event_nodes.values()
            if node.event.chain_id == chain_id
        ]
        
        if not chain_events:
            return {}
            
        total_events = len(chain_events)
        completed = sum(1 for node in chain_events if node.status == "completed")
        failed = sum(1 for node in chain_events if node.status == "failed")
        active = sum(1 for node in chain_events if node.status == "active")
        
        emergency_count = sum(1 for node in chain_events if self._is_emergency_event(node))
        combat_count = sum(1 for node in chain_events if self._is_combat_event(node))
        
        return {
            "total_events": total_events,
            "completed": completed,
            "failed": failed,
            "active": active,
            "success_rate": completed / total_events if total_events > 0 else 0,
            "emergency_count": emergency_count,
            "combat_count": combat_count,
            "average_duration": sum(
                (datetime.now() - node.timestamp).total_seconds()
                for node in chain_events
            ) / total_events if total_events > 0 else 0
        }

    def render_event_chain(self, chain_id: str) -> str:
        """Render an ASCII representation of an event chain"""
        chain_events = [
            node for node in self.event_nodes.values()
            if node.event.chain_id == chain_id
        ]
        
        if not chain_events:
            return "No events in chain"
            
        # Sort events by position and timestamp
        chain_events.sort(key=lambda n: (n.position[1], n.position[0], n.timestamp))
        
        # Create ASCII grid
        grid = [[" " for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
        
        # Place events
        for node in chain_events:
            x, y = node.position
            grid[y][x] = node.icon.value
            
        # Add connections with priority indicators
        for node in chain_events:
            for target_id in node.connections:
                if target_id in self.event_nodes:
                    target = self.event_nodes[target_id]
                    self._draw_connection(grid, node, target)
                    
        # Add emergency indicators
        for node in chain_events:
            if self._is_emergency_event(node):
                x, y = node.position
                if y > 0:
                    grid[y-1][x] = EventIcon.EMERGENCY.value
                    
        # Convert to string
        return "\n".join("".join(row) for row in grid)

    def _draw_connection(self, grid: List[List[str]], source: EventNode, target: EventNode):
        """Draw a connection line between two events with priority indicators"""
        x1, y1 = source.position
        x2, y2 = target.position
        
        # Determine connection style based on priority
        connection_char = "─"
        if max(source.priority.value, target.priority.value) >= EventPriority.HIGH.value:
            connection_char = "═"
        
        # Draw the connection
        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2)):
                if grid[y][x1] == " ":
                    grid[y][x1] = "│" if connection_char == "─" else "║"
        elif y1 == y2:  # Horizontal line
            for x in range(min(x1, x2), max(x1, x2)):
                if grid[y1][x] == " ":
                    grid[y1][x] = connection_char
        else:  # Diagonal line
            if grid[y1][x2] == " ":
                grid[y1][x2] = "└" if y2 > y1 else "┌"
            if grid[y2][x1] == " ":
                grid[y2][x1] = "┐" if y2 > y1 else "┘"

    def get_event_details(self, event_id: str) -> Optional[Dict]:
        """Get detailed information about an event"""
        if event_id not in self.event_nodes:
            return None
            
        node = self.event_nodes[event_id]
        return {
            "name": node.event.name,
            "type": node.event.event_type.value,
            "status": node.status,
            "description": node.description,
            "effects": node.effects,
            "connections": node.connections,
            "duration": node.event.duration,
            "cooldown": node.event.cooldown
        }

    def clear_completed_events(self):
        """Remove completed events from visualization"""
        completed_events = [
            event_id for event_id, node in self.event_nodes.items()
            if node.status in ["completed", "failed"]
        ]
        
        for event_id in completed_events:
            node = self.event_nodes[event_id]
            self.occupied_positions.remove(node.position)
            del self.event_nodes[event_id]
            if event_id in self.ui_components:
                del self.ui_components[event_id]

    def resize_grid(self, width: int, height: int):
        """Resize the visualization grid"""
        if width < self.grid_size[0] or height < self.grid_size[1]:
            # Check if new size can accommodate existing nodes
            max_x = max((node.position[0] for node in self.event_nodes.values()), default=0)
            max_y = max((node.position[1] for node in self.event_nodes.values()), default=0)
            
            if max_x >= width or max_y >= height:
                return False
                
        self.grid_size = (width, height)
        return True 