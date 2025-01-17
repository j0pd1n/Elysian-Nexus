from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import logging
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class StateVersion:
    """Represents a version of game state with metadata."""
    version_id: str
    timestamp: datetime
    state_data: Dict[str, Any]
    parent_version_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    checksum: str = ""

@dataclass
class StateDiff:
    """Represents differences between two state versions."""
    added: Dict[str, Any]
    modified: Dict[str, Any]
    removed: List[str]
    from_version: str
    to_version: str
    timestamp: datetime

class StateVersionManager:
    """Manages versioning of game states including history, diffing, and migration."""
    
    CURRENT_STATE_VERSION = "1.0.0"
    
    def __init__(self, version_dir: Path):
        self.version_dir = version_dir
        self.version_dir.mkdir(exist_ok=True)
        self.versions: Dict[str, StateVersion] = {}
        self.current_version: Optional[StateVersion] = None
        self.version_history: List[str] = []  # Ordered list of version IDs
        self.max_versions = 50  # Maximum number of versions to keep
        
    def create_version(self, state_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> StateVersion:
        """Create a new version of the state."""
        # Generate version ID based on timestamp and content hash
        timestamp = datetime.now()
        content_hash = self._calculate_state_hash(state_data)
        version_id = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{content_hash[:8]}"
        
        # Create new version
        version = StateVersion(
            version_id=version_id,
            timestamp=timestamp,
            state_data=state_data.copy(),
            parent_version_id=self.current_version.version_id if self.current_version else None,
            metadata=metadata or {},
            checksum=content_hash
        )
        
        # Store version
        self.versions[version_id] = version
        self.version_history.append(version_id)
        self.current_version = version
        
        # Prune old versions if needed
        self._prune_old_versions()
        
        # Save version to disk
        self._save_version_to_disk(version)
        
        return version
        
    def _calculate_state_hash(self, state_data: Dict[str, Any]) -> str:
        """Calculate a hash of the state data for versioning and integrity checking."""
        # Convert state to a stable string representation
        state_str = json.dumps(state_data, sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()
        
    def _save_version_to_disk(self, version: StateVersion):
        """Save a version to disk."""
        version_path = self.version_dir / f"version_{version.version_id}.json"
        version_data = {
            "version_id": version.version_id,
            "timestamp": version.timestamp.isoformat(),
            "state_data": version.state_data,
            "parent_version_id": version.parent_version_id,
            "metadata": version.metadata,
            "checksum": version.checksum
        }
        
        with open(version_path, 'w') as f:
            json.dump(version_data, f, indent=2)
            
    def load_version(self, version_id: str) -> Optional[StateVersion]:
        """Load a specific version from disk."""
        version_path = self.version_dir / f"version_{version_id}.json"
        
        try:
            with open(version_path, 'r') as f:
                version_data = json.load(f)
                
            # Verify checksum
            stored_checksum = version_data["checksum"]
            calculated_checksum = self._calculate_state_hash(version_data["state_data"])
            
            if stored_checksum != calculated_checksum:
                logger.error(f"Checksum mismatch for version {version_id}")
                return None
                
            version = StateVersion(
                version_id=version_data["version_id"],
                timestamp=datetime.fromisoformat(version_data["timestamp"]),
                state_data=version_data["state_data"],
                parent_version_id=version_data["parent_version_id"],
                metadata=version_data["metadata"],
                checksum=version_data["checksum"]
            )
            
            self.versions[version_id] = version
            return version
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load version {version_id}: {e}")
            return None
            
    def get_version_diff(self, from_version_id: str, to_version_id: str) -> Optional[StateDiff]:
        """Calculate the difference between two versions."""
        from_version = self.versions.get(from_version_id) or self.load_version(from_version_id)
        to_version = self.versions.get(to_version_id) or self.load_version(to_version_id)
        
        if not from_version or not to_version:
            return None
            
        added = {}
        modified = {}
        removed = []
        
        # Find added and modified fields
        for key, value in to_version.state_data.items():
            if key not in from_version.state_data:
                added[key] = value
            elif from_version.state_data[key] != value:
                modified[key] = {
                    "from": from_version.state_data[key],
                    "to": value
                }
                
        # Find removed fields
        for key in from_version.state_data:
            if key not in to_version.state_data:
                removed.append(key)
                
        return StateDiff(
            added=added,
            modified=modified,
            removed=removed,
            from_version=from_version_id,
            to_version=to_version_id,
            timestamp=datetime.now()
        )
        
    def rollback_to_version(self, version_id: str) -> Optional[StateVersion]:
        """Roll back to a specific version."""
        target_version = self.versions.get(version_id) or self.load_version(version_id)
        
        if not target_version:
            logger.error(f"Failed to rollback: Version {version_id} not found")
            return None
            
        # Create new version based on the target version
        rollback_metadata = {
            "rollback_from": self.current_version.version_id if self.current_version else None,
            "rollback_timestamp": datetime.now().isoformat()
        }
        
        new_version = self.create_version(
            target_version.state_data,
            metadata={"type": "rollback", **rollback_metadata}
        )
        
        return new_version
        
    def get_version_history(self, limit: Optional[int] = None) -> List[Tuple[str, datetime]]:
        """Get the version history with timestamps."""
        history = []
        for version_id in reversed(self.version_history):
            version = self.versions.get(version_id)
            if version:
                history.append((version_id, version.timestamp))
            if limit and len(history) >= limit:
                break
        return history
        
    def _prune_old_versions(self):
        """Remove old versions when exceeding the maximum limit."""
        while len(self.version_history) > self.max_versions:
            oldest_version_id = self.version_history.pop(0)
            version = self.versions.pop(oldest_version_id, None)
            if version:
                version_path = self.version_dir / f"version_{version.version_id}.json"
                try:
                    version_path.unlink()
                except FileNotFoundError:
                    pass
                    
    def migrate_state(self, state_data: Dict[str, Any], from_version: str) -> Dict[str, Any]:
        """Migrate state data from one version to current version."""
        if from_version == self.CURRENT_STATE_VERSION:
            return state_data
            
        migrated_data = state_data.copy()
        
        # Apply migrations sequentially
        version_parts = [int(x) for x in from_version.split('.')]
        current_parts = [int(x) for x in self.CURRENT_STATE_VERSION.split('.')]
        
        # Major version migrations
        if version_parts[0] < current_parts[0]:
            migrated_data = self._apply_major_version_migrations(
                migrated_data, 
                version_parts[0], 
                current_parts[0]
            )
            
        # Minor version migrations
        if version_parts[1] < current_parts[1]:
            migrated_data = self._apply_minor_version_migrations(
                migrated_data,
                version_parts[1],
                current_parts[1]
            )
            
        # Patch version migrations
        if version_parts[2] < current_parts[2]:
            migrated_data = self._apply_patch_version_migrations(
                migrated_data,
                version_parts[2],
                current_parts[2]
            )
            
        return migrated_data
        
    def _apply_major_version_migrations(
        self, 
        state_data: Dict[str, Any], 
        from_version: int, 
        to_version: int
    ) -> Dict[str, Any]:
        """Apply major version migrations."""
        migrated_data = state_data.copy()
        
        # Add your major version migrations here
        # Example:
        # if from_version < 1 and to_version >= 1:
        #     migrated_data = self._migrate_to_v1(migrated_data)
        
        return migrated_data
        
    def _apply_minor_version_migrations(
        self, 
        state_data: Dict[str, Any], 
        from_version: int, 
        to_version: int
    ) -> Dict[str, Any]:
        """Apply minor version migrations."""
        migrated_data = state_data.copy()
        
        # Add your minor version migrations here
        
        return migrated_data
        
    def _apply_patch_version_migrations(
        self, 
        state_data: Dict[str, Any], 
        from_version: int, 
        to_version: int
    ) -> Dict[str, Any]:
        """Apply patch version migrations."""
        migrated_data = state_data.copy()
        
        # Add your patch version migrations here
        
        return migrated_data 