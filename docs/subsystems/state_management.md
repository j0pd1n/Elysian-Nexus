# State Management System Documentation

## Overview
The State Management System in Elysian Nexus provides robust handling of game state transitions, particularly for complex events, rituals, and world-changing phenomena. It ensures data consistency and provides transaction management for critical game state changes.

## Core Components

### State Types
```python
class StateType(Enum):
    CELESTIAL_EVENT = "celestial_event"
    RITUAL = "ritual"
    DIMENSIONAL_ANOMALY = "dimensional_anomaly"
    TERRITORY_STATE = "territory_state"
    FACTION_STATE = "faction_state"
```

### State Transaction
```python
@dataclass
class StateTransaction:
    id: str
    timestamp: datetime
    state_type: StateType
    previous_state: Dict
    new_state: Dict
    status: str  # PENDING, COMMITTED, ROLLED_BACK
    metadata: Dict
```

## Technical Implementation

### Database Management
```python
def _setup_database(self):
    """Initialize SQLite database for state persistence"""
    Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    with self._get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS state_transactions (
                id TEXT PRIMARY KEY,
                timestamp DATETIME,
                state_type TEXT,
                previous_state TEXT,
                new_state TEXT,
                status TEXT,
                metadata TEXT
            )
        """)
```

### Transaction Management
1. **Begin Transaction**
   - State type validation
   - Current state capture
   - Transaction creation
   - Lock acquisition

2. **Commit Transaction**
   - State validation
   - Change application
   - History recording
   - Lock release

3. **Rollback Transaction**
   - State restoration
   - Error logging
   - Lock release
   - History update

## State Systems

### 1. Celestial Event State
```python
class CelestialEventState:
    def start_event(self, event_data: Dict) -> str:
        # Event initialization
        pass

    def end_event(self, event_id: str, outcome: Dict):
        # Event conclusion
        pass
```

### 2. Ritual State
```python
class RitualState:
    def start_ritual(self, ritual_data: Dict) -> str:
        # Ritual initialization
        pass

    def complete_ritual_phase(self, ritual_id: str, phase_data: Dict):
        # Phase progression
        pass

    def fail_ritual(self, ritual_id: str, failure_data: Dict):
        # Failure handling
        pass
```

## Advanced Features

### 1. State Persistence
- Transaction logging
- State snapshots
- History tracking
- Recovery mechanisms

### 2. Concurrency Control
- Thread-safe operations
- Lock management
- Transaction isolation
- Deadlock prevention

### 3. State Recovery
- Rollback capability
- State restoration
- Error handling
- Data integrity

### 4. State Export/Import
- Snapshot creation
- State migration
- Backup management
- Version control

## Integration Points
- Event System: State transitions
- Ritual System: Ceremony states
- Territory System: Control states
- Faction System: Relation states
- Combat System: Battle states

## Logging System
```python
def _setup_logging(self):
    logging.basicConfig(
        filename='logs/state_management.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    self.logger = logging.getLogger(__name__)
```

## Best Practices
1. Always use transactions for state changes
2. Implement proper error handling
3. Maintain state consistency
4. Log all critical operations
5. Regular state backups
6. Validate state transitions
7. Monitor transaction performance 