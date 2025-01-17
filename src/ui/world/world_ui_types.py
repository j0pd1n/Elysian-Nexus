from enum import Enum
from typing import Dict, Any, Optional, List, Tuple
from ..core.types import UIElement, UIState

class WorldUIState(Enum):
    EXPLORING = "exploring"
    COMBAT = "combat"
    DIALOGUE = "dialogue"
    CUTSCENE = "cutscene"

class WorldUIElement(UIElement):
    def __init__(self,
                 id: str,
                 element_type: str,
                 position: Tuple[float, float, float],  # 3D position (x, y, z)
                 world_space: bool = True,  # Whether element is in world space or screen space
                 scale: float = 1.0,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            id=id,
            element_type=element_type,
            state=UIState.ACTIVE,
            properties={
                "position": position,
                "world_space": world_space,
                "scale": scale,
                **(properties or {})
            }
        )
        self.position = position
        self.world_space = world_space
        self.scale = scale 