# Core Systems Documentation

## Game State Management

The Game State Management system is the backbone of Elysian Nexus, handling the core game state, save/load functionality, and game mode transitions.

### Key Components

#### Game Modes
The game supports multiple operational modes:
- `EXPLORATION`: Open world exploration
- `COMBAT`: Active combat encounters
- `DIALOGUE`: Character interactions
- `MENU`: Game menus and UI
- `CUTSCENE`: Story sequences
- `INVENTORY`: Item management
- `TRADING`: Merchant interactions
- `CRAFTING`: Item creation

#### Difficulty Settings
Four difficulty levels are available:
- `EASY`: For casual players
- `NORMAL`: Balanced experience
- `HARD`: Challenging gameplay
- `EXPERT`: Maximum difficulty

#### Save System
The save system includes:
- Automatic saving every 5 minutes (configurable)
- Manual save slots
- Comprehensive save data including:
  - Player progress
  - World state
  - Quest status
  - Inventory contents
- Checksum verification for save integrity
- Timestamp and playtime tracking

### Key Features
- Seamless game mode transitions
- Pause functionality
- Debug mode for development
- Checkpoint system
- Playtime tracking
- Save data integrity verification

### Usage Example
```python
# Initialize game state
game_state = GameState()

# Change game mode
game_state.change_mode(GameMode.COMBAT)

# Save game
save_data = game_state.create_save_data(player, world, quest_manager, inventory)
game_state.save_game(1, save_data)

# Load game
loaded_save = game_state.load_game(1)
```

## Event System

The Event System provides a robust event handling framework for managing game events, notifications, and inter-system communication.

### Key Components

#### Event Types
The system supports various event categories:
- `COMBAT`: Combat-related events
- `QUEST`: Quest progression events
- `DIALOGUE`: Character dialogue events
- `INVENTORY`: Item management events
- `MOVEMENT`: Player and NPC movement
- `INTERACTION`: World interaction events
- `SYSTEM`: Core system events
- `ACHIEVEMENT`: Player achievement events
- `FACTION`: Faction-related events
- `TRADE`: Trading system events

#### Event Priority Levels
Events can be prioritized as:
- `LOW`: Background events
- `NORMAL`: Standard game events
- `HIGH`: Important game events
- `CRITICAL`: Urgent system events

#### Event Properties
Each event contains:
- Type and name
- Custom data payload
- Priority level
- Timestamp
- Optional source and target
- Optional duration
- Optional callback function

### Key Features
- Event dispatching and listening system
- Priority-based event handling
- Event history tracking (up to 1000 events)
- Active event management
- Type-specific event filtering
- Source/target event tracking

### Usage Example
```python
# Initialize event system
event_system = EventSystem()

# Add event listener
def on_combat_event(event):
    print(f"Combat event: {event.name}")
event_system.add_listener(EventType.COMBAT, on_combat_event)

# Create and dispatch event
event = event_system.create_event(
    type=EventType.COMBAT,
    name="enemy_spotted",
    data={"enemy_id": "dragon_001"},
    priority=EventPriority.HIGH
)
event_system.dispatch_event(event)

# Query active events
combat_events = event_system.get_events_by_type(EventType.COMBAT)
```

## Save System

[Documentation for Save System will go here]

## Performance Monitoring

The Performance Monitoring system provides real-time tracking and analysis of game performance metrics.

### Key Components

#### Metric Types
The system tracks various performance metrics:
- `CPU`: CPU usage percentage
- `MEMORY`: Memory usage percentage
- `FPS`: Frames per second
- `LOAD_TIME`: Asset and level loading times
- `RESPONSE_TIME`: System response latency

#### Performance Thresholds
Default warning thresholds:
- CPU Usage: 80%
- Memory Usage: 85%
- Minimum FPS: 30
- Maximum Load Time: 2 seconds
- Maximum Response Time: 100ms

#### Metric Properties
Each metric contains:
- Metric type
- Numerical value
- Timestamp
- Context data

### Key Features
- Real-time performance monitoring
- Historical metric tracking (1000 samples per metric)
- Automatic threshold monitoring
- Performance optimization triggers
- Metric export/import functionality
- Comprehensive performance reporting

### Optimization Mechanisms
- Automatic memory optimization when usage is high
- CPU usage management
- FPS optimization triggers
- Performance report generation

### Usage Example
```python
# Initialize performance monitor
monitor = PerformanceMonitor()

# Start monitoring
monitor.start_monitoring()

# Record custom metric
monitor.record_metric(
    metric_type=MetricType.LOAD_TIME,
    value=1.5,
    context={"level": "boss_arena"}
)

# Get performance report
report = monitor.get_performance_report()

# Check specific metrics
fps_metrics = monitor.get_metrics(
    metric_type=MetricType.FPS,
    time_range=60.0  # Last minute
)

# Export metrics for analysis
monitor.export_metrics("performance_log.json")

# Stop monitoring
monitor.stop_monitoring()
```

## Error Handling

The Error Handling system provides robust error management, logging, and recovery mechanisms for the game.

### Key Components

#### Error Severity Levels
Errors are classified by severity:
- `LOW`: Minor issues that don't affect gameplay
- `MEDIUM`: Issues that may impact gameplay but aren't critical
- `HIGH`: Serious issues requiring immediate attention
- `CRITICAL`: System-threatening issues requiring emergency handling

#### Error Categories
Errors are organized by category:
- `SYSTEM`: Core system errors
- `GAMEPLAY`: General gameplay errors
- `SAVE`: Save/load operation errors
- `STATE`: Game state management errors
- `COMBAT`: Combat system errors
- `DIALOGUE`: Dialogue system errors
- `NETWORK`: Network-related errors
- `RESOURCE`: Resource loading/management errors

#### Error Properties
Each error contains:
- Descriptive message
- Severity level
- Category
- Timestamp
- Optional context data

### Key Features
- Custom error handlers per category and severity
- Comprehensive error logging system
- Error history tracking (up to 100 errors)
- Emergency save system for critical errors
- State recovery mechanisms
- Combat system stabilization
- Error export functionality

### Recovery Mechanisms
- Emergency save system for preserving game state
- State recovery for corrupted game states
- Combat system stabilization for combat-related errors
- Backup save system for data protection

### Usage Example
```python
# Initialize error handler
error_handler = ErrorHandler()

# Register custom error handler
def custom_combat_handler(error, context):
    print(f"Handling combat error: {error}")
    return True

error_handler.register_handler(
    category=ErrorCategory.COMBAT,
    severity=ErrorSeverity.HIGH,
    handler=custom_combat_handler
)

# Handle an error
try:
    # Game code that might fail
    raise GameError("Enemy spawning failed", 
                   ErrorSeverity.MEDIUM, 
                   ErrorCategory.COMBAT)
except Exception as e:
    error_handler.handle_error(
        error=e,
        severity=ErrorSeverity.MEDIUM,
        category=ErrorCategory.COMBAT,
        context={"enemy_id": "dragon_001"}
    )

# Query error history
combat_errors = error_handler.get_error_history(
    category=ErrorCategory.COMBAT,
    severity=ErrorSeverity.HIGH,
    limit=10
) 