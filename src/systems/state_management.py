from dataclasses import dataclass
from datetime import datetime
import json
import logging
from enum import Enum
from typing import Dict, List, Optional, Any
from pathlib import Path
import sqlite3
import threading
from contextlib import contextmanager

class StateType(Enum):
    CELESTIAL_EVENT = "celestial_event"
    RITUAL = "ritual"
    DIMENSIONAL_ANOMALY = "dimensional_anomaly"
    TERRITORY_STATE = "territory_state"
    FACTION_STATE = "faction_state"

@dataclass
class StateTransaction:
    id: str
    timestamp: datetime
    state_type: StateType
    previous_state: Dict
    new_state: Dict
    status: str  # PENDING, COMMITTED, ROLLED_BACK
    metadata: Dict

class StateManager:
    def __init__(self, db_path: str = "data/state.db"):
        self.db_path = db_path
        self._setup_database()
        self._setup_logging()
        self.lock = threading.Lock()
        
    def _setup_logging(self):
        """Configure logging for state management"""
        logging.basicConfig(
            filename='logs/state_management.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _setup_database(self):
        """Initialize SQLite database for state persistence"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._get_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS state_transactions (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    state_type TEXT,
                    previous_state TEXT,
                    new_state TEXT,
                    status TEXT,
                    metadata TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS active_states (
                    state_type TEXT PRIMARY KEY,
                    current_state TEXT,
                    last_updated TEXT,
                    metadata TEXT
                )
            """)

    @contextmanager
    def _get_db_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def begin_transaction(self, state_type: StateType, current_state: Dict) -> StateTransaction:
        """Begin a new state transaction"""
        transaction_id = f"{state_type.value}_{datetime.now().timestamp()}"
        transaction = StateTransaction(
            id=transaction_id,
            timestamp=datetime.now(),
            state_type=state_type,
            previous_state=current_state,
            new_state={},
            status="PENDING",
            metadata={}
        )
        
        with self.lock:
            with self._get_db_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO state_transactions 
                    (id, timestamp, state_type, previous_state, new_state, status, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        transaction.id,
                        transaction.timestamp.isoformat(),
                        transaction.state_type.value,
                        json.dumps(transaction.previous_state),
                        json.dumps(transaction.new_state),
                        transaction.status,
                        json.dumps(transaction.metadata)
                    )
                )
                conn.commit()
        
        self.logger.info(f"Started transaction {transaction_id} for {state_type.value}")
        return transaction

    def commit_transaction(self, transaction: StateTransaction, new_state: Dict):
        """Commit a state transaction"""
        with self.lock:
            try:
                with self._get_db_connection() as conn:
                    # Update transaction
                    transaction.new_state = new_state
                    transaction.status = "COMMITTED"
                    conn.execute(
                        """
                        UPDATE state_transactions 
                        SET new_state = ?, status = ?, metadata = ?
                        WHERE id = ?
                        """,
                        (
                            json.dumps(new_state),
                            "COMMITTED",
                            json.dumps(transaction.metadata),
                            transaction.id
                        )
                    )
                    
                    # Update active state
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO active_states 
                        (state_type, current_state, last_updated, metadata)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            transaction.state_type.value,
                            json.dumps(new_state),
                            datetime.now().isoformat(),
                            json.dumps(transaction.metadata)
                        )
                    )
                    conn.commit()
                
                self.logger.info(f"Committed transaction {transaction.id}")
                
            except Exception as e:
                self.logger.error(f"Failed to commit transaction {transaction.id}: {str(e)}")
                self.rollback_transaction(transaction)
                raise

    def rollback_transaction(self, transaction: StateTransaction):
        """Rollback a state transaction"""
        with self.lock:
            try:
                with self._get_db_connection() as conn:
                    # Update transaction status
                    conn.execute(
                        """
                        UPDATE state_transactions 
                        SET status = ?, metadata = ?
                        WHERE id = ?
                        """,
                        (
                            "ROLLED_BACK",
                            json.dumps({**transaction.metadata, "rollback_time": datetime.now().isoformat()}),
                            transaction.id
                        )
                    )
                    
                    # Restore previous state
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO active_states 
                        (state_type, current_state, last_updated, metadata)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            transaction.state_type.value,
                            json.dumps(transaction.previous_state),
                            datetime.now().isoformat(),
                            json.dumps({"rollback_from": transaction.id})
                        )
                    )
                    conn.commit()
                
                self.logger.warning(f"Rolled back transaction {transaction.id}")
                
            except Exception as e:
                self.logger.error(f"Failed to rollback transaction {transaction.id}: {str(e)}")
                raise

    def get_current_state(self, state_type: StateType) -> Optional[Dict]:
        """Get the current state for a given state type"""
        with self._get_db_connection() as conn:
            result = conn.execute(
                "SELECT current_state FROM active_states WHERE state_type = ?",
                (state_type.value,)
            ).fetchone()
            
            if result:
                return json.loads(result[0])
            return None

    def get_transaction_history(self, state_type: StateType = None, limit: int = 100) -> List[StateTransaction]:
        """Get transaction history, optionally filtered by state type"""
        query = "SELECT * FROM state_transactions"
        params = []
        
        if state_type:
            query += " WHERE state_type = ?"
            params.append(state_type.value)
            
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        with self._get_db_connection() as conn:
            results = conn.execute(query, params).fetchall()
            
            transactions = []
            for row in results:
                transactions.append(StateTransaction(
                    id=row[0],
                    timestamp=datetime.fromisoformat(row[1]),
                    state_type=StateType(row[2]),
                    previous_state=json.loads(row[3]),
                    new_state=json.loads(row[4]),
                    status=row[5],
                    metadata=json.loads(row[6])
                ))
            
            return transactions

    def export_state_snapshot(self, path: str):
        """Export a snapshot of all current states"""
        with self._get_db_connection() as conn:
            states = conn.execute("SELECT * FROM active_states").fetchall()
            
            snapshot = {
                "timestamp": datetime.now().isoformat(),
                "states": {
                    row[0]: {
                        "current_state": json.loads(row[1]),
                        "last_updated": row[2],
                        "metadata": json.loads(row[3])
                    }
                    for row in states
                }
            }
            
            with open(path, 'w') as f:
                json.dump(snapshot, f, indent=2)
            
            self.logger.info(f"Exported state snapshot to {path}")

    def import_state_snapshot(self, path: str):
        """Import a state snapshot"""
        with open(path, 'r') as f:
            snapshot = json.load(f)
            
        with self.lock:
            with self._get_db_connection() as conn:
                for state_type, state_data in snapshot["states"].items():
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO active_states 
                        (state_type, current_state, last_updated, metadata)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            state_type,
                            json.dumps(state_data["current_state"]),
                            state_data["last_updated"],
                            json.dumps(state_data["metadata"])
                        )
                    )
                conn.commit()
            
            self.logger.info(f"Imported state snapshot from {path}")

