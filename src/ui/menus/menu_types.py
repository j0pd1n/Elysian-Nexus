from enum import Enum
from typing import Dict, Any, Optional, List, Callable
from ..core.types import UIElement, UIState

class MenuState(Enum):
    OPEN = "open"
    CLOSED = "closed"
    TRANSITIONING = "transitioning"

class MenuItem(UIElement):
    def __init__(self,
                 id: str,
                 label: str,
                 action: Optional[Callable] = None,
                 icon: Optional[str] = None,
                 enabled: bool = True,
                 submenu: Optional['Menu'] = None):
        super().__init__(
            id=id,
            element_type="menu_item",
            state=UIState.ACTIVE if enabled else UIState.DISABLED,
            properties={
                "label": label,
                "icon": icon,
                "has_submenu": submenu is not None
            }
        )
        self.action = action
        self.submenu = submenu

class Menu(UIElement):
    def __init__(self,
                 id: str,
                 title: str,
                 items: List[MenuItem],
                 state: MenuState = MenuState.CLOSED,
                 position: Optional[Dict[str, int]] = None):
        super().__init__(
            id=id,
            element_type="menu",
            state=UIState.ACTIVE,
            properties={
                "title": title,
                "menu_state": state,
                "position": position or {"x": 0, "y": 0}
            },
            children=items
        )
        self.menu_state = state 