from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

class QuestType(Enum):
    MAIN = "main"
    SIDE = "side"
    DAILY = "daily"
    FACTION = "faction"
    WORLD = "world"
    CHALLENGE = "challenge"
    EVENT = "event"

class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"

class QuestDifficulty(Enum):
    TRIVIAL = "trivial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    LEGENDARY = "legendary"

@dataclass
class QuestObjective:
    description: str
    target_amount: int = 1
    current_amount: int = 0
    completed: bool = False

@dataclass
class QuestReward:
    experience: int
    gold: int
    items: List[str]
    reputation: Dict[str, int]
    special_rewards: List[str]

@dataclass
class Quest:
    id: str
    title: str
    description: str
    type: QuestType
    difficulty: QuestDifficulty
    objectives: List[QuestObjective]
    rewards: QuestReward
    prerequisites: List[str]
    level_requirement: int
    faction_requirement: Optional[str] = None
    time_limit: Optional[int] = None  # in seconds
    start_time: Optional[datetime] = None
    status: QuestStatus = QuestStatus.NOT_STARTED
    hidden: bool = False
    repeatable: bool = False
    completion_count: int = 0

class QuestSystem:
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.active_quests: Dict[str, Quest] = {}
        self.completed_quests: Dict[str, Quest] = {}
        self.failed_quests: Dict[str, Quest] = {}
        self.quest_chains: Dict[str, List[str]] = {}
        self.quest_callbacks: Dict[str, List[Callable]] = {}

    def add_quest(self, quest: Quest):
        """Add a new quest to the system"""
        self.quests[quest.id] = quest

    def remove_quest(self, quest_id: str):
        """Remove a quest from the system"""
        if quest_id in self.quests:
            del self.quests[quest_id]

    def start_quest(self, quest_id: str) -> bool:
        """Start a quest if prerequisites are met"""
        if quest_id not in self.quests:
            return False

        quest = self.quests[quest_id]
        if not self._check_prerequisites(quest):
            return False

        quest.status = QuestStatus.IN_PROGRESS
        quest.start_time = datetime.now()
        self.active_quests[quest_id] = quest
        return True

    def complete_quest(self, quest_id: str) -> bool:
        """Complete a quest and grant rewards"""
        if quest_id not in self.active_quests:
            return False

        quest = self.active_quests[quest_id]
        if not self._are_objectives_complete(quest):
            return False

        quest.status = QuestStatus.COMPLETED
        quest.completion_count += 1
        self.completed_quests[quest_id] = quest
        del self.active_quests[quest_id]

        self._grant_rewards(quest)
        self._trigger_callbacks(quest_id, "complete")
        return True

    def fail_quest(self, quest_id: str):
        """Fail a quest"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            quest.status = QuestStatus.FAILED
            self.failed_quests[quest_id] = quest
            del self.active_quests[quest_id]
            self._trigger_callbacks(quest_id, "fail")

    def update_objective(self, quest_id: str, objective_index: int, amount: int = 1) -> bool:
        """Update progress of a quest objective"""
        if quest_id not in self.active_quests:
            return False

        quest = self.active_quests[quest_id]
        if objective_index >= len(quest.objectives):
            return False

        objective = quest.objectives[objective_index]
        objective.current_amount = min(objective.current_amount + amount,
                                     objective.target_amount)
        objective.completed = objective.current_amount >= objective.target_amount

        if self._are_objectives_complete(quest):
            self._trigger_callbacks(quest_id, "objectives_complete")

        return True

    def get_available_quests(self, player_level: int,
                           completed_quests: List[str],
                           faction_reputation: Dict[str, int]) -> List[Quest]:
        """Get all available quests for the player"""
        available = []
        for quest in self.quests.values():
            if (quest.status == QuestStatus.NOT_STARTED and
                not quest.hidden and
                player_level >= quest.level_requirement and
                self._check_prerequisites(quest) and
                self._check_faction_requirements(quest, faction_reputation) and
                (quest.repeatable or quest.id not in completed_quests)):
                available.append(quest)
        return available

    def get_active_quests(self) -> List[Quest]:
        """Get all active quests"""
        return list(self.active_quests.values())

    def get_completed_quests(self) -> List[Quest]:
        """Get all completed quests"""
        return list(self.completed_quests.values())

    def get_failed_quests(self) -> List[Quest]:
        """Get all failed quests"""
        return list(self.failed_quests.values())

    def add_quest_callback(self, quest_id: str, callback: Callable):
        """Add a callback for quest events"""
        if quest_id not in self.quest_callbacks:
            self.quest_callbacks[quest_id] = []
        self.quest_callbacks[quest_id].append(callback)

    def remove_quest_callback(self, quest_id: str, callback: Callable):
        """Remove a quest callback"""
        if quest_id in self.quest_callbacks:
            self.quest_callbacks[quest_id] = [
                cb for cb in self.quest_callbacks[quest_id]
                if cb != callback
            ]

    def update(self):
        """Update quest system, checking for expired quests"""
        current_time = datetime.now()
        expired_quests = []

        for quest_id, quest in self.active_quests.items():
            if quest.time_limit and quest.start_time:
                elapsed = (current_time - quest.start_time).total_seconds()
                if elapsed > quest.time_limit:
                    expired_quests.append(quest_id)

        for quest_id in expired_quests:
            quest = self.active_quests[quest_id]
            quest.status = QuestStatus.EXPIRED
            self.failed_quests[quest_id] = quest
            del self.active_quests[quest_id]
            self._trigger_callbacks(quest_id, "expire")

    def add_quest_chain(self, chain_id: str, quest_ids: List[str]):
        """Add a quest chain"""
        self.quest_chains[chain_id] = quest_ids

    def get_next_chain_quest(self, chain_id: str) -> Optional[str]:
        """Get the next quest in a chain"""
        if chain_id not in self.quest_chains:
            return None

        for quest_id in self.quest_chains[chain_id]:
            if quest_id not in self.completed_quests:
                return quest_id
        return None

    def _check_prerequisites(self, quest: Quest) -> bool:
        """Check if quest prerequisites are met"""
        for prereq_id in quest.prerequisites:
            if prereq_id not in self.completed_quests:
                return False
        return True

    def _check_faction_requirements(self, quest: Quest,
                                  faction_reputation: Dict[str, int]) -> bool:
        """Check if faction requirements are met"""
        if not quest.faction_requirement:
            return True
        return faction_reputation.get(quest.faction_requirement, 0) >= 0

    def _are_objectives_complete(self, quest: Quest) -> bool:
        """Check if all quest objectives are complete"""
        return all(obj.completed for obj in quest.objectives)

    def _grant_rewards(self, quest: Quest):
        """Grant quest rewards (placeholder)"""
        print(f"Granting rewards for quest: {quest.title}")
        print(f"- Experience: {quest.rewards.experience}")
        print(f"- Gold: {quest.rewards.gold}")
        print(f"- Items: {', '.join(quest.rewards.items)}")
        for faction, rep in quest.rewards.reputation.items():
            print(f"- {faction} reputation: {rep}")
        if quest.rewards.special_rewards:
            print(f"- Special rewards: {', '.join(quest.rewards.special_rewards)}")

    def _trigger_callbacks(self, quest_id: str, event: str):
        """Trigger quest callbacks"""
        if quest_id in self.quest_callbacks:
            for callback in self.quest_callbacks[quest_id]:
                callback(quest_id, event) 