class CelestialEventState:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        
    def start_event(self, event_data: Dict) -> str:
        """Start a new celestial event"""
        current_state = self.state_manager.get_current_state(StateType.CELESTIAL_EVENT) or {}
        
        # Begin transaction for new event
        transaction = self.state_manager.begin_transaction(
            StateType.CELESTIAL_EVENT,
            current_state
        )
        
        try:
            # Add new event to current state
            event_id = f"event_{datetime.now().timestamp()}"
            new_state = {
                **current_state,
                event_id: {
                    **event_data,
                    "status": "ACTIVE",
                    "start_time": datetime.now().isoformat()
                }
            }
            
            # Commit the transaction
            self.state_manager.commit_transaction(transaction, new_state)
            return event_id
            
        except Exception as e:
            self.state_manager.rollback_transaction(transaction)
            raise

    def end_event(self, event_id: str, outcome: Dict):
        """End a celestial event"""
        current_state = self.state_manager.get_current_state(StateType.CELESTIAL_EVENT)
        if not current_state or event_id not in current_state:
            raise ValueError(f"Event {event_id} not found")
            
        transaction = self.state_manager.begin_transaction(
            StateType.CELESTIAL_EVENT,
            current_state
        )
        
        try:
            new_state = {
                **current_state,
                event_id: {
                    **current_state[event_id],
                    "status": "COMPLETED",
                    "end_time": datetime.now().isoformat(),
                    "outcome": outcome
                }
            }
            
            self.state_manager.commit_transaction(transaction, new_state)
            
        except Exception as e:
            self.state_manager.rollback_transaction(transaction)
            raise

class RitualState:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        
    def start_ritual(self, ritual_data: Dict) -> str:
        """Start a new ritual"""
        current_state = self.state_manager.get_current_state(StateType.RITUAL) or {}
        
        transaction = self.state_manager.begin_transaction(
            StateType.RITUAL,
            current_state
        )
        
        try:
            ritual_id = f"ritual_{datetime.now().timestamp()}"
            new_state = {
                **current_state,
                ritual_id: {
                    **ritual_data,
                    "status": "IN_PROGRESS",
                    "start_time": datetime.now().isoformat(),
                    "phases_completed": []
                }
            }
            
            self.state_manager.commit_transaction(transaction, new_state)
            return ritual_id
            
        except Exception as e:
            self.state_manager.rollback_transaction(transaction)
            raise

    def complete_ritual_phase(self, ritual_id: str, phase_data: Dict):
        """Complete a phase of a ritual"""
        current_state = self.state_manager.get_current_state(StateType.RITUAL)
        if not current_state or ritual_id not in current_state:
            raise ValueError(f"Ritual {ritual_id} not found")
            
        transaction = self.state_manager.begin_transaction(
            StateType.RITUAL,
            current_state
        )
        
        try:
            ritual_state = current_state[ritual_id]
            new_state = {
                **current_state,
                ritual_id: {
                    **ritual_state,
                    "phases_completed": [
                        *ritual_state["phases_completed"],
                        {
                            **phase_data,
                            "completion_time": datetime.now().isoformat()
                        }
                    ]
                }
            }
            
            self.state_manager.commit_transaction(transaction, new_state)
            
        except Exception as e:
            self.state_manager.rollback_transaction(transaction)
            raise

    def fail_ritual(self, ritual_id: str, failure_data: Dict):
        """Handle a failed ritual"""
        current_state = self.state_manager.get_current_state(StateType.RITUAL)
        if not current_state or ritual_id not in current_state:
            raise ValueError(f"Ritual {ritual_id} not found")
            
        transaction = self.state_manager.begin_transaction(
            StateType.RITUAL,
            current_state
        )
        
        try:
            new_state = {
                **current_state,
                ritual_id: {
                    **current_state[ritual_id],
                    "status": "FAILED",
                    "failure_time": datetime.now().isoformat(),
                    "failure_data": failure_data
                }
            }
            
            self.state_manager.commit_transaction(transaction, new_state)
            
        except Exception as e:
            self.state_manager.rollback_transaction(transaction)
            raise 