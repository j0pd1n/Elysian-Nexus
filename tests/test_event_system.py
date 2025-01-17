import unittest
import time
from datetime import datetime, timedelta
from typing import List
import threading

from src.core.events.event_types import *
from src.core.events.event_dispatcher import EventDispatcher
from src.core.events.event_handlers import EventHandlers

class TestEventSystem(unittest.TestCase):
    def setUp(self):
        self.dispatcher = EventDispatcher()
        self.dispatcher.start()
        self.received_events: List[GameEvent] = []
        
    def tearDown(self):
        self.dispatcher.stop()

    def test_event_dispatch_and_handling(self):
        """Test basic event dispatch and handling."""
        # Create a test handler
        def test_handler(event: GameEvent):
            self.received_events.append(event)

        # Subscribe handler
        self.dispatcher.subscribe(test_handler, EventCategory.COMBAT, EventPriority.HIGH)

        # Create and dispatch event
        combat_event = CombatEvent(
            event_id="",  # Will be set by dispatcher
            timestamp=datetime.now(),
            category=EventCategory.COMBAT,
            priority=EventPriority.HIGH,
            source="test",
            data={},
            damage_dealt=100.0,
            critical_hit=True
        )

        self.dispatcher.dispatch(combat_event)
        time.sleep(0.1)  # Allow time for processing

        # Verify event was handled
        self.assertEqual(len(self.received_events), 1)
        self.assertTrue(self.received_events[0].handled)
        self.assertEqual(self.received_events[0].category, EventCategory.COMBAT)

    def test_priority_handling(self):
        """Test that events are handled in priority order."""
        received_order = []

        def priority_handler(priority: str):
            def handler(event: GameEvent):
                received_order.append(priority)
            return handler

        # Subscribe handlers with different priorities
        self.dispatcher.subscribe(priority_handler("critical"), 
                                EventCategory.SYSTEM, EventPriority.CRITICAL)
        self.dispatcher.subscribe(priority_handler("high"), 
                                EventCategory.SYSTEM, EventPriority.HIGH)
        self.dispatcher.subscribe(priority_handler("normal"), 
                                EventCategory.SYSTEM, EventPriority.NORMAL)

        # Dispatch events with different priorities
        for priority in [EventPriority.NORMAL, EventPriority.HIGH, EventPriority.CRITICAL]:
            event = SystemEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.SYSTEM,
                priority=priority,
                source="test",
                data={},
                operation="test",
                success=True
            )
            self.dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Verify handling order
        self.assertEqual(received_order, ["critical", "high", "normal"])

    def test_event_filtering(self):
        """Test event history filtering."""
        # Create events with different timestamps
        now = datetime.now()
        events = [
            CombatEvent(
                event_id="",
                timestamp=now - timedelta(minutes=i),
                category=EventCategory.COMBAT,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                damage_dealt=50.0
            ) for i in range(5)
        ]

        # Add some events from different category
        events.extend([
            QuestEvent(
                event_id="",
                timestamp=now - timedelta(minutes=i),
                category=EventCategory.QUEST,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                quest_id=f"quest_{i}",
                quest_status="active",
                rewards={}
            ) for i in range(3)
        ])

        # Dispatch all events
        for event in events:
            self.dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Test category filtering
        combat_events = self.dispatcher.get_history(category=EventCategory.COMBAT)
        self.assertEqual(len(combat_events), 5)

        # Test time filtering
        recent_events = self.dispatcher.get_history(
            start_time=now - timedelta(minutes=2)
        )
        self.assertGreater(len(recent_events), 0)

    def test_concurrent_event_handling(self):
        """Test handling multiple events concurrently."""
        event_count = 100
        processed_events = []
        
        def concurrent_handler(event: GameEvent):
            processed_events.append(event)
            time.sleep(0.001)  # Simulate processing time

        self.dispatcher.subscribe(concurrent_handler, 
                                EventCategory.SYSTEM, EventPriority.NORMAL)

        # Dispatch multiple events rapidly
        for i in range(event_count):
            event = SystemEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.SYSTEM,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                operation=f"operation_{i}",
                success=True
            )
            self.dispatcher.dispatch(event)

        time.sleep(1)  # Allow time for processing

        # Verify all events were processed
        self.assertEqual(len(processed_events), event_count)

    def test_handler_error_recovery(self):
        """Test system recovery from handler errors."""
        def failing_handler(event: GameEvent):
            raise Exception("Simulated handler error")

        def backup_handler(event: GameEvent):
            self.received_events.append(event)

        # Subscribe both handlers
        self.dispatcher.subscribe(failing_handler, 
                                EventCategory.COMBAT, EventPriority.HIGH)
        self.dispatcher.subscribe(backup_handler, 
                                EventCategory.COMBAT, EventPriority.NORMAL)

        # Dispatch event
        event = CombatEvent(
            event_id="",
            timestamp=datetime.now(),
            category=EventCategory.COMBAT,
            priority=EventPriority.HIGH,
            source="test",
            data={},
            damage_dealt=100.0
        )
        self.dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Verify backup handler processed the event
        self.assertEqual(len(self.received_events), 1)

    def test_event_history_management(self):
        """Test event history size management."""
        # Create a dispatcher with small history size
        dispatcher = EventDispatcher()
        dispatcher._history.max_history = 5
        dispatcher.start()

        # Dispatch more events than history size
        for i in range(10):
            event = SystemEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.SYSTEM,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                operation=f"operation_{i}",
                success=True
            )
            dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Verify history size is maintained
        history = dispatcher.get_history()
        self.assertEqual(len(history), 5)
        dispatcher.stop()

    def test_complex_event_chain(self):
        """Test chain of events triggering each other."""
        event_chain = []

        def combat_handler(event: CombatEvent):
            event_chain.append("combat")
            if event.critical_hit:
                # Trigger character event
                char_event = CharacterEvent(
                    event_id="",
                    timestamp=datetime.now(),
                    category=EventCategory.CHARACTER,
                    priority=EventPriority.HIGH,
                    source="combat_handler",
                    data={},
                    level=1,
                    experience_gained=100,
                    skills_unlocked=["critical_mastery"],
                    attributes_changed={"strength": 1}
                )
                self.dispatcher.dispatch(char_event)

        def character_handler(event: CharacterEvent):
            event_chain.append("character")
            if event.skills_unlocked:
                # Trigger system event
                sys_event = SystemEvent(
                    event_id="",
                    timestamp=datetime.now(),
                    category=EventCategory.SYSTEM,
                    priority=EventPriority.NORMAL,
                    source="character_handler",
                    data={},
                    operation="skill_unlock",
                    success=True
                )
                self.dispatcher.dispatch(sys_event)

        def system_handler(event: SystemEvent):
            event_chain.append("system")

        # Subscribe handlers
        self.dispatcher.subscribe(combat_handler, EventCategory.COMBAT)
        self.dispatcher.subscribe(character_handler, EventCategory.CHARACTER)
        self.dispatcher.subscribe(system_handler, EventCategory.SYSTEM)

        # Start chain with combat event
        combat_event = CombatEvent(
            event_id="",
            timestamp=datetime.now(),
            category=EventCategory.COMBAT,
            priority=EventPriority.HIGH,
            source="test",
            data={},
            damage_dealt=100.0,
            critical_hit=True
        )
        self.dispatcher.dispatch(combat_event)

        time.sleep(0.2)  # Allow time for chain to complete

        # Verify event chain
        self.assertEqual(event_chain, ["combat", "character", "system"])

    def test_event_aggregation(self):
        """Test event aggregation functionality."""
        damage_total = 0
        hit_count = 0

        def aggregate_handler(event: CombatEvent):
            nonlocal damage_total, hit_count
            damage_total += event.damage_dealt
            hit_count += 1

        # Subscribe aggregation handler
        self.dispatcher.subscribe(aggregate_handler, EventCategory.COMBAT)

        # Dispatch multiple combat events
        for damage in [10.0, 15.0, 25.0, 50.0]:
            event = CombatEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.COMBAT,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                damage_dealt=damage
            )
            self.dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Verify aggregation
        self.assertEqual(damage_total, 100.0)
        self.assertEqual(hit_count, 4)

    def test_pattern_detection(self):
        """Test event pattern detection."""
        # Register a test pattern
        pattern_sequence = [
            EventCategory.COMBAT,
            EventCategory.CHARACTER,
            EventCategory.INVENTORY
        ]
        self.dispatcher._history._patterns = {}  # Clear existing patterns
        self.dispatcher._history.register_pattern("test_pattern", pattern_sequence)

        # Create events matching the pattern
        events = [
            CombatEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.COMBAT,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                damage_dealt=100.0
            ),
            CharacterEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.CHARACTER,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                level=1,
                experience_gained=100,
                skills_unlocked=[],
                attributes_changed={}
            ),
            InventoryEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.INVENTORY,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                item_id="test_item",
                quantity=1,
                action="add"
            )
        ]

        # Dispatch events
        for event in events:
            self.dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Verify pattern detection
        patterns = self.dispatcher._history.get_detected_patterns()
        self.assertIn("test_pattern", patterns)
        self.assertEqual(patterns["test_pattern"], 1)

    def test_combat_combo_tracking(self):
        """Test combat combination tracking."""
        # Create a sequence of combat events
        combat_types = ["slash", "thrust", "slash", "parry", "thrust"]
        
        for combat_type in combat_types:
            event = CombatEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.COMBAT,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                damage_dealt=50.0,
                combat_type=combat_type
            )
            self.dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Verify combo tracking
        combo_analysis = self.dispatcher._history.get_combat_combo_analysis()
        self.assertGreater(len(combo_analysis['combo_distribution']), 0)
        self.assertEqual(combo_analysis['combo_variety'], 4)  # unique combinations

    def test_player_progression_tracking(self):
        """Test player progression metrics tracking."""
        # Create various progression events
        events = [
            WorldEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.WORLD,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                location="new_area",
                event_type="discovery",
                affected_npcs=[],
                permanent_change=True
            ),
            CharacterEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.CHARACTER,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                level=2,
                experience_gained=1000,
                skills_unlocked=["new_skill"],
                attributes_changed={"strength": 1}
            ),
            InventoryEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.INVENTORY,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                item_id="rare_item",
                quantity=1,
                action="add",
                item_rarity="rare"
            )
        ]

        # Dispatch events
        for event in events:
            self.dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Verify progression metrics
        metrics = self.dispatcher._history.get_progression_metrics()
        self.assertGreater(metrics['achievements'], 0)
        self.assertEqual(metrics['locations_explored'], 1)
        self.assertEqual(metrics['skill_diversity'], 1)
        self.assertEqual(metrics['rare_items_found'], 1)

    def test_trend_analysis(self):
        """Test enhanced trend analysis."""
        # Create a series of combat events with increasing damage
        damages = [10.0, 20.0, 30.0, 40.0, 50.0]
        
        for damage in damages:
            event = CombatEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.COMBAT,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                damage_dealt=damage
            )
            self.dispatcher.dispatch(event)

        time.sleep(0.1)  # Allow time for processing

        # Verify trend analysis
        slope, volatility, direction = self.dispatcher._history.get_trend_analysis('damage_dealt')
        self.assertGreater(slope, 0)
        self.assertEqual(direction, TrendDirection.INCREASING)

    def test_engagement_metrics(self):
        """Test player engagement metrics."""
        # Create events with specific timing
        event_types = [
            (CombatEvent, {'damage_dealt': 50.0}),
            (WorldEvent, {'location': 'test_area', 'event_type': 'discovery', 'affected_npcs': []}),
            (QuestEvent, {'quest_id': 'test_quest', 'quest_status': 'complete', 'rewards': {}})
        ]

        for event_class, extra_args in event_types:
            event = event_class(
                event_id="",
                timestamp=datetime.now(),
                category=event_class.category if hasattr(event_class, 'category') else EventCategory.COMBAT,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                **extra_args
            )
            self.dispatcher.dispatch(event)
            time.sleep(0.1)  # Create time gaps between events

        # Verify engagement metrics
        metrics = self.dispatcher._history.get_player_engagement_metrics()
        self.assertGreater(metrics['actions_per_minute'], 0)
        self.assertGreater(metrics['activity_diversity'], 0)
        self.assertGreater(metrics['avg_time_between_actions'], 0)

    def test_complex_event_chain_with_patterns(self):
        """Test complex event chains with pattern recognition."""
        # Register a combat pattern
        combat_pattern = [
            EventCategory.COMBAT,
            EventCategory.COMBAT,
            EventCategory.CHARACTER
        ]
        self.dispatcher._history.register_pattern("combat_combo", combat_pattern)

        # Create a complex chain of events
        events = []
        # First combo
        events.extend([
            CombatEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.COMBAT,
                priority=EventPriority.HIGH,
                source="test",
                data={},
                damage_dealt=100.0,
                combat_type="slash"
            ),
            CombatEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.COMBAT,
                priority=EventPriority.HIGH,
                source="test",
                data={},
                damage_dealt=150.0,
                combat_type="thrust"
            ),
            CharacterEvent(
                event_id="",
                timestamp=datetime.now(),
                category=EventCategory.CHARACTER,
                priority=EventPriority.NORMAL,
                source="test",
                data={},
                level=1,
                experience_gained=200,
                skills_unlocked=["combo_mastery"],
                attributes_changed={"dexterity": 1}
            )
        ])

        # Dispatch events
        for event in events:
            self.dispatcher.dispatch(event)
            time.sleep(0.05)  # Small delay between events

        # Verify pattern detection and metrics
        patterns = self.dispatcher._history.get_detected_patterns()
        self.assertIn("combat_combo", patterns)
        self.assertEqual(patterns["combat_combo"], 1)

        # Verify combat efficiency
        efficiency_metrics = self.dispatcher._history.get_combat_efficiency_metrics()
        self.assertGreater(efficiency_metrics['combo_efficiency'], 0)
        self.assertGreater(efficiency_metrics['combat_mastery'], 0)

if __name__ == '__main__':
    unittest.main() 