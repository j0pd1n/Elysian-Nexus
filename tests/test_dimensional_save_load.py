import unittest
import os
import json
import tempfile
import shutil
from datetime import datetime
from src.combat_system.dimensional_combat import DimensionalCombat, DimensionalLayer, DimensionalEffect
from src.combat_system.dimensional_state_manager import DimensionalStateManager

class TestDimensionalSaveLoad(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.temp_dir = tempfile.mkdtemp()
        self.combat_system = DimensionalCombat()
        self.state_manager = DimensionalStateManager(
            self.combat_system,
            save_dir=self.temp_dir
        )
        
    def tearDown(self):
        """Clean up after tests"""
        shutil.rmtree(self.temp_dir)
        
    def test_save_creation(self):
        """Test save file creation"""
        save_path = self.state_manager.save_state("test_save")
        
        self.assertTrue(os.path.exists(save_path))
        with open(save_path, 'r') as f:
            data = json.load(f)
            
        self.assertEqual(data['version'], self.state_manager.current_version)
        self.assertIn('states', data)
        self.assertIn('active_effects', data)
        self.assertIn('stability_history', data)
        
    def test_state_persistence(self):
        """Test that state is correctly persisted"""
        # Modify state
        self.combat_system.update_dimensional_stability(
            DimensionalLayer.PHYSICAL,
            -0.5
        )
        self.combat_system.add_dimensional_effect(
            DimensionalLayer.PHYSICAL,
            DimensionalEffect.RESONANCE
        )
        
        # Save state
        save_path = self.state_manager.save_state("test_persistence")
        
        # Reset combat system
        self.combat_system = DimensionalCombat()
        self.state_manager = DimensionalStateManager(
            self.combat_system,
            save_dir=self.temp_dir
        )
        
        # Load state
        self.state_manager.load_state("test_persistence")
        
        # Verify state
        physical_state = self.combat_system.dimensional_states[DimensionalLayer.PHYSICAL]
        self.assertEqual(physical_state.stability, 0.5)
        self.assertIn(DimensionalEffect.RESONANCE, physical_state.active_effects)
        
    def test_stability_history(self):
        """Test stability history tracking and persistence"""
        # Record some stability values
        self.state_manager.record_stability(DimensionalLayer.PHYSICAL, 1.0)
        self.state_manager.record_stability(DimensionalLayer.PHYSICAL, 0.8)
        self.state_manager.record_stability(DimensionalLayer.PHYSICAL, 0.6)
        
        # Save and reload
        self.state_manager.save_state("test_history")
        
        new_manager = DimensionalStateManager(
            DimensionalCombat(),
            save_dir=self.temp_dir
        )
        new_manager.load_state("test_history")
        
        # Verify history
        history = new_manager.stability_history[DimensionalLayer.PHYSICAL]
        self.assertEqual(len(history), 3)
        self.assertEqual(history[-1], 0.6)
        
    def test_version_compatibility(self):
        """Test version compatibility checks"""
        # Create save with current version
        save_path = os.path.join(self.temp_dir, "test_version.json")
        save_data = {
            "timestamp": datetime.now().isoformat(),
            "version": self.state_manager.current_version,
            "states": {},
            "active_effects": {},
            "stability_history": {}
        }
        
        with open(save_path, 'w') as f:
            json.dump(save_data, f)
            
        # Should load without error
        self.assertTrue(self.state_manager.load_state("test_version"))
        
        # Create save with unsupported version
        save_data["version"] = "0.0.1"
        with open(save_path, 'w') as f:
            json.dump(save_data, f)
            
        # Should raise error
        with self.assertRaises(ValueError):
            self.state_manager.load_state("test_version")
            
    def test_auto_save(self):
        """Test auto-save functionality"""
        # Modify state
        self.combat_system.update_dimensional_stability(
            DimensionalLayer.PHYSICAL,
            -0.3
        )
        
        # Create auto-save
        save_path = self.state_manager.auto_save()
        self.assertIsNotNone(save_path)
        self.assertTrue(os.path.exists(save_path))
        
        # Verify auto-save content
        new_manager = DimensionalStateManager(
            DimensionalCombat(),
            save_dir=self.temp_dir
        )
        new_manager.load_state("autosave_dimensional")
        
        physical_state = new_manager.combat_system.dimensional_states[DimensionalLayer.PHYSICAL]
        self.assertEqual(physical_state.stability, 0.7)
        
    def test_save_cleanup(self):
        """Test old save cleanup"""
        # Create multiple saves
        for i in range(15):
            self.state_manager.save_state(f"test_save_{i}")
            
        # Clean up old saves
        self.state_manager.cleanup_old_saves(max_saves=10)
        
        # Check remaining saves
        saves = self.state_manager.get_save_list()
        self.assertEqual(len(saves), 10)
        
        # Verify most recent saves were kept
        save_names = [save['name'] for save in saves]
        self.assertIn("test_save_14", save_names)
        self.assertNotIn("test_save_0", save_names)
        
    def test_backup_creation(self):
        """Test backup creation"""
        # Create backup
        backup_path = self.state_manager.create_backup()
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))
        
        # Verify backup name format
        self.assertTrue("backup_dimensional_" in os.path.basename(backup_path))
        
    def test_save_list(self):
        """Test save list retrieval"""
        # Create some saves
        save_times = []
        for i in range(3):
            save_time = datetime.now()
            save_times.append(save_time)
            
            save_data = {
                "timestamp": save_time.isoformat(),
                "version": self.state_manager.current_version,
                "states": {},
                "active_effects": {},
                "stability_history": {}
            }
            
            save_path = os.path.join(self.temp_dir, f"test_save_{i}.json")
            with open(save_path, 'w') as f:
                json.dump(save_data, f)
                
        # Get save list
        saves = self.state_manager.get_save_list()
        
        # Verify list
        self.assertEqual(len(saves), 3)
        for save in saves:
            self.assertIn('name', save)
            self.assertIn('timestamp', save)
            self.assertIn('version', save)

if __name__ == '__main__':
    unittest.main() 