from enum import Enum
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import random
import math
import json
import logging

class AIBehaviorType(Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    TACTICAL = "tactical"
    SUPPORT = "support"
    BERSERKER = "berserker"
    CAUTIOUS = "cautious"

class CombatRole(Enum):
    TANK = "tank"
    DPS = "dps"
    HEALER = "healer"
    CONTROLLER = "controller"
    BUFFER = "buffer"
    DEBUFFER = "debuffer"

@dataclass
class AIState:
    health_percentage: float
    energy_percentage: float
    status_effects: List[str]
    available_abilities: List[str]
    allies_nearby: List[Dict[str, Any]]
    enemies_nearby: List[Dict[str, Any]]
    position: Dict[str, float]
    threat_level: float
    last_action: Optional[str] = None
    
class BehaviorNode:
    def __init__(self, name: str):
        self.name = name
        self.children: List[BehaviorNode] = []
        
    def add_child(self, child: 'BehaviorNode'):
        self.children.append(child)
        
    def evaluate(self, state: AIState) -> bool:
        raise NotImplementedError

class SequenceNode(BehaviorNode):
    def evaluate(self, state: AIState) -> bool:
        for child in self.children:
            if not child.evaluate(state):
                return False
        return True

class SelectorNode(BehaviorNode):
    def evaluate(self, state: AIState) -> bool:
        for child in self.children:
            if child.evaluate(state):
                return True
        return False

class ConditionNode(BehaviorNode):
    def __init__(self, name: str, condition: Callable[[AIState], bool]):
        super().__init__(name)
        self.condition = condition
        
    def evaluate(self, state: AIState) -> bool:
        return self.condition(state)

class ActionNode(BehaviorNode):
    def __init__(self, name: str, action: Callable[[AIState], bool]):
        super().__init__(name)
        self.action = action
        
    def evaluate(self, state: AIState) -> bool:
        return self.action(state)

class CombatAI:
    def __init__(self):
        self.behavior_type = AIBehaviorType.TACTICAL
        self.combat_role = CombatRole.DPS
        self.behavior_tree = self._build_behavior_tree()
        self.state = None
        self.logger = self._setup_logger()
        self.action_history: List[Dict[str, Any]] = []
        self.decision_weights = self._initialize_decision_weights()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("CombatAI")
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler("logs/combat_ai.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        logger.addHandler(handler)
        return logger
        
    def _initialize_decision_weights(self) -> Dict[str, float]:
        return {
            "health_importance": 0.8,
            "energy_importance": 0.6,
            "positioning_importance": 0.7,
            "threat_importance": 0.5,
            "ally_support_importance": 0.4,
            "ability_combo_importance": 0.6
        }
        
    def _build_behavior_tree(self) -> BehaviorNode:
        root = SelectorNode("Root")
        
        # Emergency response branch
        emergency = SequenceNode("Emergency")
        emergency.add_child(ConditionNode("LowHealth", self._is_low_health))
        emergency.add_child(SelectorNode("EmergencyActions")
            .add_child(ActionNode("UseHealingAbility", self._use_healing_ability))
            .add_child(ActionNode("Retreat", self._retreat)))
        root.add_child(emergency)
        
        # Tactical combat branch
        tactical = SequenceNode("Tactical")
        tactical.add_child(ConditionNode("CombatReady", self._is_combat_ready))
        
        combat_actions = SelectorNode("CombatActions")
        
        # Offensive actions
        offensive = SequenceNode("Offensive")
        offensive.add_child(ConditionNode("CanAttack", self._can_attack))
        offensive.add_child(SelectorNode("AttackActions")
            .add_child(ActionNode("UseSpecialAbility", self._use_special_ability))
            .add_child(ActionNode("BasicAttack", self._basic_attack)))
        combat_actions.add_child(offensive)
        
        # Support actions
        support = SequenceNode("Support")
        support.add_child(ConditionNode("CanSupport", self._can_support))
        support.add_child(ActionNode("SupportAction", self._support_action))
        combat_actions.add_child(support)
        
        tactical.add_child(combat_actions)
        root.add_child(tactical)
        
        return root
        
    def update_state(self, new_state: Dict[str, Any]):
        """Update AI state with new information"""
        self.state = AIState(**new_state)
        self.logger.debug(f"State updated: Health={self.state.health_percentage:.2f}, "
                         f"Energy={self.state.energy_percentage:.2f}, "
                         f"Threat={self.state.threat_level:.2f}")
                         
    def decide_action(self) -> Dict[str, Any]:
        """Decide next action based on current state"""
        if not self.state:
            self.logger.error("No state available for decision making")
            return {"action": "none", "reason": "no_state"}
            
        try:
            # Evaluate behavior tree
            action_result = self.behavior_tree.evaluate(self.state)
            
            # Record action
            action_data = {
                "action": self.state.last_action,
                "state": {
                    "health": self.state.health_percentage,
                    "energy": self.state.energy_percentage,
                    "threat": self.state.threat_level
                },
                "timestamp": time.time()
            }
            self.action_history.append(action_data)
            
            return action_result
            
        except Exception as e:
            self.logger.error(f"Error in decision making: {str(e)}")
            return {"action": "none", "reason": "error"}
            
    def _is_low_health(self, state: AIState) -> bool:
        """Check if health is critically low"""
        return state.health_percentage < 0.3
        
    def _is_combat_ready(self, state: AIState) -> bool:
        """Check if ready for combat"""
        return (state.health_percentage > 0.2 and 
                state.energy_percentage > 0.1 and
                not any(effect in ["stunned", "frozen", "paralyzed"] 
                       for effect in state.status_effects))
                       
    def _can_attack(self, state: AIState) -> bool:
        """Check if can perform attack actions"""
        return (len(state.enemies_nearby) > 0 and
                any(ability for ability in state.available_abilities
                    if self._is_offensive_ability(ability)))
                    
    def _can_support(self, state: AIState) -> bool:
        """Check if can perform support actions"""
        return (len(state.allies_nearby) > 0 and
                any(ability for ability in state.available_abilities
                    if self._is_support_ability(ability)))
                    
    def _use_healing_ability(self, state: AIState) -> bool:
        """Use healing ability if available"""
        healing_ability = next(
            (ability for ability in state.available_abilities
             if self._is_healing_ability(ability)),
            None
        )
        
        if healing_ability:
            state.last_action = f"heal_{healing_ability}"
            return True
        return False
        
    def _retreat(self, state: AIState) -> bool:
        """Perform retreat action"""
        # Find safest direction
        retreat_pos = self._calculate_retreat_position(state)
        state.last_action = "retreat"
        state.position = retreat_pos
        return True
        
    def _use_special_ability(self, state: AIState) -> bool:
        """Use best available special ability"""
        ability = self._select_best_ability(state)
        if ability:
            state.last_action = f"special_{ability}"
            return True
        return False
        
    def _basic_attack(self, state: AIState) -> bool:
        """Perform basic attack"""
        target = self._select_best_target(state)
        if target:
            state.last_action = f"attack_{target['id']}"
            return True
        return False
        
    def _support_action(self, state: AIState) -> bool:
        """Perform support action"""
        ally = self._select_ally_to_support(state)
        ability = self._select_support_ability(state)
        
        if ally and ability:
            state.last_action = f"support_{ability}_{ally['id']}"
            return True
        return False
        
    def _calculate_retreat_position(self, state: AIState) -> Dict[str, float]:
        """Calculate optimal retreat position"""
        # Simple retreat - move away from nearest enemy
        if state.enemies_nearby:
            nearest = min(state.enemies_nearby,
                        key=lambda e: self._distance(state.position, e["position"]))
            
            dx = state.position["x"] - nearest["position"]["x"]
            dy = state.position["y"] - nearest["position"]["y"]
            
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                return {
                    "x": state.position["x"] + (dx/distance) * 5,
                    "y": state.position["y"] + (dy/distance) * 5
                }
                
        return state.position
        
    def _select_best_ability(self, state: AIState) -> Optional[str]:
        """Select best ability based on current situation"""
        abilities = [a for a in state.available_abilities 
                    if self._is_offensive_ability(a)]
                    
        if not abilities:
            return None
            
        # Score each ability
        scored_abilities = [
            (ability, self._score_ability(ability, state))
            for ability in abilities
        ]
        
        return max(scored_abilities, key=lambda x: x[1])[0]
        
    def _select_best_target(self, state: AIState) -> Optional[Dict[str, Any]]:
        """Select best target based on various factors"""
        if not state.enemies_nearby:
            return None
            
        # Score each target
        scored_targets = [
            (target, self._score_target(target, state))
            for target in state.enemies_nearby
        ]
        
        return max(scored_targets, key=lambda x: x[1])[0]
        
    def _select_ally_to_support(self, state: AIState) -> Optional[Dict[str, Any]]:
        """Select ally most in need of support"""
        if not state.allies_nearby:
            return None
            
        return min(state.allies_nearby,
                  key=lambda a: a.get("health_percentage", 1.0))
                  
    def _select_support_ability(self, state: AIState) -> Optional[str]:
        """Select appropriate support ability"""
        abilities = [a for a in state.available_abilities 
                    if self._is_support_ability(a)]
                    
        return next(iter(abilities)) if abilities else None
        
    def _score_ability(self, ability: str, state: AIState) -> float:
        """Score an ability based on current situation"""
        base_score = 1.0
        
        # Add situational modifiers
        if state.health_percentage < 0.5:
            base_score *= 0.8  # Prefer safer abilities when low health
            
        if state.energy_percentage < 0.3:
            base_score *= 0.7  # Prefer energy-efficient abilities
            
        if len(state.enemies_nearby) > 2:
            base_score *= 1.2  # Bonus for AOE abilities
            
        return base_score
        
    def _score_target(self, target: Dict[str, Any], state: AIState) -> float:
        """Score a target based on various factors"""
        base_score = 1.0
        
        # Distance factor
        distance = self._distance(state.position, target["position"])
        base_score *= 1.0 / (1.0 + distance * 0.1)
        
        # Health factor
        target_health = target.get("health_percentage", 1.0)
        base_score *= 1.0 + (1.0 - target_health)
        
        # Threat factor
        threat = target.get("threat_level", 0.5)
        base_score *= 1.0 + threat
        
        return base_score
        
    def _distance(self, pos1: Dict[str, float], pos2: Dict[str, float]) -> float:
        """Calculate distance between two positions"""
        dx = pos1["x"] - pos2["x"]
        dy = pos1["y"] - pos2["y"]
        return math.sqrt(dx*dx + dy*dy)
        
    def _is_offensive_ability(self, ability: str) -> bool:
        """Check if ability is offensive"""
        return "attack" in ability.lower() or "strike" in ability.lower()
        
    def _is_support_ability(self, ability: str) -> bool:
        """Check if ability is supportive"""
        return "heal" in ability.lower() or "buff" in ability.lower()
        
    def _is_healing_ability(self, ability: str) -> bool:
        """Check if ability is healing"""
        return "heal" in ability.lower() or "cure" in ability.lower()
        
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze AI combat performance"""
        if not self.action_history:
            return {"status": "no_data"}
            
        analysis = {
            "total_actions": len(self.action_history),
            "action_distribution": {},
            "average_health": 0,
            "average_energy": 0,
            "average_threat": 0
        }
        
        # Calculate statistics
        for entry in self.action_history:
            action_type = entry["action"].split("_")[0]
            analysis["action_distribution"][action_type] = \
                analysis["action_distribution"].get(action_type, 0) + 1
                
            analysis["average_health"] += entry["state"]["health"]
            analysis["average_energy"] += entry["state"]["energy"]
            analysis["average_threat"] += entry["state"]["threat"]
            
        # Calculate averages
        total = len(self.action_history)
        analysis["average_health"] /= total
        analysis["average_energy"] /= total
        analysis["average_threat"] /= total
        
        # Convert counts to percentages
        for action_type in analysis["action_distribution"]:
            analysis["action_distribution"][action_type] = \
                analysis["action_distribution"][action_type] / total * 100
                
        return analysis
        
    def export_behavior_data(self, file_path: str):
        """Export behavior data for analysis"""
        data = {
            "behavior_type": self.behavior_type.value,
            "combat_role": self.combat_role.value,
            "decision_weights": self.decision_weights,
            "action_history": self.action_history
        }
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            
    def import_behavior_data(self, file_path: str):
        """Import behavior data"""
        with open(file_path, "r") as f:
            data = json.load(f)
            
        self.behavior_type = AIBehaviorType(data["behavior_type"])
        self.combat_role = CombatRole(data["combat_role"])
        self.decision_weights = data["decision_weights"]
        self.action_history = data["action_history"] 