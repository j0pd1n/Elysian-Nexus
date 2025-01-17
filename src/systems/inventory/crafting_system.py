from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import random

class CraftingType(Enum):
    WEAPONSMITHING = "Weaponsmithing"  # ⚔️
    ARMORSMITHING = "Armorsmithing"    # 🛡️
    ALCHEMY = "Alchemy"                # ⚗️
    ENCHANTING = "Enchanting"          # ✨
    ARTIFICING = "Artificing"          # 🔮
    RUNECRAFTING = "Runecrafting"      # 📜
    JEWELCRAFTING = "Jewelcrafting"    # 💎

[... rest of the file remains unchanged ...] 