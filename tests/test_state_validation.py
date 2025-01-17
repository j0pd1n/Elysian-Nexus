import unittest
from src.core.state_validation.state_validator import StateValidator, ValidationSeverity, ValidationIssue
from src.core.game_state.game_state_manager import GameStateManager
from src.core.game_state.enums import GameState, GameMode, DifficultyLevel, Location, QuestStatus

class TestStateValidation(unittest.TestCase):
    def setUp(self):
        self.validator = StateValidator()
        self.game_state_manager = GameStateManager()

    def test_player_data_validation(self):
        # Test valid player data
        valid_player_data = {
            "health": 100,
            "max_health": 100,
            "level": 1,
            "experience": 0,
            "position": {"x": 0, "y": 0, "z": 0},
            "inventory": {},
            "equipped_items": {},
            "skills": {}
        }
        issues = self.validator.validate_state(valid_player_data, "player_data")
        self.assertEqual(len(issues), 0, "Valid player data should have no issues")

        # Test invalid health value
        invalid_health_data = valid_player_data.copy()
        invalid_health_data["health"] = -1
        issues = self.validator.validate_state(invalid_health_data, "player_data")
        self.assertTrue(any(issue.severity == ValidationSeverity.ERROR and 
                          issue.field == "health" for issue in issues))

        # Test missing required field
        missing_field_data = valid_player_data.copy()
        del missing_field_data["level"]
        issues = self.validator.validate_state(missing_field_data, "player_data")
        self.assertTrue(any(issue.severity == ValidationSeverity.ERROR and 
                          issue.field == "level" for issue in issues))

        # Test invalid type
        invalid_type_data = valid_player_data.copy()
        invalid_type_data["level"] = "1"  # Should be int
        issues = self.validator.validate_state(invalid_type_data, "player_data")
        self.assertTrue(any(issue.severity == ValidationSeverity.ERROR and 
                          issue.field == "level" for issue in issues))

    def test_world_state_validation(self):
        # Test valid world state
        valid_world_state = {
            "current_region": "starting_area",
            "time_of_day": 12,
            "weather": "clear",
            "active_events": [],
            "faction_standings": {}
        }
        issues = self.validator.validate_state(valid_world_state, "world_state")
        self.assertEqual(len(issues), 0, "Valid world state should have no issues")

        # Test invalid time of day
        invalid_time_state = valid_world_state.copy()
        invalid_time_state["time_of_day"] = 25  # Should be 0-24
        issues = self.validator.validate_state(invalid_time_state, "world_state")
        self.assertTrue(any(issue.severity == ValidationSeverity.ERROR and 
                          issue.field == "time_of_day" for issue in issues))

        # Test invalid faction standings
        invalid_faction_state = valid_world_state.copy()
        invalid_faction_state["faction_standings"] = {"faction1": 150}  # Should be -100 to 100
        issues = self.validator.validate_state(invalid_faction_state, "world_state")
        self.assertTrue(any(issue.severity == ValidationSeverity.ERROR and 
                          "faction_standings" in issue.field for issue in issues))

    def test_combat_state_validation(self):
        # Test valid combat state
        valid_combat_state = {
            "in_combat": True,
            "enemies": [{"id": "enemy1", "health": 100}],
            "combat_round": 1,
            "initiative_order": ["player", "enemy1"],
            "active_effects": []
        }
        issues = self.validator.validate_state(valid_combat_state, "combat_state")
        self.assertEqual(len(issues), 0, "Valid combat state should have no issues")

        # Test invalid combat state (no enemies while in combat)
        invalid_combat_state = valid_combat_state.copy()
        invalid_combat_state["enemies"] = []
        issues = self.validator.validate_state(invalid_combat_state, "combat_state")
        self.assertTrue(any(issue.severity == ValidationSeverity.WARNING and 
                          issue.field == "enemies" for issue in issues))

        # Test duplicate initiative order
        duplicate_initiative_state = valid_combat_state.copy()
        duplicate_initiative_state["initiative_order"] = ["player", "player"]
        issues = self.validator.validate_state(duplicate_initiative_state, "combat_state")
        self.assertTrue(any(issue.severity == ValidationSeverity.ERROR and 
                          issue.field == "initiative_order" for issue in issues))

    def test_game_state_manager_validation(self):
        # Test valid state transition
        self.game_state_manager.player_data = {
            "health": 100,
            "max_health": 100,
            "level": 1,
            "experience": 0,
            "position": {"x": 0, "y": 0, "z": 0},
            "inventory": {},
            "equipped_items": {},
            "skills": {}
        }
        self.game_state_manager.world_state = {
            "current_region": "starting_area",
            "time_of_day": 12,
            "weather": "clear",
            "active_events": [],
            "faction_standings": {}
        }
        
        # Test checkpoint creation with valid state
        checkpoint = self.game_state_manager.create_checkpoint()
        self.assertIsNotNone(checkpoint, "Should create checkpoint with valid state")

        # Test checkpoint creation with invalid state
        self.game_state_manager.player_data["health"] = -1
        checkpoint = self.game_state_manager.create_checkpoint()
        self.assertIsNone(checkpoint, "Should not create checkpoint with invalid state")

        # Test save game with invalid state
        success = self.game_state_manager.save_game(1)
        self.assertFalse(success, "Should not save game with invalid state")

        # Fix the state and test again
        self.game_state_manager.player_data["health"] = 100
        success = self.game_state_manager.save_game(1)
        self.assertTrue(success, "Should save game with valid state")

    def test_equipped_items_validation(self):
        # Test valid equipped items
        valid_player_data = {
            "health": 100,
            "max_health": 100,
            "level": 1,
            "experience": 0,
            "position": {"x": 0, "y": 0, "z": 0},
            "inventory": {"item1": {"id": "item1", "type": "weapon"}},
            "equipped_items": {"weapon": "item1"},
            "skills": {}
        }
        issues = self.validator.validate_state(valid_player_data, "player_data")
        self.assertEqual(len(issues), 0, "Valid equipped items should have no issues")

        # Test equipped item not in inventory
        invalid_equipped_data = valid_player_data.copy()
        invalid_equipped_data["equipped_items"] = {"weapon": "item2"}
        issues = self.validator.validate_state(invalid_equipped_data, "player_data")
        self.assertTrue(any(issue.severity == ValidationSeverity.ERROR and 
                          "equipped_items" in issue.field for issue in issues))

if __name__ == '__main__':
    unittest.main() 