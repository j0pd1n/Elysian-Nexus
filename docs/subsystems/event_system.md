# Dynamic Events System Documentation

## Overview
The Dynamic Events System in Elysian Nexus manages the creation, execution, and resolution of dynamic world events that shape the game's narrative and gameplay. It integrates with weather, economic, and faction systems to create a living, reactive world.

## Core Components

### Event Categories
```python
class EventCategory(Enum):
    NATURAL = "natural"
    ECONOMIC = "economic"
    SOCIAL = "social"
    POLITICAL = "political"
    MILITARY = "military"
    SUPERNATURAL = "supernatural"
```

### Event Severity
```python
class EventSeverity(Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"
```

### World State Management
```python
@dataclass
class WorldState:
    metrics: Dict[WorldStateMetric, float]  # 0.0 to 1.0
    active_effects: Set[str]
    faction_relations: Dict[str, Dict[str, float]]  # -1.0 to 1.0
    location_states: Dict[str, Dict[str, Any]]
    last_update: float
```

### Dynamic Event Structure
```python
@dataclass
class DynamicEvent:
    event_id: str
    category: EventCategory
    severity: EventSeverity
    location: str
    description: str
    triggers: Dict[str, Any]
    consequences: Dict[str, Any]
    duration: float
    start_time: float
    active: bool = True
    resolved: bool = False
```

## Event Generation Systems

### 1. Natural Events
- Weather phenomena
- Natural disasters
- Seasonal changes
- Environmental shifts

### 2. Social Events
- Festivals
- Cultural celebrations
- Social movements
- Community gatherings

### 3. Political Events
- Faction conflicts
- Power struggles
- Diplomatic missions
- Territory disputes

### 4. Military Events
- Battles
- Sieges
- Troop movements
- Strategic operations

### 5. Supernatural Events
- Magical anomalies
- Celestial phenomena
- Dimensional rifts
- Arcane disasters

## Technical Implementation

### Event Management
1. **Event Creation**
   - Trigger evaluation
   - Context analysis
   - Severity calculation
   - Duration setting

2. **Event Processing**
   - State updates
   - Effect application
   - Consequence handling
   - Resolution checks

3. **Event Resolution**
   - Outcome determination
   - Reward distribution
   - World state updates
   - History recording

### World State Metrics
```python
class WorldStateMetric(Enum):
    STABILITY = "stability"      # Political/social stability
    PROSPERITY = "prosperity"    # Economic health
    DANGER_LEVEL = "danger_level"  # Threat assessment
    MORALE = "morale"           # Population happiness
    CORRUPTION = "corruption"    # System integrity
    MAGIC_SATURATION = "magic_saturation"  # Magical energy
```

## Advanced Features

### 1. Event Chains
- Sequential events
- Branching outcomes
- Conditional triggers
- Cascading effects

### 2. Dynamic Scaling
- Population impact
- Area of effect
- Duration adjustment
- Intensity scaling

### 3. World Impact
- Resource distribution
- Faction relations
- Territory control
- Economic effects

### 4. Environmental Integration
- Weather influence
- Terrain effects
- Resource availability
- Travel conditions

## Integration Points
- Weather System: Environmental conditions
- Economic System: Market effects
- Faction System: Political dynamics
- Quest System: Event-based missions
- Combat System: Military conflicts

## Event Logging
```python
def _setup_logger(self) -> logging.Logger:
    logger = logging.getLogger("DynamicEventsSystem")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler("logs/events.log")
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    return logger
```

## Best Practices
1. Regular world state monitoring
2. Balanced event distribution
3. Meaningful consequences
4. Fair impact scaling
5. Coherent narrative flow
6. Resource balance maintenance
7. Event history tracking 