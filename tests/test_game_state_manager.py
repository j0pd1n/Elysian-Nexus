import unittest
import tempfile
import shutil
from pathlib import Path
from time import sleep, time

from src.core.game_state.game_state_manager import GameStateManager, CheckpointData
from src.core.game_state.enums import GameState, GameMode, DifficultyLevel, Location, QuestStatus

class TestGameStateManager(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for saves and checkpoints
        self.temp_dir = tempfile.mkdtemp()
        self.manager = GameStateManager()
        self.manager.save_directory = Path(self.temp_dir) / "saves"
        self.manager.checkpoint_directory = Path(self.temp_dir) / "checkpoints"
        self.manager.save_directory.mkdir(exist_ok=True)
        self.manager.checkpoint_directory.mkdir(exist_ok=True)

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.temp_dir)

    def test_initial_state(self):
        """Test initial state of the manager."""
        self.assertEqual(self.manager.current_state, GameState.MAIN_MENU)
        self.assertEqual(self.manager.current_mode, GameMode.MENU)
        self.assertEqual(self.manager.difficulty, DifficultyLevel.NORMAL)
        self.assertIsNone(self.manager.current_location)

    def test_conditional_state_transitions(self):
        """Test state transitions with conditions."""
        # Test loading transition (should fail without saves)
        self.assertFalse(self.manager.change_state(GameState.LOADING))
        
        # Create a save and try again
        self.manager.save_game(1)
        self.assertTrue(self.manager.change_state(GameState.LOADING))

        # Test character creation transition
        self.manager.current_state = GameState.CHARACTER_CREATION
        self.assertFalse(self.manager.change_state(GameState.TOWN))  # Should fail without character created
        
        self.manager.player_data['character_created'] = True
        self.assertTrue(self.manager.change_state(GameState.TOWN))

    def test_combat_state_transitions(self):
        """Test combat-related state transitions."""
        # Setup exploration state
        self.manager.current_state = GameState.EXPLORATION
        
        # Cannot enter battle without enemies
        self.assertFalse(self.manager.change_state(GameState.BATTLE))
        
        # Add nearby enemies and try again
        self.manager.world_state['enemies_nearby'] = True
        selfassertTrue(self.manager.change_state(GameState.BATTLE))
        
        # Cannot leave battle while in combat
        self.manager.world_state['in_combat'] = True
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        # Can leave after combat ends
        self.manager.world_state['in_combat'] = False
        self.assertTrue(self.manager.change_state(GameState.EXPLORATION))

    def test_location_based_transitions(self):
        """Test location-based state transitions."""
        self.manager.current_state = GameState.EXPLORATION
        
        # Cannot return to town from invalid location
        self.manager.current_location = Location.SHADOW_CAVES
        self.assertFalse(self.manager.change_state(GameState.TOWN))
        
        # Can return to town from valid location
        self.manager.current_location = Location.NEXUS_CITY
        self.assertTrue(self.manager.change_state(GameState.TOWN))

    def test_expanded_difficulty_modifiers(self):
        """Test the expanded set of difficulty modifiers."""
        # Test EASY difficulty modifiers
        self.manager.set_difficulty(DifficultyLevel.EASY)
        self.assertEqual(self.manager.get_difficulty_modifier('stamina_drain_rate'), 0.75)
        self.assertEqual(self.manager.get_difficulty_modifier('dodge_window_multiplier'), 1.5)
        self.assertEqual(self.manager.get_difficulty_modifier('critical_hit_chance'), 1.25)
        self.assertEqual(self.manager.get_difficulty_modifier('merchant_price_multiplier'), 0.9)

        # Test EXPERT difficulty modifiers
        self.manager.set_difficulty(DifficultyLevel.EXPERT)
        self.assertEqual(self.manager.get_difficulty_modifier('stamina_drain_rate'), 1.5)
        self.assertEqual(self.manager.get_difficulty_modifier('dodge_window_multiplier'), 0.5)
        self.assertEqual(self.manager.get_difficulty_modifier('healing_effectiveness'), 0.5)
        self.assertEqual(self.manager.get_difficulty_modifier('merchant_price_multiplier'), 1.25)

    def test_health_based_checkpoint(self):
        """Test checkpoint creation based on health changes."""
        self.manager.player_data['health'] = 100
        self.manager.player_data['max_health'] = 100
        self.manager.last_health_percentage = 100
        
        # No checkpoint on small health change
        self.manager.player_data['health'] = 90
        self._check_auto_checkpoint()
        self.assertIsNone(self.manager.last_checkpoint)
        
        # Checkpoint on significant health drop
        self.manager.player_data['health'] = 60
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)

    def test_quest_completion_checkpoint(self):
        """Test checkpoint creation on quest completion."""
        # Setup quest status
        self.manager.quest_status = {
            'main_quest': QuestStatus.IN_PROGRESS,
            'side_quest': QuestStatus.NOT_STARTED
        }
        
        # Complete a quest
        self.manager.quest_status['side_quest'] = QuestStatus.COMPLETED
        self._check_auto_checkpoint()
        
        # Verify checkpoint was created
        self.assertIsNotNone(self.manager.last_checkpoint)
        self.assertEqual(self.manager.last_checkpoint.quest_status['side_quest'], QuestStatus.COMPLETED)

    def test_level_up_checkpoint(self):
        """Test checkpoint creation on level up."""
        # Trigger level up
        self.manager.player_data['leveled_up'] = True
        self._check_auto_checkpoint()
        
        # Verify checkpoint was created and flag was reset
        self.assertIsNotNone(self.manager.last_checkpoint)
        self.assertFalse(self.manager.player_data['leveled_up'])

    def test_rare_item_checkpoint(self):
        """Test checkpoint creation on rare item acquisition."""
        # Simulate finding a rare item
        self.manager.player_data['rare_item_found'] = True
        self._check_auto_checkpoint()
        
        # Verify checkpoint was created and flag was reset
        self.assertIsNotNone(self.manager.last_checkpoint)
        self.assertFalse(self.manager.player_data['rare_item_found'])

    def test_shop_hours_transition(self):
        """Test shop transitions based on game time."""
        self.manager.current_state = GameState.TOWN
        
        # Test during shop hours
        self.manager.world_state['time_of_day'] = 14  # 2 PM
        self.assertTrue(self.manager.change_state(GameState.SHOP))
        
        # Test outside shop hours
        self.manager.world_state['time_of_day'] = 22  # 10 PM
        self.assertFalse(self.manager.change_state(GameState.SHOP))

    def test_town_lockdown_transitions(self):
        """Test town transitions during lockdown."""
        self.manager.current_state = GameState.TOWN
        
        # Test normal conditions
        self.assertTrue(self.manager.change_state(GameState.EXPLORATION))
        
        # Test during lockdown
        self.manager.world_state['town_lockdown'] = True
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        # Test during active event
        self.manager.world_state['town_lockdown'] = False
        self.manager.world_state['active_event'] = True
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))

    def test_combat_inventory_restrictions(self):
        """Test combat-related inventory access restrictions."""
        self.manager.current_state = GameState.BATTLE
        
        # Test during boss battle
        self.manager.world_state['boss_battle'] = True
        self.assertFalse(self.manager.change_state(GameState.INVENTORY))
        
        # Test normal combat with insufficient turns
        self.manager.world_state['boss_battle'] = False
        self.manager.player_data['combat_turns_since_inventory'] = 2
        self.assertFalse(self.manager.change_state(GameState.INVENTORY))
        
        # Test after sufficient turns
        self.manager.player_data['combat_turns_since_inventory'] = 3
        self.assertTrue(self.manager.change_state(GameState.INVENTORY))

    def test_danger_level_calculation(self):
        """Test danger level calculation under various conditions."""
        # Test base state
        self.assertAlmostEqual(self.manager._calculate_danger_level(), 0.0)
        
        # Test combat danger
        self.manager.world_state['in_combat'] = True
        self.assertAlmostEqual(self.manager._calculate_danger_level(), 0.3)
        
        # Test boss battle
        self.manager.world_state['boss_battle'] = True
        self.assertAlmostEqual(self.manager._calculate_danger_level(), 0.8)
        
        # Test environmental factors
        self.manager.world_state['hazardous_environment'] = True
        self.manager.world_state['extreme_weather'] = True
        self.assertAlmostEqual(self.manager._calculate_danger_level(), 1.0)

    def test_dynamic_checkpoint_intervals(self):
        """Test checkpoint creation with dynamic intervals based on danger."""
        # Set up initial state
        self.manager.checkpoint_interval = 10  # 10 seconds for testing
        self.manager.current_state = GameState.EXPLORATION
        
        # Test normal interval
        sleep(5)
        self._check_auto_checkpoint()
        self.assertIsNone(self.manager.last_checkpoint)
        
        # Test with high danger
        self.manager.world_state['in_combat'] = True
        self.manager.world_state['boss_battle'] = True
        sleep(3)  # Should trigger earlier due to high danger
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)

    def test_advanced_difficulty_modifiers(self):
        """Test the expanded set of difficulty modifiers."""
        # Test EASY difficulty advanced modifiers
        self.manager.set_difficulty(DifficultyLevel.EASY)
        self.assertEqual(self.manager.get_difficulty_modifier('enemy_aggression_multiplier'), 0.75)
        self.assertEqual(self.manager.get_difficulty_modifier('boss_damage_multiplier'), 0.75)
        self.assertEqual(self.manager.get_difficulty_modifier('skill_xp_multiplier'), 1.25)
        self.assertEqual(self.manager.get_difficulty_modifier('reputation_gain_multiplier'), 1.25)
        
        # Test EXPERT difficulty advanced modifiers
        self.manager.set_difficulty(DifficultyLevel.EXPERT)
        self.assertEqual(self.manager.get_difficulty_modifier('critical_damage_multiplier'), 1.5)
        self.assertEqual(self.manager.get_difficulty_modifier('durability_loss_rate'), 1.5)
        self.assertEqual(self.manager.get_difficulty_modifier('weather_effect_intensity'), 1.5)
        self.assertEqual(self.manager.get_difficulty_modifier('sneak_attack_multiplier'), 1.5)

    def test_special_event_checkpoints(self):
        """Test checkpoint creation for special events."""
        # Test boss defeat checkpoint
        self.manager.world_state['boss_defeated'] = True
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)
        self.assertFalse(self.manager.world_state.get('boss_defeated', False))  # Should be reset
        
        # Test area discovery checkpoint
        self.manager.last_checkpoint = None
        self.manager.world_state['area_discovered'] = True
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)
        self.assertFalse(self.manager.world_state.get('area_discovered', False))

    def test_recovery_checkpoints(self):
        """Test checkpoint creation during recovery scenarios."""
        # Set up recovery scenario
        self.manager.consecutive_deaths = 2
        self.manager.player_data['health'] = 80
        self.manager.player_data['max_health'] = 100
        
        # Test checkpoint creation on recovery
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)
        self.assertEqual(self.manager.consecutive_deaths, 0)  # Should be reset

    def test_safe_zone_mechanics(self):
        """Test safe zone related state transitions."""
        self.manager.current_state = GameState.EXPLORATION
        self.manager.world_state['enemies_nearby'] = True
        
        # Test battle prevention in safe zone
        self.manager.world_state['in_safe_zone'] = True
        self.assertFalse(self.manager.change_state(GameState.BATTLE))
        
        # Test battle allowance outside safe zone
        self.manager.world_state['in_safe_zone'] = False
        self.assertTrue(self.manager.change_state(GameState.BATTLE))

    def test_environmental_state_restrictions(self):
        """Test state transitions based on environmental conditions."""
        self.manager.current_state = GameState.TOWN
        
        # Test storm conditions
        self.manager.environmental_conditions.active_effects.add('storm')
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        # Test with proper gear
        self.manager.player_data['storm_gear'] = True
        self.assertTrue(self.manager.change_state(GameState.EXPLORATION))
        
        # Test extreme heat conditions
        self.manager.environmental_conditions.active_effects.clear()
        self.manager.environmental_conditions.active_effects.add('extreme_heat')
        self.manager.environmental_conditions.time_of_day = 13  # Peak heat
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        # Test with heat resistance
        self.manager.player_data['heat_resistance'] = 75
        self.assertTrue(self.manager.change_state(GameState.EXPLORATION))

    def test_faction_based_restrictions(self):
        """Test state transitions based on faction standings."""
        self.manager.current_state = GameState.EXPLORATION
        self.manager.current_location = Location.NEXUS_CITY
        
        # Set controlling faction
        self.manager.world_state['NEXUS_CITY_controlling_faction'] = 'merchants_guild'
        
        # Test with neutral standing
        self.manager.faction_standings['merchants_guild'] = 0
        self.assertTrue(self.manager.change_state(GameState.TOWN))
        self.assertFalse(self.manager.change_state(GameState.SHOP))  # Requires positive standing
        
        # Test with negative standing
        self.manager.faction_standings['merchants_guild'] = -60
        self.assertFalse(self.manager.change_state(GameState.TOWN))
        
        # Test with positive standing
        self.manager.faction_standings['merchants_guild'] = 50
        self.assertTrue(self.manager.change_state(GameState.SHOP))

    def test_environmental_checkpoint_triggers(self):
        """Test checkpoint creation based on environmental changes."""
        # Test weather change trigger
        self.manager.world_state['weather_changed'] = True
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)
        self.assertFalse(self.manager.world_state.get('weather_changed', False))
        
        # Test day/night transition
        self.manager.last_checkpoint = None
        self.manager.world_state['previous_time_of_day'] = 17
        self.manager.environmental_conditions.time_of_day = 18
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)
        
        # Test hazardous area entry
        self.manager.last_checkpoint = None
        self.manager.environmental_conditions.is_hazardous = True
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)

    def test_faction_checkpoint_triggers(self):
        """Test checkpoint creation based on faction changes."""
        # Test reputation change trigger
        self.manager.faction_standings['merchants_guild'] = 0
        self.manager.world_state['previous_faction_standing_merchants_guild'] = -30
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)
        
        # Test faction territory change
        self.manager.last_checkpoint = None
        self.manager.world_state['faction_territory_changed'] = True
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)
        self.assertFalse(self.manager.world_state.get('faction_territory_changed', False))
        
        # Test becoming friendly with faction
        self.manager.last_checkpoint = None
        self.manager.faction_standings['merchants_guild'] = 75
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)

    def test_exploration_safety_conditions(self):
        """Test exploration safety checks based on environmental conditions."""
        self.manager.current_state = GameState.TOWN
        
        # Test extreme weather prevention
        self.manager.environmental_conditions.weather_type = 'blizzard'
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        # Test visibility requirements
        self.manager.environmental_conditions.weather_type = 'clear'
        self.manager.environmental_conditions.visibility = 0.1
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        # Test with enhanced vision
        self.manager.player_data['enhanced_vision'] = True
        self.assertTrue(self.manager.change_state(GameState.EXPLORATION))
        
        # Test wind conditions
        self.manager.environmental_conditions.visibility = 1.0
        self.manager.environmental_conditions.wind_speed = 35
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))

    def test_night_exploration_requirements(self):
        """Test night exploration requirements."""
        self.manager.current_state = GameState.TOWN
        self.manager.environmental_conditions.time_of_day = 23  # Night time
        
        # Test without light source or night vision
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        # Test with light source
        self.manager.player_data['light_source'] = True
        self.assertTrue(self.manager.change_state(GameState.EXPLORATION))
        
        # Test with night vision
        self.manager.player_data['light_source'] = False
        self.manager.player_data['night_vision'] = True
        self.assertTrue(self.manager.change_state(GameState.EXPLORATION))

    def test_enhanced_danger_calculation(self):
        """Test enhanced danger level calculation."""
        # Test environmental factors
        self.manager.environmental_conditions.is_hazardous = True
        self.manager.environmental_conditions.terrain_type = 'treacherous'
        self.manager.environmental_conditions.light_level = 0.2
        self.manager.environmental_conditions.visibility = 0.4
        danger = self.manager._calculate_danger_level()
        self.assertGreater(danger, 0.5)
        
        # Test faction danger
        self.manager.current_location = Location.NEXUS_CITY
        self.manager.world_state['NEXUS_CITY_controlling_faction'] = 'merchants_guild'
        self.manager.faction_standings['merchants_guild'] = -80
        danger = self.manager._calculate_danger_level()
        self.assertGreater(danger, 0.8)

    def test_checkpoint_state_updates(self):
        """Test checkpoint state tracking updates."""
        # Setup initial state
        self.manager.environmental_conditions.time_of_day = 14
        self.manager.environmental_conditions.is_hazardous = True
        self.manager.faction_standings = {'merchants_guild': 50}
        
        # Create checkpoint and verify state updates
        self.manager.create_checkpoint()
        self._check_auto_checkpoint()
        
        self.assertEqual(
            self.manager.world_state['previous_time_of_day'],
            self.manager.environmental_conditions.time_of_day
        )
        self.assertEqual(
            self.manager.world_state['previous_is_hazardous'],
            self.manager.environmental_conditions.is_hazardous
        )
        self.assertEqual(
            self.manager.world_state['previous_faction_standing_merchants_guild'],
            self.manager.faction_standings['merchants_guild']
        )

    def test_time_based_checkpoint_triggers(self):
        """Test time-based checkpoint triggers with dynamic intervals."""
        self.manager.checkpoint_interval = 10  # 10 seconds for testing
        
        # Test normal interval
        self.manager.last_checkpoint_time = time.time() - 5
        self.assertFalse(self._check_time_based_triggers())
        
        # Test with valuable items
        self.manager.player_data['valuable_items_found'] = 2
        self.manager.last_checkpoint_time = time.time() - 8
        self.assertTrue(self._check_time_based_triggers())
        
        # Test in dangerous area
        self.manager.current_location = Location.SHADOW_CAVES
        self.manager.world_state['SHADOW_CAVES_danger_level'] = 0.8
        self.manager.last_checkpoint_time = time.time() - 4
        self.assertTrue(self._check_time_based_triggers())

    def test_discovery_checkpoint_triggers(self):
        """Test discovery-based checkpoint triggers."""
        # Test secret area discovery
        self.manager.world_state['secret_found'] = True
        self.assertTrue(self._check_location_triggers())
        
        # Test strategic position
        self.manager.world_state['secret_found'] = False
        self.manager.world_state['strategic_position_reached'] = True
        self.assertTrue(self._check_location_triggers())
        
        # Test resource discovery
        self.manager.world_state['strategic_position_reached'] = False
        self.manager.world_state['resource_node_found'] = True
        self.assertTrue(self._check_location_triggers())

    def test_combat_intensity_calculation(self):
        """Test combat intensity calculation under various conditions."""
        # Test base combat
        self.manager.world_state['in_combat'] = True
        intensity = self.manager._calculate_combat_intensity()
        self.assertAlmostEqual(intensity, 0.3)
        
        # Test boss battle
        self.manager.world_state['boss_battle'] = True
        intensity = self.manager._calculate_combat_intensity()
        self.assertAlmostEqual(intensity, 0.7)
        
        # Test critical situation
        self.manager.world_state['surrounded'] = True
        self.manager.world_state['low_health'] = True
        self.manager.environmental_conditions.is_hazardous = True
        intensity = self.manager._calculate_combat_intensity()
        self.assertAlmostEqual(intensity, 1.0)

    def test_resource_status_calculation(self):
        """Test resource status calculation."""
        # Test full resources
        self.manager.player_data.update({
            'health_percentage': 1.0,
            'mana_percentage': 1.0,
            'stamina_percentage': 1.0,
            'ammunition_percentage': 1.0,
            'consumables_percentage': 1.0
        })
        self.assertAlmostEqual(self.manager._calculate_resource_status(), 1.0)
        
        # Test critical resources
        self.manager.player_data.update({
            'health_percentage': 0.2,
            'mana_percentage': 0.1,
            'stamina_percentage': 0.15,
            'ammunition_percentage': 0.05,
            'consumables_percentage': 0.0
        })
        self.assertAlmostEqual(self.manager._calculate_resource_status(), 0.1)

    def test_progression_checkpoint_triggers(self):
        """Test progression-based checkpoint triggers."""
        # Test skill progression
        self.manager.player_data['skill_unlocked'] = True
        self.assertTrue(self._check_progression_triggers())
        
        # Test equipment progression
        self.manager.player_data['skill_unlocked'] = False
        self.manager.player_data['equipment_upgraded'] = True
        self.assertTrue(self._check_progression_triggers())
        
        # Test collection completion
        self.manager.player_data['equipment_upgraded'] = False
        self.manager.player_data['collection_completed'] = True
        self.assertTrue(self._check_progression_triggers())

    def test_special_event_checkpoint_triggers(self):
        """Test special event checkpoint triggers."""
        # Test world events
        self.manager.world_state['world_boss_appeared'] = True
        self.assertTrue(self._check_special_event_triggers())
        
        # Test time-limited events
        self.manager.world_state['world_boss_appeared'] = False
        self.manager.world_state['daily_objective_completed'] = True
        self.assertTrue(self._check_special_event_triggers())
        
        # Test story events
        self.manager.world_state['daily_objective_completed'] = False
        self.manager.world_state['story_branch_chosen'] = True
        self.assertTrue(self._check_special_event_triggers())

    def test_combat_checkpoint_triggers(self):
        """Test combat-related checkpoint triggers."""
        # Test high intensity combat
        self.manager.world_state.update({
            'in_combat': True,
            'boss_battle': True,
            'surrounded': True
        })
        self.assertTrue(self._check_combat_triggers(0.9))
        
        # Test combat achievements
        self.manager.world_state.update({
            'boss_battle': False,
            'surrounded': False,
            'perfect_combat': True
        })
        self.assertTrue(self._check_combat_triggers(0.3))
        
        # Test strategic events
        self.manager.world_state.update({
            'perfect_combat': False,
            'ambush_survived': True
        })
        self.assertTrue(self._check_combat_triggers(0.3))

    def test_health_resource_checkpoint_triggers(self):
        """Test health and resource-related checkpoint triggers."""
        # Test critical resources
        self.assertTrue(self._check_health_triggers(80, 0.15))
        
        # Test buff acquisition
        self.manager.world_state['major_buff_acquired'] = True
        self.assertTrue(self._check_health_triggers(100, 1.0))
        
        # Test recovery
        self.manager.world_state['major_buff_acquired'] = False
        self.manager.world_state['full_recovery'] = True
        self.assertTrue(self._check_health_triggers(100, 1.0))

    def test_complex_state_transitions(self):
        """Test complex state transitions with multiple conditions."""
        # Setup initial state
        self.manager.current_state = GameState.EXPLORATION
        self.manager.current_location = Location.NEXUS_CITY
        self.manager.world_state.update({
            'in_combat': True,
            'enemies_nearby': True,
            'being_pursued': True,
            'town_lockdown': True,
            'active_event': True
        })
        
        # Test multiple blocking conditions
        self.assertFalse(self.manager.change_state(GameState.TOWN))
        
        # Remove conditions one by one
        self.manager.world_state['in_combat'] = False
        self.assertFalse(self.manager.change_state(GameState.TOWN))  # Still being pursued
        
        self.manager.world_state['being_pursued'] = False
        self.assertFalse(self.manager.change_state(GameState.TOWN))  # Still in lockdown
        
        self.manager.world_state['town_lockdown'] = False
        self.assertTrue(self.manager.change_state(GameState.TOWN))  # Finally allowed

    def test_cascading_checkpoint_triggers(self):
        """Test multiple checkpoint triggers occurring simultaneously."""
        # Setup multiple trigger conditions
        self.manager.world_state.update({
            'boss_defeated': True,
            'quest_milestone_reached': True,
            'area_discovered': True,
            'weather_changed': True
        })
        self.manager.player_data.update({
            'leveled_up': True,
            'skill_unlocked': True
        })
        
        # Create checkpoint and verify all flags are reset
        self._check_auto_checkpoint()
        self.assertIsNotNone(self.manager.last_checkpoint)
        
        # Verify all flags were reset
        self.assertFalse(self.manager.world_state.get('boss_defeated', False))
        self.assertFalse(self.manager.world_state.get('quest_milestone_reached', False))
        self.assertFalse(self.manager.world_state.get('area_discovered', False))
        self.assertFalse(self.manager.world_state.get('weather_changed', False))
        self.assertFalse(self.manager.player_data.get('leveled_up', False))
        self.assertFalse(self.manager.player_data.get('skill_unlocked', False))

    def test_environmental_combat_interaction(self):
        """Test interaction between environmental conditions and combat."""
        self.manager.current_state = GameState.EXPLORATION
        self.manager.environmental_conditions.update({
            'weather_type': 'storm',
            'visibility': 0.3,
            'is_hazardous': True
        })
        self.manager.world_state['enemies_nearby'] = True
        
        # Calculate combat intensity with environmental factors
        intensity = self.manager._calculate_combat_intensity()
        self.assertGreater(intensity, 0.5)  # Environmental factors should increase intensity
        
        # Test checkpoint frequency in hazardous combat
        self.manager.checkpoint_interval = 10
        self.manager.last_checkpoint_time = time.time() - 4
        self.assertTrue(self._check_time_based_triggers())  # Should trigger earlier due to danger

    def test_resource_depletion_cascade(self):
        """Test cascading effects of resource depletion."""
        # Setup critical resource state
        self.manager.player_data.update({
            'health_percentage': 0.2,
            'mana_percentage': 0.1,
            'stamina_percentage': 0.1,
            'ammunition_percentage': 0.0,
            'consumables_percentage': 0.0
        })
        
        # Verify danger level increases
        danger = self.manager._calculate_danger_level()
        self.assertGreater(danger, 0.6)
        
        # Verify checkpoint triggers
        self.assertTrue(self._check_health_triggers(20, 0.08))
        
        # Verify state transition restrictions
        self.manager.current_state = GameState.EXPLORATION
        self.assertFalse(self.manager.change_state(GameState.BATTLE))

    def test_faction_reputation_thresholds(self):
        """Test faction reputation threshold effects."""
        self.manager.current_state = GameState.EXPLORATION
        self.manager.current_location = Location.NEXUS_CITY
        self.manager.world_state['NEXUS_CITY_controlling_faction'] = 'merchants_guild'
        
        # Test reputation thresholds
        reputation_thresholds = [-75, -50, -25, 0, 25, 50, 75]
        expected_states = {
            GameState.TOWN: -50,
            GameState.SHOP: 0,
            GameState.QUEST_LOG: -25
        }
        
        for rep in reputation_thresholds:
            self.manager.faction_standings['merchants_guild'] = rep
            for state, threshold in expected_states.items():
                if rep > threshold:
                    self.assertTrue(self.manager.change_state(state),
                                  f"Should allow {state} at reputation {rep}")
                else:
                    self.assertFalse(self.manager.change_state(state),
                                   f"Should deny {state} at reputation {rep}")

    def test_time_based_state_restrictions(self):
        """Test comprehensive time-based state restrictions."""
        self.manager.current_state = GameState.TOWN
        
        # Test 24-hour cycle
        for hour in range(24):
            self.manager.environmental_conditions.time_of_day = hour
            
            # Shop access
            can_access_shop = 6 <= hour <= 20
            self.assertEqual(self.manager.change_state(GameState.SHOP), can_access_shop,
                           f"Shop access incorrect at hour {hour}")
            
            # Night exploration
            self.manager.current_state = GameState.TOWN
            if 22 <= hour or hour <= 4:
                self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
                self.manager.player_data['night_vision'] = True
                self.assertTrue(self.manager.change_state(GameState.EXPLORATION))
                self.manager.player_data['night_vision'] = False
            else:
                self.assertTrue(self.manager.change_state(GameState.EXPLORATION))

    def test_combat_state_edge_cases(self):
        """Test edge cases in combat state transitions."""
        self.manager.current_state = GameState.BATTLE
        self.manager.world_state.update({
            'in_combat': True,
            'boss_battle': True,
            'elite_enemies': True,
            'surrounded': True,
            'low_health': True
        })
        
        # Test inventory access under extreme conditions
        self.assertFalse(self.manager.change_state(GameState.INVENTORY))
        
        # Test escape conditions
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        # Test gradual condition improvement
        self.manager.world_state['surrounded'] = False
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        self.manager.world_state['boss_battle'] = False
        self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
        
        self.manager.world_state['in_combat'] = False
        self.assertTrue(self.manager.change_state(GameState.EXPLORATION))

    def test_checkpoint_priority_ordering(self):
        """Test checkpoint trigger priority and ordering."""
        # Setup multiple triggers with different priorities
        self.manager.world_state.update({
            'boss_defeated': True,  # High priority
            'weather_changed': True,  # Medium priority
            'map_updated': True  # Low priority
        })
        
        # Track checkpoint creation count
        original_create_checkpoint = self.manager.create_checkpoint
        checkpoint_count = 0
        
        def count_checkpoints(*args, **kwargs):
            nonlocal checkpoint_count
            checkpoint_count += 1
            return original_create_checkpoint(*args, **kwargs)
        
        self.manager.create_checkpoint = count_checkpoints
        
        # Trigger checkpoint check
        self._check_auto_checkpoint()
        
        # Verify only one checkpoint was created despite multiple triggers
        self.assertEqual(checkpoint_count, 1)
        
        # Restore original method
        self.manager.create_checkpoint = original_create_checkpoint

    def test_environmental_condition_combinations(self):
        """Test combinations of environmental conditions."""
        test_conditions = [
            {'weather_type': 'storm', 'visibility': 0.3, 'wind_speed': 25},
            {'weather_type': 'blizzard', 'temperature': -15, 'visibility': 0.2},
            {'weather_type': 'clear', 'temperature': 40, 'wind_speed': 35},
            {'weather_type': 'sandstorm', 'visibility': 0.1, 'wind_speed': 30}
        ]
        
        self.manager.current_state = GameState.TOWN
        for conditions in test_conditions:
            # Update environmental conditions
            for key, value in conditions.items():
                setattr(self.manager.environmental_conditions, key, value)
            
            # Test exploration permission
            self.assertFalse(self.manager.change_state(GameState.EXPLORATION))
            
            # Test with appropriate gear
            if conditions['weather_type'] == 'storm':
                self.manager.player_data['storm_gear'] = True
                self.assertTrue(self.manager.change_state(GameState.EXPLORATION))
                self.manager.player_data['storm_gear'] = False
            elif conditions['weather_type'] == 'blizzard':
                self.manager.player_data['cold_resistance'] = 75
                self.assertTrue(self.manager.change_state(GameState.EXPLORATION))
                self.manager.player_data['cold_resistance'] = 0

    def _check_time_based_triggers(self) -> bool:
        """Helper method to check time-based triggers."""
        return self.manager._check_time_based_triggers(time.time(), self.manager._calculate_danger_level())

    def _check_location_triggers(self) -> bool:
        """Helper method to check location triggers."""
        return self.manager._check_location_triggers()

    def _check_combat_triggers(self, combat_intensity: float) -> bool:
        """Helper method to check combat triggers."""
        return self.manager._check_combat_triggers(combat_intensity)

    def _check_health_triggers(self, health_percentage: float, resource_status: float) -> bool:
        """Helper method to check health triggers."""
        return self.manager._check_health_triggers(health_percentage, resource_status)

    def _check_progression_triggers(self) -> bool:
        """Helper method to check progression triggers."""
        return self.manager._check_progression_triggers()

    def _check_special_event_triggers(self) -> bool:
        """Helper method to check special event triggers."""
        return self.manager._check_special_event_triggers()

    def _check_auto_checkpoint(self):
        """Helper method to trigger auto checkpoint check."""
        self.manager._check_auto_checkpoint()

if __name__ == '__main__':
    unittest.main() 