import unittest
from datetime import datetime
from pathlib import Path
import tempfile
import shutil
import json

from src.core.state_versioning.state_version_manager import (
    StateVersionManager,
    StateVersion,
    StateDiff
)

class TestStateVersioning(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for version files
        self.temp_dir = Path(tempfile.mkdtemp())
        self.version_manager = StateVersionManager(self.temp_dir)
        
        # Sample test data
        self.test_state = {
            "player_data": {
                "health": 100,
                "level": 1,
                "experience": 0
            },
            "world_state": {
                "current_region": "starting_area",
                "time_of_day": 12
            }
        }
        
    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)
        
    def test_create_version(self):
        # Test creating a new version
        version = self.version_manager.create_version(self.test_state)
        
        self.assertIsNotNone(version)
        self.assertEqual(version.state_data, self.test_state)
        self.assertIsNone(version.parent_version_id)
        self.assertTrue(version.checksum)
        
        # Test version file was created
        version_file = self.temp_dir / f"version_{version.version_id}.json"
        self.assertTrue(version_file.exists())
        
        # Test creating a second version
        modified_state = self.test_state.copy()
        modified_state["player_data"]["health"] = 90
        
        second_version = self.version_manager.create_version(modified_state)
        self.assertEqual(second_version.parent_version_id, version.version_id)
        
    def test_version_loading(self):
        # Create a version
        original_version = self.version_manager.create_version(self.test_state)
        version_id = original_version.version_id
        
        # Clear cached versions
        self.version_manager.versions.clear()
        
        # Load version from disk
        loaded_version = self.version_manager.load_version(version_id)
        
        self.assertIsNotNone(loaded_version)
        self.assertEqual(loaded_version.version_id, original_version.version_id)
        self.assertEqual(loaded_version.state_data, original_version.state_data)
        self.assertEqual(loaded_version.checksum, original_version.checksum)
        
    def test_version_diffing(self):
        # Create initial version
        first_version = self.version_manager.create_version(self.test_state)
        
        # Create modified version
        modified_state = self.test_state.copy()
        modified_state["player_data"]["health"] = 90
        modified_state["player_data"]["new_field"] = "test"
        del modified_state["world_state"]["time_of_day"]
        
        second_version = self.version_manager.create_version(modified_state)
        
        # Get diff between versions
        diff = self.version_manager.get_version_diff(
            first_version.version_id,
            second_version.version_id
        )
        
        self.assertIsNotNone(diff)
        self.assertEqual(diff.added, {"player_data.new_field": "test"})
        self.assertEqual(diff.modified, {
            "player_data.health": {
                "from": 100,
                "to": 90
            }
        })
        self.assertEqual(diff.removed, ["world_state.time_of_day"])
        
    def test_version_rollback(self):
        # Create initial version
        first_version = self.version_manager.create_version(self.test_state)
        
        # Create modified version
        modified_state = self.test_state.copy()
        modified_state["player_data"]["health"] = 90
        second_version = self.version_manager.create_version(modified_state)
        
        # Rollback to first version
        rollback_version = self.version_manager.rollback_to_version(first_version.version_id)
        
        self.assertIsNotNone(rollback_version)
        self.assertEqual(rollback_version.state_data, first_version.state_data)
        self.assertEqual(
            rollback_version.metadata["rollback_from"],
            second_version.version_id
        )
        
    def test_version_pruning(self):
        # Set a small max_versions limit
        self.version_manager.max_versions = 2
        
        # Create multiple versions
        versions = []
        for i in range(3):
            state = self.test_state.copy()
            state["player_data"]["health"] = 100 - i
            versions.append(self.version_manager.create_version(state))
            
        # Check that old versions were pruned
        self.assertEqual(len(self.version_manager.versions), 2)
        self.assertNotIn(versions[0].version_id, self.version_manager.versions)
        self.assertIn(versions[1].version_id, self.version_manager.versions)
        self.assertIn(versions[2].version_id, self.version_manager.versions)
        
    def test_version_migration(self):
        # Test migrating from an old version format
        old_state = {
            "player": {  # Old format used "player" instead of "player_data"
                "hp": 100,  # Old format used "hp" instead of "health"
                "level": 1
            }
        }
        
        migrated_state = self.version_manager.migrate_state(old_state, "0.9.0")
        
        # Check that the state was properly migrated
        self.assertIn("player_data", migrated_state)
        self.assertEqual(migrated_state["player_data"]["health"], 100)
        
    def test_checksum_verification(self):
        # Create a version
        version = self.version_manager.create_version(self.test_state)
        version_id = version.version_id
        
        # Tamper with the saved file
        version_path = self.temp_dir / f"version_{version_id}.json"
        with open(version_path, 'r') as f:
            data = json.load(f)
            
        data["state_data"]["player_data"]["health"] = 50
        
        with open(version_path, 'w') as f:
            json.dump(data, f)
            
        # Try to load the tampered version
        loaded_version = self.version_manager.load_version(version_id)
        self.assertIsNone(loaded_version)  # Should fail checksum verification
        
    def test_version_history(self):
        # Create multiple versions
        versions = []
        for i in range(3):
            state = self.test_state.copy()
            state["player_data"]["health"] = 100 - i
            versions.append(self.version_manager.create_version(state))
            
        # Get version history
        history = self.version_manager.get_version_history()
        
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0][0], versions[2].version_id)  # Most recent first
        self.assertEqual(history[2][0], versions[0].version_id)  # Oldest last
        
        # Test history limit
        limited_history = self.version_manager.get_version_history(limit=2)
        self.assertEqual(len(limited_history), 2)
        self.assertEqual(limited_history[0][0], versions[2].version_id)

if __name__ == '__main__':
    unittest.main() 