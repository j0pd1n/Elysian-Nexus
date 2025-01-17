import unittest
from unittest.mock import Mock, patch
import time
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum

from faction_territory_system import FactionTerritorySystem, TerritoryType
from faction_alliance_system import FactionAllianceSystem, AllianceType
from dialogue_system import DialogueSystem

class QuestType(Enum):
    CELESTIAL_EVENT = "celestial_event"
    RITUAL = "ritual"
    FACTION = "faction"
    DYNAMIC = "dynamic"

class QuestStatus(Enum):
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class QuestObjective:
    description: str
    type: str
    required_progress: int
    current_progress: int = 0
    completed: bool = False
    
@dataclass
class QuestReward:
    faction_reputation: Dict[str, float]
    ritual_knowledge: Dict[str, float]
    celestial_affinity: float
    special_items: List[str]

class QuestSystemTest(unittest.TestCase):
    def setUp(self):
        self.territory_system = FactionTerritorySystem()
        self.alliance_system = FactionAllianceSystem()
        self.dialogue_system = DialogueSystem()
        
        # Initialize test data
        self.celestial_order = "Celestial Order"
        self.void_seekers = "Void Seekers"
        self.test_territory = self.territory_system.create_territory(
            name="Sacred Grove",
            territory_type=TerritoryType.CELESTIAL,
            strategic_value=100.0
        )
        
        # Quest tracking
        self.active_quests: Dict[str, Dict] = {}
        self.completed_quests: Dict[str, Dict] = {}
        self.quest_chains: Dict[str, List[str]] = {}
        
    def test_celestial_quest_chain_creation(self):
        """Test creation of celestial event quest chains"""
        # Create celestial convergence quest chain
        convergence_chain = [
            {
                'id': 'celestial_signs',
                'name': 'Signs in the Heavens',
                'type': QuestType.CELESTIAL_EVENT,
                'description': 'Observe and document celestial anomalies',
                'objectives': [
                    QuestObjective(
                        description="Observe celestial patterns",
                        type="observation",
                        required_progress=3
                    ),
                    QuestObjective(
                        description="Record constellation alignments",
                        type="recording",
                        required_progress=5
                    )
                ],
                'rewards': QuestReward(
                    faction_reputation={self.celestial_order: 10},
                    ritual_knowledge={"celestial_observation": 0.2},
                    celestial_affinity=0.1,
                    special_items=["Star Chart"]
                )
            },
            {
                'id': 'power_gathering',
                'name': 'Gathering the Power',
                'type': QuestType.RITUAL,
                'description': 'Prepare the ritual components',
                'prerequisites': ['celestial_signs'],
                'objectives': [
                    QuestObjective(
                        description="Collect celestial essence",
                        type="gathering",
                        required_progress=100
                    ),
                    QuestObjective(
                        description="Attune ritual focuses",
                        type="crafting",
                        required_progress=3
                    )
                ],
                'rewards': QuestReward(
                    faction_reputation={self.celestial_order: 15},
                    ritual_knowledge={"power_focusing": 0.3},
                    celestial_affinity=0.2,
                    special_items=["Attuned Focus"]
                )
            },
            {
                'id': 'convergence_ritual',
                'name': 'The Great Convergence',
                'type': QuestType.CELESTIAL_EVENT,
                'description': 'Perform the convergence ritual',
                'prerequisites': ['power_gathering'],
                'objectives': [
                    QuestObjective(
                        description="Establish ritual circle",
                        type="ritual",
                        required_progress=1
                    ),
                    QuestObjective(
                        description="Channel celestial power",
                        type="channeling",
                        required_progress=1000
                    ),
                    QuestObjective(
                        description="Stabilize convergence",
                        type="stabilization",
                        required_progress=1
                    )
                ],
                'rewards': QuestReward(
                    faction_reputation={self.celestial_order: 25},
                    ritual_knowledge={"convergence_mastery": 0.5},
                    celestial_affinity=0.4,
                    special_items=["Convergence Crystal"]
                )
            }
        ]
        
        # Register quest chain
        chain_id = "celestial_convergence"
        self.quest_chains[chain_id] = [quest['id'] for quest in convergence_chain]
        
        # Verify chain structure
        self.assertEqual(len(self.quest_chains[chain_id]), 3)
        self.assertEqual(convergence_chain[2]['prerequisites'], ['power_gathering'])
        
        # Test quest availability
        self.assertTrue(self._is_quest_available(convergence_chain[0]))
        self.assertFalse(self._is_quest_available(convergence_chain[1]))
        
    def test_faction_ritual_quest_generation(self):
        """Test generation of faction-specific ritual quests"""
        # Create faction ritual quest
        ritual_quest = {
            'id': 'celestial_initiation',
            'name': 'Celestial Order Initiation',
            'type': QuestType.RITUAL,
            'faction': self.celestial_order,
            'description': 'Complete the initiation ritual',
            'objectives': [
                QuestObjective(
                    description="Study ancient texts",
                    type="study",
                    required_progress=5
                ),
                QuestObjective(
                    description="Perform cleansing ritual",
                    type="ritual",
                    required_progress=1
                ),
                QuestObjective(
                    description="Channel celestial energy",
                    type="channeling",
                    required_progress=100
                )
            ],
            'rewards': QuestReward(
                faction_reputation={self.celestial_order: 20},
                ritual_knowledge={"initiation_rites": 0.4},
                celestial_affinity=0.2,
                special_items=["Initiate's Robes", "Celestial Focus"]
            )
        }
        
        # Add quest to active quests
        self.active_quests[ritual_quest['id']] = ritual_quest
        
        # Test quest tracking
        self.assertIn('celestial_initiation', self.active_quests)
        self.assertEqual(
            len(self.active_quests['celestial_initiation']['objectives']),
            3
        )
        
    def test_dynamic_event_quest_generation(self):
        """Test dynamic generation of event-based quests"""
        # Create celestial pattern
        pattern = Mock(
            pattern_type="CELESTIAL_CONVERGENCE",
            alignment=TerritoryType.CELESTIAL,
            intensity=0.8,
            duration=3600
        )
        
        # Generate dynamic quest based on celestial event
        dynamic_quest = self._generate_dynamic_quest(pattern)
        
        # Verify quest properties
        self.assertEqual(dynamic_quest['type'], QuestType.DYNAMIC)
        self.assertTrue(any(
            obj.type == "observation" 
            for obj in dynamic_quest['objectives']
        ))
        self.assertGreater(
            dynamic_quest['rewards'].celestial_affinity,
            0.0
        )
        
    def test_quest_progress_tracking(self):
        """Test tracking of quest progress and completion"""
        # Create test quest
        test_quest = {
            'id': 'ritual_mastery',
            'name': 'Path to Mastery',
            'type': QuestType.RITUAL,
            'status': QuestStatus.IN_PROGRESS,
            'objectives': [
                QuestObjective(
                    description="Complete minor rituals",
                    type="ritual",
                    required_progress=3
                ),
                QuestObjective(
                    description="Study ritual texts",
                    type="study",
                    required_progress=5
                )
            ],
            'rewards': QuestReward(
                faction_reputation={self.celestial_order: 15},
                ritual_knowledge={"ritual_mastery": 0.3},
                celestial_affinity=0.2,
                special_items=["Master's Grimoire"]
            )
        }
        
        # Add quest to active quests
        self.active_quests[test_quest['id']] = test_quest
        
        # Update progress
        self._update_quest_progress(
            test_quest['id'],
            'ritual',
            2
        )
        self._update_quest_progress(
            test_quest['id'],
            'study',
            5
        )
        
        # Verify progress
        quest = self.active_quests[test_quest['id']]
        self.assertEqual(
            quest['objectives'][0].current_progress,
            2
        )
        self.assertTrue(quest['objectives'][1].completed)
        
        # Complete quest
        self._update_quest_progress(
            test_quest['id'],
            'ritual',
            1
        )
        
        # Verify completion
        self.assertIn(test_quest['id'], self.completed_quests)
        self.assertNotIn(test_quest['id'], self.active_quests)
        
    def _is_quest_available(self, quest: Dict) -> bool:
        """Check if a quest is available based on prerequisites"""
        if 'prerequisites' not in quest:
            return True
            
        return all(
            prereq in self.completed_quests
            for prereq in quest['prerequisites']
        )
        
    def _generate_dynamic_quest(self, celestial_pattern: Mock) -> Dict:
        """Generate a dynamic quest based on celestial event"""
        return {
            'id': f"dynamic_{time.time()}",
            'name': f"{celestial_pattern.pattern_type} Study",
            'type': QuestType.DYNAMIC,
            'description': f"Study the effects of {celestial_pattern.pattern_type}",
            'objectives': [
                QuestObjective(
                    description="Observe celestial phenomena",
                    type="observation",
                    required_progress=3
                ),
                QuestObjective(
                    description="Record energy fluctuations",
                    type="recording",
                    required_progress=5
                ),
                QuestObjective(
                    description="Analyze pattern effects",
                    type="analysis",
                    required_progress=1
                )
            ],
            'rewards': QuestReward(
                faction_reputation={self.celestial_order: 10},
                ritual_knowledge={
                    celestial_pattern.pattern_type.lower(): 0.2
                },
                celestial_affinity=0.1 * celestial_pattern.intensity,
                special_items=[f"{celestial_pattern.pattern_type} Record"]
            )
        }
        
    def _update_quest_progress(
        self,
        quest_id: str,
        objective_type: str,
        progress: int
    ) -> None:
        """Update progress for a quest objective"""
        if quest_id not in self.active_quests:
            return
            
        quest = self.active_quests[quest_id]
        
        # Update matching objectives
        for objective in quest['objectives']:
            if objective.type == objective_type:
                objective.current_progress += progress
                if objective.current_progress >= objective.required_progress:
                    objective.completed = True
                    
        # Check if all objectives are completed
        if all(obj.completed for obj in quest['objectives']):
            self.completed_quests[quest_id] = quest
            del self.active_quests[quest_id] 