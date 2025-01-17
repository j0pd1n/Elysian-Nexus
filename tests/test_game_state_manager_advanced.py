import unittest
import tempfile
import shutil
import time
import random
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.core.game_state.game_state_manager import GameStateManager, CheckpointData
from src.core.game_state.enums import GameState, GameMode, DifficultyLevel, Location, QuestStatus

class TestGameStateManagerAdvanced(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = GameStateManager()
        self.manager.save_directory = Path(self.temp_dir) / "saves"
        self.manager.checkpoint_directory = Path(self.temp_dir) / "checkpoints"
        self.manager.save_directory.mkdir(exist_ok=True)
        self.manager.checkpoint_directory.mkdir(exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_rapid_state_transitions(self):
        """Test rapid state transitions under heavy load."""
        transitions = 0
        start_time = time.time()
        duration = 2.0  # Test for 2 seconds
        
        # Setup valid transition path
        self.manager.current_state = GameState.TOWN
        self.manager.player_data['light_source'] = True
        
        while time.time() - start_time < duration:
            # Cycle through states rapidly
            self.manager.change_state(GameState.EXPLORATION)
            self.manager.change_state(GameState.INVENTORY)
            self.manager.change_state(GameState.TOWN)
            transitions += 3
        
        # Verify system stability
        self.assertIsNotNone(self.manager.current_state)
        print(f"Completed {transitions} transitions in {duration} seconds")

    def test_concurrent_state_access(self):
        """Test concurrent access to game state."""
        def state_changer():
            for _ in range(100):
                self.manager.change_state(GameState.EXPLORATION)
                self.manager.change_state(GameState.TOWN)
                time.sleep(0.001)  # Small delay to simulate real usage

        def checkpoint_creator():
            for _ in range(50):
                self.manager._check_auto_checkpoint()
                time.sleep(0.002)

        threads = [
            threading.Thread(target=state_changer),
            threading.Thread(target=state_changer),
            threading.Thread(target=checkpoint_creator)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Verify system integrity
        self.assertIn(self.manager.current_state, {GameState.EXPLORATION, GameState.TOWN})

    def test_checkpoint_stress(self):
        """Test checkpoint system under heavy load."""
        checkpoints_created = 0
        start_time = time.time()
        
        # Create rapid checkpoint triggers
        while time.time() - start_time < 1.0:  # Test for 1 second
            self.manager.world_state['boss_defeated'] = True
            self.manager._check_auto_checkpoint()
            self.manager.world_state['area_discovered'] = True
            self.manager._check_auto_checkpoint()
            checkpoints_created += 2
        
        # Verify checkpoint files
        checkpoint_files = list(self.manager.checkpoint_directory.glob("checkpoint_*.json"))
        print(f"Created {checkpoints_created} checkpoints, files: {len(checkpoint_files)}")

    def test_complex_environmental_cascade(self):
        """Test complex cascading environmental effects."""
        # Setup initial conditions
        self.manager.current_state = GameState.EXPLORATION
        self.manager.environmental_conditions.weather_type = 'storm'
        self.manager.environmental_conditions.visibility = 0.3
        
        # Trigger cascading environmental changes
        events = [
            ('temperature', -10),  # Cold front
            ('wind_speed', 35),    # Strong winds
            ('visibility', 0.1),   # Poor visibility
            ('is_hazardous', True) # Hazardous conditions
        ]
        
        for attr, value in events:
            # Update condition
            setattr(self.manager.environmental_conditions, attr, value)
            # Verify state restrictions
            self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
            # Calculate danger
            danger = self.manager._calculate_danger_level()
            self.assertGreater(danger, 0.5)

    def test_resource_depletion_stress(self):
        """Test system behavior under extreme resource conditions."""
        resources = ['health_percentage', 'mana_percentage', 'stamina_percentage', 
                    'ammunition_percentage', 'consumables_percentage']
        
        # Test rapid resource fluctuation
        for _ in range(100):
            # Randomly deplete resources
            for resource in resources:
                self.manager.player_data[resource] = random.random()
            
            # Calculate resource status
            status = self.manager._calculate_resource_status()
            # Verify danger level adjustment
            danger = self.manager._calculate_danger_level()
            
            # Verify checkpoint triggers
            if status < 0.2:
                self.assertTrue(self._check_health_triggers(
                    self.manager.player_data['health_percentage'] * 100, 
                    status
                ))

    def test_faction_warfare_simulation(self):
        """Test system behavior during complex faction interactions."""
        factions = ['merchants_guild', 'warriors_clan', 'mystic_order']
        locations = [Location.NEXUS_CITY, Location.CRYSTAL_PEAKS, Location.SHADOW_CAVES]
        
        for _ in range(50):  # Simulate 50 turns of faction warfare
            # Update faction controls
            for location in locations:
                controlling_faction = random.choice(factions)
                self.manager.world_state[f'{location.name}_controlling_faction'] = controlling_faction
            
            # Update faction standings
            for faction in factions:
                self.manager.faction_standings[faction] = random.randint(-100, 100)
            
            # Attempt state transitions
            for location in locations:
                self.manager.current_location = location
                # Verify state access based on faction standings
                self._verify_faction_access()

    def test_performance_checkpoint_creation(self):
        """Test checkpoint creation performance under load."""
        # Prepare large game state
        self.manager.player_data = {f'item_{i}': i for i in range(1000)}
        self.manager.world_state = {f'state_{i}': i for i in range(1000)}
        
        # Measure checkpoint creation time
        times = []
        for _ in range(100):
            start = time.time()
            self.manager.create_checkpoint()
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"Average checkpoint creation time: {avg_time:.4f} seconds")
        self.assertLess(avg_time, 0.1)  # Should be reasonably fast

    def test_parallel_save_load(self):
        """Test parallel save/load operations."""
        def save_load_cycle(slot):
            self.manager.save_game(slot)
            return self.manager.load_game(slot)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(save_load_cycle, i) for i in range(10)]
            results = [f.result() for f in as_completed(futures)]
            
        self.assertTrue(all(results))

    def test_extreme_state_transitions(self):
        """Test state transitions under extreme conditions."""
        # Setup complex state
        self.manager.current_state = GameState.BATTLE
        self.manager.world_state.update({
            'in_combat': True,
            'boss_battle': True,
            'elite_enemies': True,
            'surrounded': True,
            'low_health': True,
            'out_of_resources': True,
            'being_pursued': True,
            'hazardous_environment': True
        })
        
        # Test all possible state transitions
        for state in GameState:
            result = self.manager.change_state(state)
            # Verify only valid transitions are allowed
            if state == GameState.PAUSED:
                self.assertTrue(result)
            else:
                self.assertFalse(result)

    def test_checkpoint_recovery(self):
        """Test checkpoint recovery under extreme conditions."""
        # Create checkpoints with increasing complexity
        checkpoints = []
        for i in range(10):
            self.manager.player_data[f'complex_data_{i}'] = {
                'nested': {'data': [1] * 1000},
                'more_nested': {'data': {'deep': [2] * 1000}}
            }
            checkpoints.append(self.manager.create_checkpoint())
        
        # Test rapid checkpoint loading
        for checkpoint in checkpoints:
            self.manager.load_checkpoint(checkpoint)
            # Verify data integrity
            self.assertIn(f'complex_data_{len(checkpoints)-1}', 
                         self.manager.player_data)

    def test_environmental_transition_matrix(self):
        """Test all possible environmental condition combinations."""
        weather_types = ['clear', 'rain', 'storm', 'blizzard', 'sandstorm']
        times = [0, 6, 12, 18, 23]
        visibilities = [0.1, 0.3, 0.5, 0.8, 1.0]
        
        total_combinations = len(weather_types) * len(times) * len(visibilities)
        valid_transitions = 0
        
        for weather in weather_types:
            for time_of_day in times:
                for visibility in visibilities:
                    self.manager.environmental_conditions.weather_type = weather
                    self.manager.environmental_conditions.time_of_day = time_of_day
                    self.manager.environmental_conditions.visibility = visibility
                    
                    if self.manager._is_safe_to_explore():
                        valid_transitions += 1
        
        print(f"Valid transitions: {valid_transitions}/{total_combinations}")

    def _verify_faction_access(self):
        """Helper method to verify faction-based access rules."""
        controlling_faction = self.manager.world_state.get(
            f'{self.manager.current_location.name}_controlling_faction'
        )
        if controlling_faction:
            standing = self.manager.faction_standings.get(controlling_faction, 0)
            
            # Verify state access based on standing
            self.assertEqual(
                self.manager.change_state(GameState.TOWN),
                standing > -50
            )
            self.assertEqual(
                self.manager.change_state(GameState.SHOP),
                standing > 0
            )

    def _check_health_triggers(self, health_percentage: float, resource_status: float) -> bool:
        """Helper method to check health triggers."""
        return self.manager._check_health_triggers(health_percentage, resource_status)

if __name__ == '__main__':
    unittest.main() 