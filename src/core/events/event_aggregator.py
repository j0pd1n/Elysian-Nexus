from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set, DefaultDict, Callable, Union, Pattern
import statistics
from enum import Enum
import re

from .event_types import (
    GameEvent, EventCategory, CombatEvent, QuestEvent,
    WorldEvent, FactionEvent, InventoryEvent, CharacterEvent,
    DimensionalEvent
)
from ...combat_system.dimensional_combat import DimensionalLayer, DimensionalEffect

class PatternType(Enum):
    """Types of patterns that can be detected."""
    SEQUENCE = "sequence"  # Exact sequence of events
    CONCURRENT = "concurrent"  # Events occurring within time window
    CONDITIONAL = "conditional"  # Events meeting specific conditions
    REPETITIVE = "repetitive"  # Repeated sequences
    COMPOSITE = "composite"  # Combination of other patterns

class PatternCondition:
    """Represents a condition for pattern matching."""
    def __init__(self, 
                 event_type: type,
                 predicate: Callable[[GameEvent], bool],
                 description: str):
        self.event_type = event_type
        self.predicate = predicate
        self.description = description

class EventPattern:
    """Represents a pattern of events with enhanced matching capabilities."""
    def __init__(self, 
                 name: str,
                 pattern_type: PatternType,
                 window: timedelta,
                 conditions: Optional[List[PatternCondition]] = None,
                 min_occurrences: int = 1,
                 max_occurrences: Optional[int] = None,
                 cooldown: Optional[timedelta] = None):
        self.name = name
        self.pattern_type = pattern_type
        self.window = window
        self.conditions = conditions or []
        self.min_occurrences = min_occurrences
        self.max_occurrences = max_occurrences
        self.cooldown = cooldown
        self.last_match: Optional[datetime] = None
        self.match_count: int = 0
        self.current_sequence: List[GameEvent] = []
        self.matched_sequences: List[List[GameEvent]] = []

class PatternMatcher:
    """Handles pattern matching with different strategies."""
    
    @staticmethod
    def match_sequence(events: List[GameEvent], 
                      pattern: EventPattern) -> bool:
        """Match exact sequence of events."""
        if len(events) < len(pattern.conditions):
            return False
            
        for i in range(len(events) - len(pattern.conditions) + 1):
            if all(isinstance(events[i+j], cond.event_type) and 
                   cond.predicate(events[i+j])
                   for j, cond in enumerate(pattern.conditions)):
                return True
        return False

    @staticmethod
    def match_concurrent(events: List[GameEvent], 
                        pattern: EventPattern) -> bool:
        """Match events occurring within time window regardless of order."""
        matched_conditions = set()
        
        for event in events:
            for i, condition in enumerate(pattern.conditions):
                if (i not in matched_conditions and
                    isinstance(event, condition.event_type) and
                    condition.predicate(event)):
                    matched_conditions.add(i)
                    
        return len(matched_conditions) == len(pattern.conditions)

    @staticmethod
    def match_repetitive(events: List[GameEvent], 
                        pattern: EventPattern) -> bool:
        """Match repeated sequences of events."""
        if not events:
            return False
            
        occurrence_count = 0
        current_pos = 0
        
        while current_pos <= len(events) - len(pattern.conditions):
            if all(isinstance(events[current_pos+j], cond.event_type) and 
                   cond.predicate(events[current_pos+j])
                   for j, cond in enumerate(pattern.conditions)):
                occurrence_count += 1
                current_pos += len(pattern.conditions)
            else:
                current_pos += 1
                
        return (occurrence_count >= pattern.min_occurrences and
                (pattern.max_occurrences is None or 
                 occurrence_count <= pattern.max_occurrences))

