"""
Quest System Analyzer Tool

This tool provides real-time analysis and debugging capabilities for the quest system
in Elysian Nexus. It tracks quest states, monitors progression, and identifies potential
issues in quest chains and requirements.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='quest_analyzer.log'
)
logger = logging.getLogger('QuestAnalyzer')

@dataclass
class QuestState:
    """Represents the current state of a quest."""
    quest_id: str
    category: str
    status: str  # active, completed, failed, available
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    objectives_progress: Dict[str, float] = field(default_factory=dict)
    current_dimension: Optional[str] = None
    player_level: int = 1
    rewards_claimed: bool = False

@dataclass
class QuestChainAnalysis:
    """Analysis results for a quest chain."""
    chain_id: str
    completed_quests: List[str]
    available_quests: List[str]
    blocked_quests: List[str]
    blocking_requirements: Dict[str, List[str]]
    estimated_completion_time: Optional[timedelta] = None

class QuestAnalyzer:
    def __init__(self, config_path: str = "config/features/quest_system.json"):
        """Initialize the Quest Analyzer with configuration."""
        self.config = self._load_config(config_path)
        self.quest_states: Dict[str, QuestState] = {}
        self.active_chains: Dict[str, QuestChainAnalysis] = {}
        self.performance_metrics: Dict[str, float] = {
            'avg_completion_time': 0,
            'failure_rate': 0,
            'objective_completion_rate': 0
        }
        logger.info("Quest Analyzer initialized")

    def _load_config(self, config_path: str) -> dict:
        """Load quest system configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def track_quest_state(self, quest_state: QuestState) -> None:
        """Track the state of a quest and update analysis."""
        self.quest_states[quest_state.quest_id] = quest_state
        self._analyze_quest_requirements(quest_state)
        self._update_performance_metrics()
        logger.info(f"Updated state for quest {quest_state.quest_id}")

    def _analyze_quest_requirements(self, quest_state: QuestState) -> None:
        """Analyze if quest requirements are met and identify blocking issues."""
        category_config = self.config['quest_categories'].get(quest_state.category)
        if not category_config:
            logger.warning(f"Unknown quest category: {quest_state.category}")
            return

        # Check level requirements
        if quest_state.player_level < category_config['min_level']:
            logger.warning(
                f"Player level {quest_state.player_level} below required "
                f"{category_config['min_level']} for quest {quest_state.quest_id}"
            )

        # Check dimensional requirements
        if (category_config['dimensional_requirements'] and 
            not quest_state.current_dimension):
            logger.warning(
                f"Missing dimensional requirement for quest {quest_state.quest_id}"
            )

    def analyze_quest_chain(self, chain_id: str) -> QuestChainAnalysis:
        """Analyze the state and progression of a quest chain."""
        chain_quests = self._get_chain_quests(chain_id)
        completed = []
        available = []
        blocked = []
        blocking_reqs = {}

        for quest_id in chain_quests:
            state = self.quest_states.get(quest_id)
            if not state:
                continue

            if state.status == 'completed':
                completed.append(quest_id)
            elif state.status == 'available':
                if self._check_requirements(quest_id):
                    available.append(quest_id)
                else:
                    blocked.append(quest_id)
                    blocking_reqs[quest_id] = self._get_blocking_requirements(quest_id)

        analysis = QuestChainAnalysis(
            chain_id=chain_id,
            completed_quests=completed,
            available_quests=available,
            blocked_quests=blocked,
            blocking_requirements=blocking_reqs,
            estimated_completion_time=self._estimate_completion_time(chain_id)
        )
        
        self.active_chains[chain_id] = analysis
        return analysis

    def _get_chain_quests(self, chain_id: str) -> List[str]:
        """Get all quests in a chain."""
        # Implementation would depend on quest chain data structure
        return []

    def _check_requirements(self, quest_id: str) -> bool:
        """Check if all requirements are met for a quest."""
        state = self.quest_states.get(quest_id)
        if not state:
            return False

        category_config = self.config['quest_categories'].get(state.category)
        if not category_config:
            return False

        # Check level requirement
        if state.player_level < category_config['min_level']:
            return False

        # Check dimensional requirement
        if (category_config['dimensional_requirements'] and 
            not state.current_dimension):
            return False

        return True

    def _get_blocking_requirements(self, quest_id: str) -> List[str]:
        """Get list of requirements blocking a quest."""
        blocking = []
        state = self.quest_states.get(quest_id)
        if not state:
            return blocking

        category_config = self.config['quest_categories'].get(state.category)
        if not category_config:
            return blocking

        if state.player_level < category_config['min_level']:
            blocking.append(f"Level {category_config['min_level']} required")

        if (category_config['dimensional_requirements'] and 
            not state.current_dimension):
            blocking.append("Dimensional access required")

        return blocking

    def _estimate_completion_time(self, chain_id: str) -> Optional[timedelta]:
        """Estimate time to complete remaining quests in chain."""
        completed_quests = [q for q in self.quest_states.values() 
                          if q.status == 'completed' and 
                          q.start_time and q.completion_time]
        
        if not completed_quests:
            return None

        avg_time = sum(
            (q.completion_time - q.start_time).total_seconds() 
            for q in completed_quests
        ) / len(completed_quests)

        remaining_quests = len(self._get_chain_quests(chain_id)) - len(completed_quests)
        return timedelta(seconds=avg_time * remaining_quests)

    def _update_performance_metrics(self) -> None:
        """Update performance metrics based on current quest states."""
        completed_quests = [q for q in self.quest_states.values() 
                          if q.status == 'completed']
        failed_quests = [q for q in self.quest_states.values() 
                        if q.status == 'failed']
        
        if completed_quests:
            avg_time = sum(
                (q.completion_time - q.start_time).total_seconds() 
                for q in completed_quests 
                if q.start_time and q.completion_time
            ) / len(completed_quests)
            self.performance_metrics['avg_completion_time'] = avg_time

        total_quests = len(completed_quests) + len(failed_quests)
        if total_quests > 0:
            self.performance_metrics['failure_rate'] = len(failed_quests) / total_quests

        objective_progress = sum(
            sum(o.values()) / len(o) 
            for q in self.quest_states.values() 
            if (o := q.objectives_progress)
        ) / len(self.quest_states) if self.quest_states else 0
        self.performance_metrics['objective_completion_rate'] = objective_progress

    def generate_report(self) -> dict:
        """Generate a comprehensive analysis report."""
        return {
            'quest_states': {
                quest_id: {
                    'category': state.category,
                    'status': state.status,
                    'progress': sum(state.objectives_progress.values()) / 
                              len(state.objectives_progress) 
                              if state.objectives_progress else 0,
                    'time_active': (
                        (datetime.now() - state.start_time).total_seconds()
                        if state.start_time and state.status == 'active'
                        else None
                    )
                }
                for quest_id, state in self.quest_states.items()
            },
            'active_chains': {
                chain_id: {
                    'completion_percentage': (
                        len(analysis.completed_quests) / 
                        (len(analysis.completed_quests) + 
                         len(analysis.available_quests) + 
                         len(analysis.blocked_quests)) * 100
                    ),
                    'blocked_quests': len(analysis.blocked_quests),
                    'estimated_completion_time': (
                        analysis.estimated_completion_time.total_seconds()
                        if analysis.estimated_completion_time
                        else None
                    )
                }
                for chain_id, analysis in self.active_chains.items()
            },
            'performance_metrics': self.performance_metrics
        }

def main():
    """Main function to demonstrate the Quest Analyzer usage."""
    analyzer = QuestAnalyzer()
    
    # Example quest state
    quest_state = QuestState(
        quest_id="quest_001",
        category="main_story",
        status="active",
        start_time=datetime.now(),
        objectives_progress={'objective1': 0.5, 'objective2': 0.75},
        current_dimension="physical",
        player_level=5
    )
    
    # Track quest state
    analyzer.track_quest_state(quest_state)
    
    # Analyze quest chain
    chain_analysis = analyzer.analyze_quest_chain("chain_001")
    
    # Generate report
    report = analyzer.generate_report()
    
    # Log results
    logger.info("Quest Analysis Report:")
    logger.info(json.dumps(report, indent=2))

if __name__ == "__main__":
    main() 