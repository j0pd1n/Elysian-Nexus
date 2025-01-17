from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QGraphicsView, QGraphicsScene,
                             QScrollArea, QTextEdit, QComboBox, QSpinBox, QCheckBox, 
                             QGroupBox, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from typing import Dict, Set, List, Tuple
from unified_map_system import UnifiedWorldMap, TerrainType, LocationType, Location
from map_route_system import RouteCalculator, Route

class MapGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        # Zoom parameters
        self.zoom_factor = 1.15
        self.min_zoom = 0.5
        self.max_zoom = 2.0
        self.current_zoom = 1.0
        
        # Pan parameters
        self.panning = False
        self.last_pos = None
        
    def wheelEvent(self, event):
        """Handle zoom with mouse wheel"""
        if event.angleDelta().y() > 0:
            factor = self.zoom_factor
        else:
            factor = 1 / self.zoom_factor
            
        new_zoom = self.current_zoom * factor
        if self.min_zoom <= new_zoom <= self.max_zoom:
            self.current_zoom = new_zoom
            self.scale(factor, factor)
            
    def mousePressEvent(self, event):
        """Start panning on middle mouse button"""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.panning = True
            self.last_pos = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)
            
    def mouseReleaseEvent(self, event):
        """Stop panning"""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)
            
    def mouseMoveEvent(self, event):
        """Handle panning movement"""
        if self.panning and self.last_pos:
            delta = event.pos() - self.last_pos
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y())
            self.last_pos = event.pos()
        super().mouseMoveEvent(event)

class MapScene(QGraphicsScene):
    def __init__(self, world_map: UnifiedWorldMap):
        super().__init__()
        self.world_map = world_map
        self.grid_size = 50  # pixels per grid cell
        self.current_route = None
        self.setupScene()
        
    def setupScene(self):
        """Initialize the map scene"""
        # Set scene size based on world boundaries
        min_x = self.world_map.min_x * self.grid_size
        max_x = self.world_map.max_x * self.grid_size
        min_y = self.world_map.min_y * self.grid_size
        max_y = self.world_map.max_y * self.grid_size
        self.setSceneRect(min_x, min_y, max_x - min_x, max_y - min_y)
        
        # Draw grid
        self.drawGrid()
        
        # Draw paths
        self.drawPaths()
        
        # Draw discovered locations
        self.drawLocations()
        
        # Draw current position
        self.drawCurrentPosition()
        
    def drawGrid(self):
        """Draw the background grid"""
        grid_pen = QPen(QColor("#2C2F33"), 1)  # Dark gray lines
        
        # Draw vertical lines
        for x in range(self.world_map.min_x, self.world_map.max_x + 1):
            x_pos = x * self.grid_size
            self.addLine(x_pos, self.world_map.min_y * self.grid_size,
                        x_pos, self.world_map.max_y * self.grid_size, grid_pen)
            
        # Draw horizontal lines
        for y in range(self.world_map.min_y, self.world_map.max_y + 1):
            y_pos = y * self.grid_size
            self.addLine(self.world_map.min_x * self.grid_size, y_pos,
                        self.world_map.max_x * self.grid_size, y_pos, grid_pen)
            
    def drawPaths(self):
        """Draw discovered paths between locations"""
        path_pen = QPen(QColor("#FFD700"), 2)  # Gold lines
        glow_pen = QPen(QColor("#FFD70033"), 6)  # Transparent gold for glow
        
        for path in self.world_map.paths:
            if path.discovered:
                start_x = path.start.position[0] * self.grid_size
                start_y = path.start.position[1] * self.grid_size
                end_x = path.end.position[0] * self.grid_size
                end_y = path.end.position[1] * self.grid_size
                
                # Draw glow effect
                self.addLine(start_x, start_y, end_x, end_y, glow_pen)
                # Draw main path
                self.addLine(start_x, start_y, end_x, end_y, path_pen)
            
    def drawLocations(self):
        """Draw discovered locations"""
        for location in self.world_map.locations.values():
            if location.discovered:
                x, y = location.position
                x_pos = x * self.grid_size
                y_pos = y * self.grid_size
                
                # Draw location marker
                marker = self.addEllipse(
                    x_pos - 15, y_pos - 15, 30, 30,
                    QPen(QColor("#FFD700")),  # Gold outline
                    QBrush(QColor("#2C2F33"))  # Dark background
                )
                
                # Add location icon
                icon_text = self.addText(location.icon, QFont("Segoe UI Emoji", 12))
                icon_text.setDefaultTextColor(QColor("#FFD700"))
                icon_text.setPos(x_pos - 12, y_pos - 12)
                
                # Add location name if it's a major location
                if location.location_type in [LocationType.MAJOR_CITY, 
                                           LocationType.QUEST_LOCATION]:
                    name_text = self.addText(location.name, QFont("Trajan Pro", 8))
                    name_text.setDefaultTextColor(QColor("#FFD700"))
                    name_text.setPos(x_pos - 30, y_pos + 20)
                
                # Add fast travel indicator if available
                if location.fast_travel_unlocked:
                    ft_text = self.addText("⚡", QFont("Segoe UI Emoji", 8))
                    ft_text.setDefaultTextColor(QColor("#00FF00"))
                    ft_text.setPos(x_pos + 15, y_pos - 15)
            
    def drawCurrentPosition(self):
        """Draw the player's current position"""
        x, y = self.world_map.current_position
        x_pos = x * self.grid_size
        y_pos = y * self.grid_size
        
        # Draw position marker
        marker = self.addEllipse(
            x_pos - 20, y_pos - 20, 40, 40,
            QPen(QColor("#00FF00"), 2),  # Green outline
            QBrush(QColor("#2C2F33"))  # Dark background
        )
        
        # Add player icon
        player_text = self.addText("🧙", QFont("Segoe UI Emoji", 14))
        player_text.setDefaultTextColor(QColor("#00FF00"))
        player_text.setPos(x_pos - 15, y_pos - 15)

    def draw_route(self, route: Route):
        """Draw a route on the map"""
        self.current_route = route
        
        if not route:
            return
            
        # Create route pen with arrow markers
        route_pen = QPen(QColor("#00FF00"), 3)  # Green line
        route_pen.setStyle(Qt.PenStyle.DashLine)
        
        # Draw each segment
        for segment in route.segments:
            start_x = segment.start.position[0] * self.grid_size
            start_y = segment.start.position[1] * self.grid_size
            end_x = segment.end.position[0] * self.grid_size
            end_y = segment.end.position[1] * self.grid_size
            
            # Draw path line
            path_item = self.addLine(
                start_x, start_y, end_x, end_y, route_pen
            )
            path_item.setZValue(1)  # Draw above terrain
            
            # Add waypoint marker
            marker = self.addEllipse(
                end_x - 5, end_y - 5, 10, 10,
                QPen(QColor("#00FF00")),
                QBrush(QColor("#00FF00"))
            )
            marker.setZValue(2)
            
            # Add segment info
            info_text = (
                f"{segment.terrain.value}\n"
                f"{segment.estimated_time:.1f} min"
            )
            text_item = self.addText(
                info_text, 
                QFont("Segoe UI", 8)
            )
            text_item.setDefaultTextColor(QColor("#00FF00"))
            text_item.setPos(
                (start_x + end_x) / 2 - 20,
                (start_y + end_y) / 2 - 20
            )
            text_item.setZValue(2)

