# Faction Territory System Documentation

## Overview
The Faction Territory System in Elysian Nexus manages the control, resources, and influence points of different territories across the game world. It integrates with weather, economic, and faction systems to create a dynamic territorial control mechanic.

## Core Components

### Territory Types
1. **Mundane**
   - Standard territories
   - Basic resource nodes
   - Normal influence mechanics

2. **Magical**
   - Enhanced magical properties
   - Mana-rich environments
   - Mystical influence points

3. **Celestial**
   - Cosmic power centers
   - Celestial alignments
   - Divine influence zones

4. **Void**
   - Dimensional anomalies
   - Void energy sources
   - Space-time distortions

5. **Temporal**
   - Time-warped regions
   - Chronological anomalies
   - Temporal power sources

6. **Primal**
   - Raw power sources
   - Elemental confluences
   - Natural energy wells

### Resource Nodes
```python
@dataclass
class ResourceNode:
    node_type: ResourceNodeType
    base_yield: float
    current_yield: float
    quality: float  # 0.0 to 1.0
    depletion_rate: float
    regeneration_rate: float
    magical_resonance: float
    controlling_faction: Optional[str]
    last_harvest: float
```

#### Node Types
- Mana Well: Magical energy source
- Crystal Vein: Mineral resources
- Void Rift: Dimensional materials
- Celestial Anchor: Divine resources
- Temporal Nexus: Time-based resources
- Primal Spring: Elemental resources
- Essence Pool: Pure energy source

### Influence Points
```python
@dataclass
class InfluencePoint:
    point_type: InfluencePointType
    base_strength: float
    current_strength: float
    magical_attunement: float
    area_of_effect: float
    maintenance_cost: float
    special_abilities: List[str]
    controlling_faction: str
    linked_points: Set[str]
    last_update: float
```

#### Point Types
- Fortress: Military control
- Ritual Circle: Magical influence
- Observatory: Celestial monitoring
- Void Gate: Dimensional control
- Time Lock: Temporal stability
- Primal Shrine: Elemental power

## Advanced Features

### 1. Territory Control
- Faction influence calculation
- Control point management
- Resource node control
- Territory contestation

### 2. Resource Management
- Node yield calculation
- Resource depletion
- Regeneration mechanics
- Quality fluctuation

### 3. Influence Networks
- Ritual network creation
- Power calculation
- Network synergies
- Maintenance systems

### 4. Celestial Integration
- Weather effect processing
- Celestial pattern impact
- Magical resonance
- Power fluctuations

## Technical Implementation

### Territory Management
```python
@dataclass
class Territory:
    name: str
    territory_type: TerritoryType
    controlling_faction: Optional[str]
    resource_nodes: Dict[str, ResourceNode]
    influence_points: Dict[str, InfluencePoint]
    strategic_value: float
    magical_stability: float
    celestial_alignment: float
    contested: bool
    last_control_change: float
```

### Key Systems
1. **Control Calculation**
   - Influence point strength
   - Faction presence
   - Resource control
   - Strategic value

2. **Resource Processing**
   - Yield calculation
   - Depletion tracking
   - Regeneration timing
   - Quality management

3. **Network Management**
   - Point linking
   - Power distribution
   - Synergy calculation
   - Maintenance tracking

## Integration Points
- Weather System: Environmental effects
- Economic System: Resource markets
- Faction System: Control mechanics
- Combat System: Territory defense
- Quest System: Territory missions

## Best Practices
1. Regular territory status updates
2. Monitor resource depletion
3. Balance influence distribution
4. Maintain network stability
5. Track celestial effects
6. Manage control transitions
7. Process resource regeneration 