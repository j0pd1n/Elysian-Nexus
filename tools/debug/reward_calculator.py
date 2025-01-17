"""
Reward Calculator Tool

This tool calculates and analyzes quest rewards based on various parameters
including player level, difficulty, and reputation standing.
"""

import json
import random
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

@dataclass
class RewardCalculation:
    experience: int
    currency: int
    items: List[Dict[str, any]]
    reputation: Dict[str, int]
    total_value: float

class RewardCalculator:
    def __init__(self, config_path: str = "config/features/reward_tables.json"):
        self.config_path = Path(config_path)
        self.load_config()
        
    def load_config(self) -> None:
        """Load reward tables configuration."""
        with open(self.config_path) as f:
            self.config = json.load(f)
            
    def calculate_quest_rewards(
        self,
        quest_type: str,
        player_level: int,
        difficulty: str = "normal",
        reputation_standing: str = "neutral",
        faction: Optional[str] = None
    ) -> RewardCalculation:
        """Calculate rewards for a quest based on parameters."""
        
        # Calculate base rewards
        experience = self._calculate_experience(quest_type, player_level, difficulty)
        currency = self._calculate_currency(quest_type, player_level, difficulty)
        items = self._generate_item_rewards(quest_type, player_level)
        reputation = self._calculate_reputation(faction, player_level, reputation_standing)
        
        # Calculate total value
        total_value = self._calculate_total_value(
            experience, currency, items, reputation
        )
        
        return RewardCalculation(
            experience=experience,
            currency=currency,
            items=items,
            reputation=reputation,
            total_value=total_value
        )
        
    def _calculate_experience(
        self,
        quest_type: str,
        player_level: int,
        difficulty: str
    ) -> int:
        """Calculate experience reward."""
        exp_table = self.config["experience_tables"][quest_type]
        base_exp = exp_table["base"]
        level_scaling = exp_table["level_scaling"]
        difficulty_mult = exp_table["difficulty_multipliers"][difficulty]
        
        return int(base_exp * (1 + level_scaling * player_level) * difficulty_mult)
        
    def _calculate_currency(
        self,
        quest_type: str,
        player_level: int,
        difficulty: str
    ) -> int:
        """Calculate currency reward."""
        currency_table = self.config["currency_tables"][quest_type]
        base_currency = currency_table["base"]
        level_scaling = currency_table["level_scaling"]
        difficulty_mult = currency_table["difficulty_multipliers"][difficulty]
        
        return int(base_currency * (1 + level_scaling * player_level) * difficulty_mult)
        
    def _generate_item_rewards(
        self,
        quest_type: str,
        player_level: int
    ) -> List[Dict[str, any]]:
        """Generate item rewards from pools."""
        rewards = []
        
        # Select from dimensional artifacts based on level
        tier = self._determine_tier(player_level)
        artifact_pool = self.config["item_pools"]["dimensional_artifacts"][tier]
        
        # Add one artifact
        artifact = self._select_from_pool(artifact_pool)
        if artifact:
            rewards.append(artifact)
            
        # Add crafting materials
        material_pool = self.config["item_pools"]["crafting_materials"]["common"]
        materials = self._select_from_pool(material_pool, count=2)
        rewards.extend(materials)
        
        return rewards
        
    def _determine_tier(self, player_level: int) -> str:
        """Determine reward tier based on player level."""
        if player_level >= 30:
            return "tier_3"
        elif player_level >= 15:
            return "tier_2"
        return "tier_1"
        
    def _select_from_pool(
        self,
        pool: List[Dict],
        count: int = 1
    ) -> List[Dict[str, any]]:
        """Select items from a pool based on weights."""
        selected = []
        total_weight = sum(item["weight"] for item in pool)
        
        for _ in range(count):
            roll = random.uniform(0, total_weight)
            current_weight = 0
            
            for item in pool:
                current_weight += item["weight"]
                if roll <= current_weight:
                    quantity = random.randint(
                        item["quantity"]["min"],
                        item["quantity"]["max"]
                    )
                    selected.append({
                        "id": item["id"],
                        "quantity": quantity
                    })
                    break
                    
        return selected
        
    def _calculate_reputation(
        self,
        faction: Optional[str],
        player_level: int,
        standing: str
    ) -> Dict[str, int]:
        """Calculate reputation rewards."""
        if not faction or faction not in self.config["reputation_tables"]:
            return {}
            
        rep_table = self.config["reputation_tables"][faction]
        base_rep = rep_table["base"]
        level_scaling = rep_table["level_scaling"]
        standing_mult = rep_table["standing_multipliers"][standing]
        
        amount = int(base_rep * (1 + level_scaling * player_level) * standing_mult)
        return {faction: amount}
        
    def _calculate_total_value(
        self,
        experience: int,
        currency: int,
        items: List[Dict],
        reputation: Dict[str, int]
    ) -> float:
        """Calculate total reward value for balancing purposes."""
        # These are example conversion rates
        value = (
            experience * 0.1 +  # Experience to value ratio
            currency +         # Direct currency value
            sum(50 for _ in items) +  # Simplified item value
            sum(rep * 0.2 for rep in reputation.values())  # Reputation to value
        )
        return round(value, 2)
        
    def analyze_reward_distribution(
        self,
        quest_type: str,
        level_range: range,
        iterations: int = 100
    ) -> Dict[str, any]:
        """Analyze reward distribution across levels."""
        results = {
            "levels": {},
            "summary": {
                "min_value": float('inf'),
                "max_value": 0,
                "avg_value": 0
            }
        }
        
        total_value = 0
        for level in level_range:
            level_results = []
            for _ in range(iterations):
                rewards = self.calculate_quest_rewards(
                    quest_type=quest_type,
                    player_level=level
                )
                level_results.append(rewards.total_value)
                
                # Update summary stats
                results["summary"]["min_value"] = min(
                    results["summary"]["min_value"],
                    rewards.total_value
                )
                results["summary"]["max_value"] = max(
                    results["summary"]["max_value"],
                    rewards.total_value
                )
                total_value += rewards.total_value
                
            results["levels"][level] = {
                "min": min(level_results),
                "max": max(level_results),
                "avg": sum(level_results) / len(level_results)
            }
            
        total_calculations = len(level_range) * iterations
        results["summary"]["avg_value"] = total_value / total_calculations
        
        return results

def main():
    """Main function demonstrating the reward calculator usage."""
    calculator = RewardCalculator()
    
    # Example calculations
    reward = calculator.calculate_quest_rewards(
        quest_type="main_story",
        player_level=10,
        difficulty="normal",
        faction="mystics"
    )
    
    print("\nReward Calculation Example:")
    print(f"Experience: {reward.experience}")
    print(f"Currency: {reward.currency}")
    print("Items:", reward.items)
    print("Reputation:", reward.reputation)
    print(f"Total Value: {reward.total_value}")
    
    # Distribution analysis
    analysis = calculator.analyze_reward_distribution(
        quest_type="main_story",
        level_range=range(1, 11)
    )
    
    print("\nReward Distribution Analysis:")
    print(f"Min Value: {analysis['summary']['min_value']}")
    print(f"Max Value: {analysis['summary']['max_value']}")
    print(f"Avg Value: {analysis['summary']['avg_value']}")

if __name__ == "__main__":
    main() 