class EventAggregator:
    """Aggregates and analyzes event patterns."""

    def __init__(self, window_size: timedelta = timedelta(minutes=5)):
        self.window_size = window_size
        self._combat_stats: Dict[str, List[float]] = defaultdict(list)
        self._quest_stats: Dict[str, int] = defaultdict(int)
        self._event_counts: Dict[EventCategory, int] = defaultdict(int)
        self._last_aggregation = datetime.now()
        
        # Enhanced tracking
        self._event_sequence: deque = deque(maxlen=1000)
        self._patterns: Dict[str, EventPattern] = {}
        self._location_stats: DefaultDict[str, int] = defaultdict(int)
        self._faction_influence: DefaultDict[str, float] = defaultdict(float)
        self._item_frequency: DefaultDict[str, int] = defaultdict(int)
        self._skill_usage: DefaultDict[str, int] = defaultdict(int)
        self._combat_combos: DefaultDict[tuple, int] = defaultdict(int)
        self._player_achievements: Set[str] = set()
        
        # Enhanced pattern tracking
        self._pattern_matches: DefaultDict[str, List[datetime]] = defaultdict(list)
        self._composite_patterns: Dict[str, List[str]] = {}

        self._dimensional_stats: DefaultDict[DimensionalLayer, Dict[str, float]] = defaultdict(
            lambda: {'stability': 1.0, 'distortion': 0.0, 'effect_count': 0}
        )
        self._dimensional_transitions: DefaultDict[Tuple[DimensionalLayer, DimensionalLayer], int] = defaultdict(int)

    def process_event(self, event: GameEvent) -> None:
        """Process an event for aggregation."""
        self._event_counts[event.category] += 1
        self._event_sequence.append((datetime.now(), event))

        # Process by event type
        if isinstance(event, CombatEvent):
            self._process_combat_event(event)
        elif isinstance(event, QuestEvent):
            self._process_quest_event(event)
        elif isinstance(event, WorldEvent):
            self._process_world_event(event)
        elif isinstance(event, FactionEvent):
            self._process_faction_event(event)
        elif isinstance(event, InventoryEvent):
            self._process_inventory_event(event)
        elif isinstance(event, CharacterEvent):
            self._process_character_event(event)
        elif isinstance(event, DimensionalEvent):
            self._process_dimensional_event(event)
        elif isinstance(event, CombatEvent) and event.source_dimension:
            self._process_dimensional_combat(event)

        self._check_patterns()
        
        # Clear old data if needed
        if datetime.now() - self._last_aggregation > self.window_size:
            self._clear_old_data()

    def _process_combat_event(self, event: CombatEvent) -> None:
        """Process combat event statistics."""
        self._combat_stats['damage_dealt'].append(event.damage_dealt)
        self._combat_stats['damage_received'].append(event.damage_received)
        self._combat_stats['critical_hits'].append(1.0 if event.critical_hit else 0.0)
        
        # Track combat combinations
        if len(self._event_sequence) >= 2:
            prev_event = self._event_sequence[-2][1]
            if isinstance(prev_event, CombatEvent):
                combo = (prev_event.combat_type, event.combat_type)
                self._combat_combos[combo] += 1

    def _process_world_event(self, event: WorldEvent) -> None:
        """Process world event statistics."""
        self._location_stats[event.location] += 1
        if event.permanent_change:
            self._player_achievements.add(f"changed_{event.location}")

    def _process_faction_event(self, event: FactionEvent) -> None:
        """Process faction event statistics."""
        self._faction_influence[event.faction_id] += event.reputation_change
        if event.territory_affected:
            self._location_stats[event.territory_affected] += 1

    def _process_inventory_event(self, event: InventoryEvent) -> None:
        """Process inventory event statistics."""
        self._item_frequency[event.item_id] += 1
        if event.item_rarity != "common":
            self._player_achievements.add(f"found_rare_{event.item_id}")

    def _process_character_event(self, event: CharacterEvent) -> None:
        """Process character event statistics."""
        for skill in event.skills_unlocked:
            self._skill_usage[skill] += 1
            self._player_achievements.add(f"unlocked_{skill}")

    def _process_dimensional_event(self, event: DimensionalEvent) -> None:
        """Process dimensional event statistics."""
        # Update stability metrics
        self._dimensional_stats[event.source_dimension]['stability'] += event.stability_change
        self._dimensional_stats[event.source_dimension]['distortion'] += event.distortion_level
        
        if event.effect_type:
            self._dimensional_stats[event.source_dimension]['effect_count'] += 1
        
        # Track dimensional transitions
        if event.target_dimension:
            transition = (event.source_dimension, event.target_dimension)
            self._dimensional_transitions[transition] += 1

    def _process_dimensional_combat(self, event: CombatEvent) -> None:
        """Process dimensional aspects of combat events."""
        if event.target_dimension:
            # Track cross-dimensional combat
            transition = (event.source_dimension, event.target_dimension)
            self._dimensional_transitions[transition] += 1
            
            # Update stability for both dimensions
            self._dimensional_stats[event.source_dimension]['stability'] += event.dimensional_stability_change
            self._dimensional_stats[event.target_dimension]['stability'] += event.dimensional_stability_change

    def register_pattern(self, pattern: EventPattern) -> None:
        """Register a pattern to track."""
        self._patterns[pattern.name] = pattern

    def register_composite_pattern(self, name: str, 
                                 sub_patterns: List[str],
                                 window: timedelta) -> None:
        """Register a composite pattern made up of other patterns."""
        self._composite_patterns[name] = sub_patterns
        self._patterns[name] = EventPattern(
            name=name,
            pattern_type=PatternType.COMPOSITE,
            window=window
        )

    def get_detected_patterns(self) -> Dict[str, int]:
        """Get all detected patterns and their frequencies."""
        return {name: pattern.match_count for name, pattern in self._patterns.items()}

    def get_combat_efficiency_metrics(self) -> Dict[str, float]:
        """Get detailed combat efficiency metrics."""
        stats = self.get_combat_statistics()
        
        metrics = {
            'damage_efficiency': stats.get('damage_dealt', {}).get('mean', 0.0) / 
                               max(stats.get('damage_received', {}).get('mean', 1.0), 1.0),
            'critical_rate': stats.get('critical_hits', {}).get('mean', 0.0),
            'survival_rating': 1.0 - min(stats.get('damage_received', {}).get('mean', 0.0) / 100.0, 1.0),
            'combo_efficiency': len(self._combat_combos) / max(sum(self._combat_combos.values()), 1)
        }
        
        # Calculate combat mastery score
        damage_consistency = 1.0 - (stats.get('damage_dealt', {}).get('std', 0.0) / 
                                  max(stats.get('damage_dealt', {}).get('mean', 1.0), 1.0))
        metrics['combat_mastery'] = (metrics['damage_efficiency'] * 0.4 +
                                   metrics['critical_rate'] * 0.2 +
                                   metrics['survival_rating'] * 0.2 +
                                   damage_consistency * 0.2)
        
        return metrics

    def get_progression_metrics(self) -> Dict[str, Any]:
        """Get player progression metrics."""
        return {
            'achievements': len(self._player_achievements),
            'locations_explored': len(self._location_stats),
            'skill_diversity': len(self._skill_usage),
            'faction_standings': self._faction_influence,
            'item_collection': len(self._item_frequency),
            'rare_items_found': sum(1 for item_id in self._item_frequency 
                                  if f"found_rare_{item_id}" in self._player_achievements)
        }

    def get_player_engagement_metrics(self) -> Dict[str, float]:
        """Get metrics related to player engagement."""
        total_events = len(self._event_sequence)
        if total_events == 0:
            return {}

        # Calculate time-based engagement
        event_times = [event_time for event_time, _ in self._event_sequence]
        if len(event_times) >= 2:
            avg_time_between_events = (max(event_times) - min(event_times)).total_seconds() / (len(event_times) - 1)
        else:
            avg_time_between_events = 0

        return {
            'actions_per_minute': total_events / (self.window_size.total_seconds() / 60),
            'avg_time_between_actions': avg_time_between_events,
            'activity_diversity': len(set(event.category for _, event in self._event_sequence)) / len(EventCategory),
            'combat_engagement': sum(isinstance(event, CombatEvent) for _, event in self._event_sequence) / total_events,
            'exploration_rate': len(self._location_stats) / total_events,
            'quest_engagement': self._quest_stats['total_quests'] / total_events
        }

    def get_trend_analysis(self, metric: str) -> Tuple[float, float, TrendDirection]:
        """Enhanced trend analysis with direction indication."""
        if metric not in self._combat_stats:
            return (0.0, 0.0, TrendDirection.STABLE)
            
        values = self._combat_stats[metric]
        if len(values) < 10:
            return (0.0, 0.0, TrendDirection.STABLE)
            
        # Calculate trends using linear regression
        x = list(range(len(values)))
        y = values
        
        # Simple linear regression
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        slope = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / \
               sum((xi - mean_x) ** 2 for xi in x)
        
        # Calculate volatility
        volatility = statistics.stdev(y) / mean_y if mean_y != 0 else 0
        
        # Determine trend direction
        if volatility > 0.5:
            direction = TrendDirection.VOLATILE
        elif abs(slope) < 0.1:
            direction = TrendDirection.STABLE
        elif slope > 0:
            direction = TrendDirection.INCREASING
        else:
            direction = TrendDirection.DECREASING
        
        return (slope, volatility, direction)

    def get_combat_combo_analysis(self) -> Dict[str, Any]:
        """Analyze combat combination patterns."""
        if not self._combat_combos:
            return {}

        total_combos = sum(self._combat_combos.values())
        return {
            'most_common_combo': max(self._combat_combos.items(), key=lambda x: x[1]),
            'combo_variety': len(self._combat_combos),
            'avg_combo_frequency': total_combos / len(self._combat_combos),
            'combo_distribution': {
                combo: count / total_combos
                for combo, count in self._combat_combos.items()
            }
        }

    def _check_patterns(self) -> None:
        """Check for registered pattern matches with enhanced detection."""
        current_time = datetime.now()
        recent_events = [
            event for time, event in self._event_sequence
            if current_time - time <= max(p.window for p in self._patterns.values())
        ]

        for name, pattern in self._patterns.items():
            # Skip if in cooldown
            if (pattern.cooldown and pattern.last_match and
                current_time - pattern.last_match <= pattern.cooldown):
                continue

            matched = False
            if pattern.pattern_type == PatternType.SEQUENCE:
                matched = PatternMatcher.match_sequence(recent_events, pattern)
            elif pattern.pattern_type == PatternType.CONCURRENT:
                matched = PatternMatcher.match_concurrent(recent_events, pattern)
            elif pattern.pattern_type == PatternType.REPETITIVE:
                matched = PatternMatcher.match_repetitive(recent_events, pattern)
            elif pattern.pattern_type == PatternType.COMPOSITE:
                # Check if all sub-patterns have matched within the window
                sub_patterns = self._composite_patterns[pattern.name]
                matched = all(
                    any(match_time >= current_time - pattern.window
                        for match_time in self._pattern_matches[sub_pattern])
                    for sub_pattern in sub_patterns
                )

            if matched:
                pattern.match_count += 1
                pattern.last_match = current_time
                self._pattern_matches[pattern.name].append(current_time)
                # Keep only recent matches
                self._pattern_matches[pattern.name] = [
                    t for t in self._pattern_matches[pattern.name]
                    if current_time - t <= pattern.window
                ]

    def get_pattern_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed statistics about pattern matches."""
        stats = {}
        current_time = datetime.now()
        
        for name, pattern in self._patterns.items():
            recent_matches = [
                t for t in self._pattern_matches[name]
                if current_time - t <= pattern.window
            ]
            
            if not recent_matches:
                continue
                
            match_intervals = [
                (t2 - t1).total_seconds()
                for t1, t2 in zip(recent_matches[:-1], recent_matches[1:])
            ]
            
            stats[name] = {
                'total_matches': pattern.match_count,
                'recent_matches': len(recent_matches),
                'last_match': pattern.last_match,
                'avg_interval': statistics.mean(match_intervals) if match_intervals else None,
                'pattern_type': pattern.pattern_type.value
            }
            
            if pattern.pattern_type == PatternType.COMPOSITE:
                stats[name]['sub_patterns'] = self._composite_patterns[name]
                
        return stats

    def create_combat_patterns(self) -> None:
        """Create predefined combat patterns."""
        # Basic combo pattern
        self.register_pattern(EventPattern(
            name="basic_combo",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(seconds=5),
            conditions=[
                PatternCondition(
                    CombatEvent,
                    lambda e: e.combat_type == "slash",
                    "Slash attack"
                ),
                PatternCondition(
                    CombatEvent,
                    lambda e: e.combat_type == "thrust",
                    "Thrust attack"
                )
            ]
        ))

        # Critical chain pattern
        self.register_pattern(EventPattern(
            name="critical_chain",
            pattern_type=PatternType.REPETITIVE,
            window=timedelta(seconds=10),
            conditions=[
                PatternCondition(
                    CombatEvent,
                    lambda e: e.critical_hit,
                    "Critical hit"
                )
            ],
            min_occurrences=3
        ))

        # Combat mastery pattern
        self.register_composite_pattern(
            name="combat_mastery",
            sub_patterns=["basic_combo", "critical_chain"],
            window=timedelta(seconds=15)
        )

    def create_progression_patterns(self) -> None:
        """Create predefined progression patterns."""
        # Skill advancement pattern
        self.register_pattern(EventPattern(
            name="skill_advancement",
            pattern_type=PatternType.CONCURRENT,
            window=timedelta(minutes=5),
            conditions=[
                PatternCondition(
                    CharacterEvent,
                    lambda e: len(e.skills_unlocked) > 0,
                    "Skill unlock"
                ),
                PatternCondition(
                    CombatEvent,
                    lambda e: e.damage_dealt > 100,
                    "High damage"
                )
            ]
        ))

        # Explorer pattern
        self.register_pattern(EventPattern(
            name="explorer",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(minutes=10),
            conditions=[
                PatternCondition(
                    WorldEvent,
                    lambda e: e.event_type == "discovery",
                    "Area discovery"
                ),
                PatternCondition(
                    QuestEvent,
                    lambda e: e.quest_status == "complete",
                    "Quest completion"
                )
            ],
            cooldown=timedelta(minutes=30)
        ))

    def _clear_old_data(self) -> None:
        """Clear old data to free up memory."""
        self._combat_stats = defaultdict(list)
        self._quest_stats = defaultdict(int)
        self._event_counts = defaultdict(int)
        self._event_sequence.clear()
        self._patterns.clear()
        self._location_stats.clear()
        self._faction_influence.clear()
        self._item_frequency.clear()
        self._skill_usage.clear()
        self._combat_combos.clear()
        self._player_achievements.clear()
        self._pattern_matches.clear()
        self._composite_patterns.clear()

    def _last_aggregation(self) -> datetime:
        """Get the last aggregation time."""
        return self._last_aggregation

    def _window_size(self) -> timedelta:
        """Get the window size."""
        return self.window_size

    def _combat_stats(self) -> Dict[str, List[float]]:
        """Get combat statistics."""
        return self._combat_stats

    def _quest_stats(self) -> Dict[str, int]:
        """Get quest statistics."""
        return self._quest_stats

    def _event_counts(self) -> Dict[EventCategory, int]:
        """Get event counts."""
        return self._event_counts

    def _event_sequence(self) -> deque:
        """Get the event sequence."""
        return self._event_sequence

    def _patterns(self) -> Dict[str, EventPattern]:
        """Get the patterns."""
        return self._patterns

    def _location_stats(self) -> DefaultDict[str, int]:
        """Get the location statistics."""
        return self._location_stats

    def _faction_influence(self) -> DefaultDict[str, float]:
        """Get the faction influence."""
        return self._faction_influence

    def _item_frequency(self) -> DefaultDict[str, int]:
        """Get the item frequency."""
        return self._item_frequency

    def _skill_usage(self) -> DefaultDict[str, int]:
        """Get the skill usage."""
        return self._skill_usage

    def _combat_combos(self) -> DefaultDict[tuple, int]:
        """Get the combat combos."""
        return self._combat_combos

    def _player_achievements(self) -> Set[str]:
        """Get the player achievements."""
        return self._player_achievements

    def _pattern_matches(self) -> DefaultDict[str, List[datetime]]:
        """Get the pattern matches."""
        return self._pattern_matches

    def _composite_patterns(self) -> Dict[str, List[str]]:
        """Get the composite patterns."""
        return self._composite_patterns 

    def create_faction_patterns(self) -> None:
        """Create patterns for faction-related mechanics."""
        # Faction influence pattern
        self.register_pattern(EventPattern(
            name="faction_influence",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(minutes=15),
            conditions=[
                PatternCondition(
                    FactionEvent,
                    lambda e: e.reputation_change > 0,
                    "Reputation gain"
                ),
                PatternCondition(
                    WorldEvent,
                    lambda e: e.event_type == "interaction",
                    "Faction interaction"
                ),
                PatternCondition(
                    FactionEvent,
                    lambda e: e.territory_affected is not None,
                    "Territory influence"
                )
            ]
        ))

        # Territory control pattern
        self.register_pattern(EventPattern(
            name="territory_control",
            pattern_type=PatternType.CONCURRENT,
            window=timedelta(minutes=30),
            conditions=[
                PatternCondition(
                    FactionEvent,
                    lambda e: abs(e.reputation_change) >= 50,
                    "Major reputation change"
                ),
                PatternCondition(
                    WorldEvent,
                    lambda e: e.permanent_change,
                    "Permanent world change"
                )
            ],
            cooldown=timedelta(hours=1)
        ))

    def create_crafting_patterns(self) -> None:
        """Create patterns for crafting and resource management."""
        # Resource gathering chain
        self.register_pattern(EventPattern(
            name="resource_chain",
            pattern_type=PatternType.REPETITIVE,
            window=timedelta(minutes=5),
            conditions=[
                PatternCondition(
                    InventoryEvent,
                    lambda e: e.action == "add" and e.item_rarity != "common",
                    "Rare resource gathering"
                )
            ],
            min_occurrences=3,
            cooldown=timedelta(minutes=10)
        ))

        # Crafting mastery
        self.register_pattern(EventPattern(
            name="crafting_mastery",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(minutes=10),
            conditions=[
                PatternCondition(
                    InventoryEvent,
                    lambda e: e.action == "use",
                    "Resource use"
                ),
                PatternCondition(
                    InventoryEvent,
                    lambda e: e.action == "add" and e.item_rarity == "rare",
                    "Rare item creation"
                ),
                PatternCondition(
                    CharacterEvent,
                    lambda e: any("craft" in skill.lower() for skill in e.skills_unlocked),
                    "Crafting skill gain"
                )
            ]
        ))

    def create_quest_patterns(self) -> None:
        """Create patterns for quest and story progression."""
        # Quest chain completion
        self.register_pattern(EventPattern(
            name="quest_chain",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(hours=1),
            conditions=[
                PatternCondition(
                    QuestEvent,
                    lambda e: e.quest_status == "complete",
                    "Quest completion"
                ),
                PatternCondition(
                    WorldEvent,
                    lambda e: e.event_type == "change",
                    "World state change"
                ),
                PatternCondition(
                    QuestEvent,
                    lambda e: e.quest_status == "complete" and len(e.rewards) > 2,
                    "Major quest completion"
                )
            ]
        ))

        # Story milestone
        self.register_pattern(EventPattern(
            name="story_milestone",
            pattern_type=PatternType.CONCURRENT,
            window=timedelta(minutes=30),
            conditions=[
                PatternCondition(
                    QuestEvent,
                    lambda e: e.quest_status == "complete",
                    "Quest completion"
                ),
                PatternCondition(
                    WorldEvent,
                    lambda e: e.permanent_change,
                    "Permanent world change"
                ),
                PatternCondition(
                    FactionEvent,
                    lambda e: abs(e.reputation_change) >= 100,
                    "Major faction change"
                )
            ],
            cooldown=timedelta(hours=2)
        ))

    def validate_pattern(self, pattern: EventPattern) -> List[str]:
        """Validate a pattern configuration and return any issues."""
        issues = []
        
        # Basic validation
        if not pattern.name:
            issues.append("Pattern name is required")
        if not pattern.conditions:
            issues.append("Pattern must have at least one condition")
        
        # Type-specific validation
        if pattern.pattern_type == PatternType.REPETITIVE:
            if pattern.min_occurrences < 1:
                issues.append("Minimum occurrences must be at least 1")
            if pattern.max_occurrences and pattern.max_occurrences < pattern.min_occurrences:
                issues.append("Maximum occurrences must be greater than minimum")
        
        # Window validation
        if pattern.window.total_seconds() <= 0:
            issues.append("Pattern window must be positive")
        if pattern.cooldown and pattern.cooldown.total_seconds() <= 0:
            issues.append("Pattern cooldown must be positive")
        
        # Condition validation
        for i, condition in enumerate(pattern.conditions):
            if not condition.predicate:
                issues.append(f"Condition {i} missing predicate")
            if not condition.description:
                issues.append(f"Condition {i} missing description")
        
        return issues

    def get_pattern_debug_info(self, pattern_name: str) -> Dict[str, Any]:
        """Get detailed debug information for a pattern."""
        pattern = self._patterns.get(pattern_name)
        if not pattern:
            return {"error": "Pattern not found"}
            
        current_time = datetime.now()
        recent_matches = [
            t for t in self._pattern_matches[pattern_name]
            if current_time - t <= pattern.window
        ]
        
        debug_info = {
            'pattern_config': {
                'type': pattern.pattern_type.value,
                'window': pattern.window.total_seconds(),
                'conditions': [c.description for c in pattern.conditions],
                'min_occurrences': pattern.min_occurrences,
                'max_occurrences': pattern.max_occurrences,
                'cooldown': pattern.cooldown.total_seconds() if pattern.cooldown else None
            },
            'matching_stats': {
                'total_matches': pattern.match_count,
                'recent_matches': len(recent_matches),
                'last_match_age': (current_time - pattern.last_match).total_seconds() if pattern.last_match else None,
                'in_cooldown': bool(pattern.cooldown and pattern.last_match and 
                                  current_time - pattern.last_match <= pattern.cooldown)
            },
            'current_sequence': [
                {
                    'timestamp': current_time - timedelta(seconds=i),
                    'event_type': type(event).__name__,
                    'matched_conditions': [
                        c.description for c in pattern.conditions
                        if isinstance(event, c.event_type) and c.predicate(event)
                    ]
                }
                for i, event in enumerate(pattern.current_sequence)
            ]
        }
        
        if pattern.pattern_type == PatternType.COMPOSITE:
            debug_info['sub_patterns'] = {
                sub: self.get_pattern_debug_info(sub)
                for sub in self._composite_patterns[pattern_name]
            }
            
        return debug_info

    def get_enhanced_pattern_analytics(self) -> Dict[str, Any]:
        """Get enhanced analytics about pattern matching."""
        current_time = datetime.now()
        analytics = {
            'pattern_success_rates': {},
            'pattern_correlations': {},
            'pattern_sequences': {},
            'time_based_analysis': {}
        }
        
        # Calculate success rates
        for name, pattern in self._patterns.items():
            recent_matches = [
                t for t in self._pattern_matches[name]
                if current_time - t <= pattern.window
            ]
            total_attempts = len(pattern.current_sequence)
            success_rate = len(recent_matches) / max(total_attempts, 1)
            analytics['pattern_success_rates'][name] = {
                'success_rate': success_rate,
                'attempts': total_attempts,
                'matches': len(recent_matches)
            }
        
        # Find pattern correlations
        pattern_times = {
            name: set(t.timestamp() for t in matches)
            for name, matches in self._pattern_matches.items()
        }
        for p1 in self._patterns:
            for p2 in self._patterns:
                if p1 < p2:  # Avoid duplicate combinations
                    times1 = pattern_times[p1]
                    times2 = pattern_times[p2]
                    if times1 and times2:
                        correlation = len(times1.intersection(times2)) / len(times1.union(times2))
                        analytics['pattern_correlations'][f"{p1}-{p2}"] = correlation
        
        # Analyze pattern sequences
        for name, pattern in self._patterns.items():
            if pattern.matched_sequences:
                analytics['pattern_sequences'][name] = {
                    'avg_sequence_length': statistics.mean(len(seq) for seq in pattern.matched_sequences),
                    'most_common_first_event': max(
                        (type(seq[0]).__name__ for seq in pattern.matched_sequences),
                        key=lambda x: sum(1 for seq in pattern.matched_sequences if type(seq[0]).__name__ == x)
                    )
                }
        
        # Time-based analysis
        hour_distribution = defaultdict(int)
        for matches in self._pattern_matches.values():
            for match_time in matches:
                hour_distribution[match_time.hour] += 1
        
        analytics['time_based_analysis'] = {
            'hour_distribution': dict(hour_distribution),
            'peak_hour': max(hour_distribution.items(), key=lambda x: x[1])[0] if hour_distribution else None,
            'active_hours': len([h for h, c in hour_distribution.items() if c > 0])
        }
        
        return analytics 

    def create_stealth_patterns(self) -> None:
        """Create patterns for stealth and infiltration mechanics."""
        # Stealth chain
        self.register_pattern(EventPattern(
            name="stealth_chain",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(minutes=5),
            conditions=[
                PatternCondition(
                    CharacterEvent,
                    lambda e: "sneak" in str(e.action_type).lower(),
                    "Enter stealth"
                ),
                PatternCondition(
                    CombatEvent,
                    lambda e: e.is_sneak_attack and e.critical_hit,
                    "Sneak attack critical"
                ),
                PatternCondition(
                    CharacterEvent,
                    lambda e: "hide" in str(e.action_type).lower(),
                    "Return to stealth"
                )
            ]
        ))

        # Shadow master
        self.register_pattern(EventPattern(
            name="shadow_master",
            pattern_type=PatternType.CONCURRENT,
            window=timedelta(minutes=10),
            conditions=[
                PatternCondition(
                    CombatEvent,
                    lambda e: e.is_sneak_attack and e.damage_dealt > 200,
                    "High damage stealth attack"
                ),
                PatternCondition(
                    WorldEvent,
                    lambda e: e.event_type == "detection_avoided",
                    "Detection avoided"
                )
            ],
            cooldown=timedelta(minutes=15)
        ))

    def create_trading_patterns(self) -> None:
        """Create patterns for trading and economy mechanics."""
        # Market manipulator
        self.register_pattern(EventPattern(
            name="market_manipulator",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(minutes=30),
            conditions=[
                PatternCondition(
                    InventoryEvent,
                    lambda e: e.action == "buy" and e.quantity >= 10,
                    "Bulk purchase"
                ),
                PatternCondition(
                    WorldEvent,
                    lambda e: e.event_type == "market_change",
                    "Market price change"
                ),
                PatternCondition(
                    InventoryEvent,
                    lambda e: e.action == "sell" and e.profit_margin > 0.5,
                    "Profitable sale"
                )
            ]
        ))

        # Trade network
        self.register_pattern(EventPattern(
            name="trade_network",
            pattern_type=PatternType.CONCURRENT,
            window=timedelta(hours=1),
            conditions=[
                PatternCondition(
                    InventoryEvent,
                    lambda e: e.action in ["buy", "sell"] and e.total_value > 1000,
                    "High value transaction"
                ),
                PatternCondition(
                    FactionEvent,
                    lambda e: e.reputation_change > 0 and "merchant" in str(e.faction_type).lower(),
                    "Merchant reputation gain"
                )
            ]
        ))

    def create_environmental_patterns(self) -> None:
        """Create patterns for environmental interaction mechanics."""
        # Weather master
        self.register_pattern(EventPattern(
            name="weather_master",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(minutes=15),
            conditions=[
                PatternCondition(
                    WorldEvent,
                    lambda e: "weather" in str(e.event_type).lower(),
                    "Weather change"
                ),
                PatternCondition(
                    CombatEvent,
                    lambda e: e.environmental_bonus > 0,
                    "Weather combat bonus"
                ),
                PatternCondition(
                    CharacterEvent,
                    lambda e: any("weather" in skill.lower() for skill in e.skills_used),
                    "Weather skill use"
                )
            ]
        ))

        # Nature's ally
        self.register_pattern(EventPattern(
            name="natures_ally",
            pattern_type=PatternType.CONCURRENT,
            window=timedelta(minutes=20),
            conditions=[
                PatternCondition(
                    WorldEvent,
                    lambda e: e.event_type == "environmental_interaction",
                    "Environmental interaction"
                ),
                PatternCondition(
                    CharacterEvent,
                    lambda e: any("nature" in skill.lower() for skill in e.skills_unlocked),
                    "Nature skill gain"
                )
            ],
            cooldown=timedelta(minutes=30)
        ))

    def get_advanced_analytics(self) -> Dict[str, Any]:
        """Get advanced analytics with detailed metrics."""
        analytics = self.get_enhanced_pattern_analytics()
        current_time = datetime.now()

        # Pattern chain analysis
        chain_analytics = {}
        for name, pattern in self._patterns.items():
            if pattern.matched_sequences:
                chain_lengths = [len(seq) for seq in pattern.matched_sequences]
                chain_analytics[name] = {
                    'max_chain': max(chain_lengths),
                    'avg_chain': statistics.mean(chain_lengths),
                    'chain_consistency': 1 - (statistics.stdev(chain_lengths) / statistics.mean(chain_lengths)) 
                        if len(chain_lengths) > 1 else 1.0
                }

        # Time-based performance metrics
        hourly_performance = defaultdict(lambda: defaultdict(list))
        for name, matches in self._pattern_matches.items():
            for match_time in matches:
                hour = match_time.hour
                hourly_performance[name]['matches_by_hour'][hour] = \
                    hourly_performance[name]['matches_by_hour'].get(hour, 0) + 1

        # Pattern synergy analysis
        synergy_scores = {}
        for p1 in self._patterns:
            for p2 in self._patterns:
                if p1 < p2:
                    p1_times = set(t.timestamp() for t in self._pattern_matches[p1])
                    p2_times = set(t.timestamp() for t in self._pattern_matches[p2])
                    if p1_times and p2_times:
                        time_diff = min(abs(t1 - t2) for t1 in p1_times for t2 in p2_times)
                        synergy_scores[f"{p1}-{p2}"] = 1.0 / (1.0 + time_diff)

        # Skill progression metrics
        skill_metrics = {}
        for skill, usage in self._skill_usage.items():
            related_patterns = [
                name for name, pattern in self._patterns.items()
                if any(skill.lower() in str(c.description).lower() for c in pattern.conditions)
            ]
            skill_metrics[skill] = {
                'usage_frequency': usage,
                'related_patterns': related_patterns,
                'pattern_success_rate': statistics.mean([
                    analytics['pattern_success_rates'][pattern]['success_rate']
                    for pattern in related_patterns
                    if pattern in analytics['pattern_success_rates']
                ]) if related_patterns else 0.0
            }

        return {
            'chain_analytics': chain_analytics,
            'hourly_performance': dict(hourly_performance),
            'pattern_synergy': synergy_scores,
            'skill_metrics': skill_metrics,
            'base_analytics': analytics
        }

    def get_visualization_data(self) -> Dict[str, Any]:
        """Get data formatted for visualization."""
        analytics = self.get_advanced_analytics()
        
        visualization_data = {
            'time_series': {
                'pattern_matches': {
                    name: [
                        {'timestamp': t.isoformat(), 'value': 1}
                        for t in matches
                    ]
                    for name, matches in self._pattern_matches.items()
                },
                'hourly_activity': analytics['hourly_performance']
            },
            'relationships': {
                'pattern_synergy': [
                    {
                        'source': p1,
                        'target': p2,
                        'weight': score
                    }
                    for (p1, p2), score in analytics['pattern_synergy'].items()
                ],
                'skill_patterns': [
                    {
                        'skill': skill,
                        'patterns': data['related_patterns'],
                        'success_rate': data['pattern_success_rate']
                    }
                    for skill, data in analytics['skill_metrics'].items()
                ]
            },
            'distributions': {
                'chain_lengths': {
                    name: data['chain_analytics']
                    for name, data in analytics['chain_analytics'].items()
                },
                'success_rates': analytics['base_analytics']['pattern_success_rates']
            },
            'metrics': {
                'skill_usage': {
                    skill: usage for skill, usage in self._skill_usage.items()
                },
                'pattern_completion': {
                    name: pattern.match_count
                    for name, pattern in self._patterns.items()
                }
            }
        }
        
        return visualization_data 

    def get_dimensional_metrics(self) -> Dict[str, Any]:
        """Get metrics related to dimensional activity."""
        metrics = {
            'dimension_stability': {
                dim.name: stats['stability'] 
                for dim, stats in self._dimensional_stats.items()
            },
            'dimension_distortion': {
                dim.name: stats['distortion']
                for dim, stats in self._dimensional_stats.items()
            },
            'dimensional_transitions': {
                f"{src.name}->{dst.name}": count
                for (src, dst), count in self._dimensional_transitions.items()
            },
            'most_active_dimension': max(
                self._dimensional_stats.items(),
                key=lambda x: x[1]['effect_count'],
                default=(None, {'effect_count': 0})
            )[0]
        }
        
        # Calculate dimensional stability trend
        for dim in DimensionalLayer:
            if dim in self._dimensional_stats:
                stats = self._dimensional_stats[dim]
                metrics[f'{dim.name}_trend'] = {
                    'stability_trend': self._calculate_trend(stats['stability']),
                    'distortion_trend': self._calculate_trend(stats['distortion'])
                }
        
        return metrics

    def create_dimensional_patterns(self) -> None:
        """Create patterns for tracking dimensional phenomena."""
        # Pattern for dimensional resonance cascade
        self.register_pattern(EventPattern(
            name="dimensional_resonance_cascade",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(minutes=1),
            conditions=[
                PatternCondition(
                    DimensionalEvent,
                    lambda e: (
                        e.effect_type == DimensionalEffect.RESONANCE and
                        e.stability_change > 0.2
                    ),
                    "High resonance effect"
                ),
                PatternCondition(
                    CombatEvent,
                    lambda e: e.dimensional_effects and
                             DimensionalEffect.RESONANCE in e.dimensional_effects,
                    "Combat with resonance"
                )
            ]
        ))
        
        # Pattern for dimensional instability
        self.register_pattern(EventPattern(
            name="dimensional_instability",
            pattern_type=PatternType.CONCURRENT,
            window=timedelta(minutes=5),
            conditions=[
                PatternCondition(
                    DimensionalEvent,
                    lambda e: e.stability_change < -0.3,
                    "Major stability decrease"
                ),
                PatternCondition(
                    DimensionalEvent,
                    lambda e: e.distortion_level > 0.5,
                    "High distortion"
                )
            ]
        ))
        
        # Pattern for dimensional mastery
        self.register_pattern(EventPattern(
            name="dimensional_mastery",
            pattern_type=PatternType.SEQUENCE,
            window=timedelta(minutes=10),
            conditions=[
                PatternCondition(
                    CombatEvent,
                    lambda e: (
                        e.source_dimension != e.target_dimension and
                        e.damage_dealt > 50
                    ),
                    "Powerful cross-dimensional attack"
                ),
                PatternCondition(
                    DimensionalEvent,
                    lambda e: e.effect_type == DimensionalEffect.PHASING,
                    "Dimensional phasing"
                ),
                PatternCondition(
                    CombatEvent,
                    lambda e: len(e.dimensional_effects) >= 2,
                    "Multiple dimensional effects"
                )
            ]
        )) 