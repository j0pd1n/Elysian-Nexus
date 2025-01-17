from typing import Dict, Any, List, Optional, Type
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3

@dataclass
class ValidationIssue:
    """Represents a validation issue found during state validation."""
    severity: ValidationSeverity
    field: str
    message: str
    value: Any
    expected_type: Optional[Type] = None
    constraints: Optional[Dict[str, Any]] = None

class StateValidator:
    """Handles comprehensive state validation for game states."""
    
    def __init__(self):
        self.validation_rules: Dict[str, Dict[str, Any]] = {
            "player_data": {
                "required_fields": [
                    "health", "max_health", "level", "experience",
                    "position", "inventory", "equipped_items", "skills"
                ],
                "field_types": {
                    "health": (float, int),
                    "max_health": (float, int),
                    "level": int,
                    "experience": (float, int),
                    "position": dict,
                    "inventory": dict,
                    "equipped_items": dict,
                    "skills": dict
                },
                "value_ranges": {
                    "health": (0, float('inf')),
                    "max_health": (1, float('inf')),
                    "level": (1, 100),
                    "experience": (0, float('inf'))
                }
            },
            "world_state": {
                "required_fields": [
                    "current_region", "time_of_day", "weather",
                    "active_events", "faction_standings"
                ],
                "field_types": {
                    "current_region": str,
                    "time_of_day": (float, int),
                    "weather": str,
                    "active_events": list,
                    "faction_standings": dict
                },
                "value_ranges": {
                    "time_of_day": (0, 24)
                }
            },
            "combat_state": {
                "required_fields": [
                    "in_combat", "enemies", "combat_round",
                    "initiative_order", "active_effects"
                ],
                "field_types": {
                    "in_combat": bool,
                    "enemies": list,
                    "combat_round": int,
                    "initiative_order": list,
                    "active_effects": list
                },
                "value_ranges": {
                    "combat_round": (0, float('inf'))
                }
            }
        }
        
    def validate_state(self, state_data: Dict[str, Any], state_type: str) -> List[ValidationIssue]:
        """Validate a state against defined rules."""
        issues = []
        
        if state_type not in self.validation_rules:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                field="state_type",
                message=f"Unknown state type: {state_type}",
                value=state_type
            ))
            return issues
            
        rules = self.validation_rules[state_type]
        
        # Check required fields
        issues.extend(self._validate_required_fields(state_data, rules))
        
        # Check field types
        issues.extend(self._validate_field_types(state_data, rules))
        
        # Check value ranges
        issues.extend(self._validate_value_ranges(state_data, rules))
        
        # Check state-specific rules
        issues.extend(self._validate_state_specific_rules(state_data, state_type))
        
        return issues
        
    def _validate_required_fields(self, state_data: Dict[str, Any], rules: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate presence of required fields."""
        issues = []
        
        for field in rules.get("required_fields", []):
            if field not in state_data:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field=field,
                    message=f"Missing required field: {field}",
                    value=None
                ))
                
        return issues
        
    def _validate_field_types(self, state_data: Dict[str, Any], rules: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate field types."""
        issues = []
        
        for field, expected_type in rules.get("field_types", {}).items():
            if field in state_data:
                value = state_data[field]
                if isinstance(expected_type, tuple):
                    if not any(isinstance(value, t) for t in expected_type):
                        issues.append(ValidationIssue(
                            severity=ValidationSeverity.ERROR,
                            field=field,
                            message=f"Invalid type for {field}. Expected one of {expected_type}, got {type(value)}",
                            value=value,
                            expected_type=expected_type
                        ))
                elif not isinstance(value, expected_type):
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        field=field,
                        message=f"Invalid type for {field}. Expected {expected_type}, got {type(value)}",
                        value=value,
                        expected_type=expected_type
                    ))
                    
        return issues
        
    def _validate_value_ranges(self, state_data: Dict[str, Any], rules: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate value ranges for numeric fields."""
        issues = []
        
        for field, (min_val, max_val) in rules.get("value_ranges", {}).items():
            if field in state_data:
                value = state_data[field]
                if isinstance(value, (int, float)):
                    if not min_val <= value <= max_val:
                        issues.append(ValidationIssue(
                            severity=ValidationSeverity.ERROR,
                            field=field,
                            message=f"Value out of range for {field}. Expected between {min_val} and {max_val}, got {value}",
                            value=value,
                            constraints={"min": min_val, "max": max_val}
                        ))
                        
        return issues
        
    def _validate_state_specific_rules(self, state_data: Dict[str, Any], state_type: str) -> List[ValidationIssue]:
        """Validate rules specific to certain state types."""
        issues = []
        
        if state_type == "combat_state":
            issues.extend(self._validate_combat_state(state_data))
        elif state_type == "player_data":
            issues.extend(self._validate_player_state(state_data))
        elif state_type == "world_state":
            issues.extend(self._validate_world_state(state_data))
            
        return issues
        
    def _validate_combat_state(self, state_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate combat-specific state rules."""
        issues = []
        
        if state_data.get("in_combat"):
            # Validate enemies list
            enemies = state_data.get("enemies", [])
            if not enemies:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="enemies",
                    message="In combat state but no enemies present",
                    value=enemies
                ))
                
            # Validate initiative order
            initiative_order = state_data.get("initiative_order", [])
            if len(initiative_order) != len(set(initiative_order)):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="initiative_order",
                    message="Duplicate entries in initiative order",
                    value=initiative_order
                ))
                
        return issues
        
    def _validate_player_state(self, state_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate player-specific state rules."""
        issues = []
        
        # Validate health values
        health = state_data.get("health", 0)
        max_health = state_data.get("max_health", 0)
        if health > max_health:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                field="health",
                message=f"Health ({health}) exceeds max_health ({max_health})",
                value=health,
                constraints={"max": max_health}
            ))
            
        # Validate equipped items
        equipped_items = state_data.get("equipped_items", {})
        inventory = state_data.get("inventory", {})
        for slot, item_id in equipped_items.items():
            if item_id not in inventory:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field=f"equipped_items.{slot}",
                    message=f"Equipped item {item_id} not found in inventory",
                    value=item_id
                ))
                
        return issues
        
    def _validate_world_state(self, state_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate world-specific state rules."""
        issues = []
        
        # Validate faction standings
        faction_standings = state_data.get("faction_standings", {})
        for faction, standing in faction_standings.items():
            if not isinstance(standing, (int, float)) or not -100 <= standing <= 100:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field=f"faction_standings.{faction}",
                    message=f"Invalid faction standing value: {standing}. Must be between -100 and 100",
                    value=standing,
                    constraints={"min": -100, "max": 100}
                ))
                
        # Validate active events
        active_events = state_data.get("active_events", [])
        seen_events = set()
        for event in active_events:
            if not isinstance(event, dict) or "id" not in event:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="active_events",
                    message="Invalid event format",
                    value=event
                ))
            elif event["id"] in seen_events:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="active_events",
                    message=f"Duplicate event ID: {event['id']}",
                    value=event
                ))
            seen_events.add(event["id"])
                
        return issues 