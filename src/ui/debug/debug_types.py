from enum import Enum
from typing import Dict, Any, Optional, List
from ..core.types import UIElement, UIState

class DebugState(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    MINIMAL = "minimal"
    VERBOSE = "verbose"

class DebugElement(UIElement):
    def __init__(self,
                 id: str,
                 debug_type: str,  # e.g., "fps", "memory", "position", etc.
                 value: Any,
                 update_interval: float = 1.0,  # Update interval in seconds
                 format_string: Optional[str] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            id=id,
            element_type="debug_element",
            state=UIState.ACTIVE,
            properties={
                "debug_type": debug_type,
                "value": value,
                "update_interval": update_interval,
                "format_string": format_string or "{}",
                **(properties or {})
            }
        )
        self.debug_type = debug_type
        self.value = value
        self.update_interval = update_interval
        self.format_string = format_string or "{}"
        self.last_update = 0  # Time of last update 