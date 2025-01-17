from enum import Enum
from typing import Dict, Any, Optional, List, Callable

class UIState(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    HIDDEN = "hidden"
    DISABLED = "disabled"

class UIEvent(Enum):
    CLICK = "click"
    HOVER = "hover"
    FOCUS = "focus"
    BLUR = "blur"
    KEY_PRESS = "key_press"
    VALUE_CHANGE = "value_change"

class UIElement:
    def __init__(self, 
                 id: str,
                 element_type: str,
                 state: UIState = UIState.ACTIVE,
                 properties: Optional[Dict[str, Any]] = None,
                 children: Optional[List['UIElement']] = None,
                 event_handlers: Optional[Dict[UIEvent, Callable]] = None):
        self.id = id
        self.element_type = element_type
        self.state = state
        self.properties = properties or {}
        self.children = children or []
        self.event_handlers = event_handlers or {} 