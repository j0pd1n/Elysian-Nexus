from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import random
from enum import Enum

class CombatPhase(Enum):
    # Basic Phases
    PREPARATION = "Preparation"  # 🔰
    ENGAGEMENT = "Engagement"    # ⚔️
    EXECUTION = "Execution"      # 🎯
    RESOLUTION = "Resolution"    # ✨
    
    # Advanced Phases
    POSITIONING = "Positioning"  # 👣

def resolve_combat(player, enemy):
    """Resolve combat between player and enemy."""
    # Combat logic...
    
    # After defeating the enemy
    if enemy.health <= 0:
        print(f"You have defeated the {enemy.name}!")
        drops = enemy.drops
        for drop in drops:
            player.inventory.add_item(drop)  # Assuming player has an inventory system
            print(f"You received: {drop.name}!")

[... rest of the file remains unchanged ...]