class LocationInfoPanel(QFrame):
    """Panel showing information about the current location"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #2C2F33;
                border: 1px solid #FFD700;
                border-radius: 5px;
            }
            QLabel {
                color: #FFD700;
            }
            QTextEdit {
                background-color: #23272A;
                color: #FFFFFF;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Title
        self.title_label = QLabel("📍 Current Location")
        self.title_label.setFont(QFont("Trajan Pro", 12))
        layout.addWidget(self.title_label)
        
        # Description
        self.description = QTextEdit()
        self.description.setReadOnly(True)
        self.description.setMaximumHeight(100)
        layout.addWidget(self.description)
        
        # Stats
        self.stats_layout = QVBoxLayout()
        layout.addLayout(self.stats_layout)
        
    def update_info(self, location_info: Dict):
        """Update the panel with new location information"""
        self.title_label.setText(f"{location_info['icon']} {location_info['name']}")
        self.description.setText(location_info['description'])
        
        # Clear previous stats
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Add new stats
        stats = [
            ("🏷️ Type", location_info['type']),
            ("🌍 Terrain", location_info['terrain']),
            ("⚔️ Danger Level", f"{location_info['danger_level']}/10"),
            ("📜 Active Quests", len(location_info['quests'])),
            ("💎 Resources", len(location_info['resources']))
        ]
        
        for label, value in stats:
            stat_label = QLabel(f"{label}: {value}")
            stat_label.setFont(QFont("Segoe UI", 10))
            self.stats_layout.addWidget(stat_label)

class RoutePanel(QGroupBox):
    """Panel for route planning controls"""
    def __init__(self, world_map: UnifiedWorldMap, parent=None):
        super().__init__("🗺️ Route Planner", parent)
        self.world_map = world_map
        self.calculator = RouteCalculator(world_map)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Start location combo
        self.start_combo = QComboBox()
        self.start_combo.addItems(
            [loc.name for loc in self.world_map.locations.values() 
             if loc.discovered]
        )
        layout.addRow("From:", self.start_combo)
        
        # End location combo
        self.end_combo = QComboBox()
        self.end_combo.addItems(
            [loc.name for loc in self.world_map.locations.values() 
             if loc.discovered]
        )
        layout.addRow("To:", self.end_combo)
        
        # Player level spinner
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 100)
        self.level_spin.setValue(1)
        layout.addRow("Player Level:", self.level_spin)
        
        # Prefer safe routes checkbox
        self.safe_check = QCheckBox("Prefer Safe Routes")
        layout.addRow(self.safe_check)
        
        # Avoid terrain types
        self.avoid_terrain = {}
        terrain_box = QGroupBox("Avoid Terrain")
        terrain_layout = QVBoxLayout(terrain_box)
        
        for terrain in TerrainType:
            check = QCheckBox(terrain.value)
            self.avoid_terrain[terrain] = check
            terrain_layout.addWidget(check)
            
        layout.addRow(terrain_box)
        
        # Find route button
        self.find_btn = QPushButton("Find Route")
        self.find_btn.clicked.connect(self.find_route)
        layout.addRow(self.find_btn)
        
    def find_route(self):
        """Calculate and display a route"""
        # Get avoided terrain
        avoid = [
            terrain for terrain, check in self.avoid_terrain.items()
            if check.isChecked()
        ]
        
        # Find route
        route = self.calculator.find_route(
            self.start_combo.currentText(),
            self.end_combo.currentText(),
            player_level=self.level_spin.value(),
            avoid_terrain=avoid,
            prefer_safe=self.safe_check.isChecked()
        )
        
        if route:
            # Show route on map
            self.parent().map_scene.draw_route(route)
            
            # Show route details
            QMessageBox.information(
                self,
                "Route Found",
                self.calculator.get_route_description(route)
            )
        else:
            QMessageBox.warning(
                self,
                "No Route Found",
                "Could not find a route between these locations."
            )

class MapWindow(QMainWindow):
    def __init__(self, world_map: UnifiedWorldMap):
        super().__init__()
        self.world_map = world_map
        self.initUI()
        
    def initUI(self):
        """Initialize the main window UI"""
        self.setWindowTitle("Elysian Nexus - World Map")
        self.setMinimumSize(1024, 768)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #23272A;
            }
            QPushButton {
                background-color: #2C2F33;
                color: #FFD700;
                border: 1px solid #FFD700;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #FFD700;
                color: #2C2F33;
            }
            QLabel {
                color: #FFD700;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QVBoxLayout(central_widget)
        
        # Add title
        title = QLabel("🗺️ World Map - Elysian Nexus")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Trajan Pro", 16))
        layout.addWidget(title)
        
        # Create main content layout
        content_layout = QHBoxLayout()
        
        # Create map view
        self.map_view = MapGraphicsView()
        self.map_scene = MapScene(self.world_map)
        self.map_view.setScene(self.map_scene)
        content_layout.addWidget(self.map_view, stretch=2)
        
        # Create right panel
        right_panel = QVBoxLayout()
        
        # Add location info panel
        self.location_info = LocationInfoPanel()
        right_panel.addWidget(self.location_info)
        
        # Add route planner
        self.route_panel = RoutePanel(self.world_map, self)
        right_panel.addWidget(self.route_panel)
        
        # Add controls
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #2C2F33;
                border: 1px solid #FFD700;
                border-radius: 5px;
            }
        """)
        controls_layout = QVBoxLayout(controls_frame)
        
        # Navigation controls
        nav_layout = QHBoxLayout()
        
        # Navigation buttons
        for direction, icon in [("north", "⬆️"), ("south", "⬇️"), 
                              ("east", "➡️"), ("west", "⬅️")]:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda d=direction: self.move_player(d))
            nav_layout.addWidget(btn)
            
        controls_layout.addLayout(nav_layout)
        
        # Reset view button
        reset_btn = QPushButton("Reset View")
        reset_btn.clicked.connect(self.reset_view)
        controls_layout.addWidget(reset_btn)
        
        right_panel.addWidget(controls_frame)
        
        # Add discovery progress
        progress_label = QLabel(f"🗺️ World Discovered: {self.world_map.get_discovered_percentage():.1f}%")
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_panel.addWidget(progress_label)
        
        content_layout.addLayout(right_panel, stretch=1)
        layout.addLayout(content_layout)
        
        # Update location info
        self.update_location_info()
        
    def move_player(self, direction: str):
        """Handle player movement"""
        success, message = self.world_map.move_player(direction)
        if success:
            self.map_scene.clear()
            self.map_scene.setupScene()
            self.update_location_info()
            
    def reset_view(self):
        """Reset the map view to default"""
        self.map_view.resetTransform()
        self.map_view.current_zoom = 1.0
        
    def update_location_info(self):
        """Update the location information panel"""
        info = self.world_map.get_current_location_info()
        self.location_info.update_info(info)
        
def show_map(world_map: UnifiedWorldMap):
    """Create and show the map window"""
    window = MapWindow(world_map)
    window.show()
    return window 