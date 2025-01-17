import logging
import traceback
import sys
import json
from typing import Dict, Any, Optional, Callable
from enum import Enum
from datetime import datetime
import os

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    SYSTEM = "system"
    GAMEPLAY = "gameplay"
    SAVE = "save"
    STATE = "state"
    COMBAT = "combat"
    DIALOGUE = "dialogue"
    NETWORK = "network"
    RESOURCE = "resource"

class GameError(Exception):
    def __init__(self, message: str, severity: ErrorSeverity, category: ErrorCategory):
        self.message = message
        self.severity = severity
        self.category = category
        self.timestamp = datetime.now()
        super().__init__(self.message)

class ErrorHandler:
    def __init__(self):
        self.log_directory = "logs"
        self.error_handlers: Dict[ErrorCategory, Dict[ErrorSeverity, Callable]] = {}
        self.error_history: List[Dict[str, Any]] = []
        self.max_history = 100
        
        # Setup logging
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
            
        self.logger = self._setup_logger()
        
        # Initialize default error handlers
        self._initialize_default_handlers()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("ElysianNexus")
        logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(
            os.path.join(self.log_directory, f"game_{datetime.now().strftime('%Y%m%d')}.log")
        )
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger

    def _initialize_default_handlers(self):
        """Initialize default error handlers for different categories and severities"""
        # System errors
        self.register_handler(
            ErrorCategory.SYSTEM,
            ErrorSeverity.CRITICAL,
            self._handle_critical_system_error
        )
        
        # Save errors
        self.register_handler(
            ErrorCategory.SAVE,
            ErrorSeverity.HIGH,
            self._handle_save_error
        )
        
        # State errors
        self.register_handler(
            ErrorCategory.STATE,
            ErrorSeverity.HIGH,
            self._handle_state_error
        )
        
        # Combat errors
        self.register_handler(
            ErrorCategory.COMBAT,
            ErrorSeverity.MEDIUM,
            self._handle_combat_error
        )

    def register_handler(
        self,
        category: ErrorCategory,
        severity: ErrorSeverity,
        handler: Callable
    ):
        """Register a custom error handler"""
        if category not in self.error_handlers:
            self.error_handlers[category] = {}
        self.error_handlers[category][severity] = handler

    def handle_error(
        self,
        error: Exception,
        severity: ErrorSeverity,
        category: ErrorCategory,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Handle an error with the appropriate handler"""
        try:
            # Log error
            self._log_error(error, severity, category, context)
            
            # Add to history
            self._add_to_history(error, severity, category, context)
            
            # Find and execute handler
            handler = self._get_handler(category, severity)
            if handler:
                return handler(error, context)
                
            # Default handling
            return self._default_handler(error, severity, category, context)
            
        except Exception as e:
            # Meta-error handling
            self.logger.critical(f"Error in error handler: {str(e)}")
            return False

    def _log_error(
        self,
        error: Exception,
        severity: ErrorSeverity,
        category: ErrorCategory,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log error details"""
        error_data = {
            "message": str(error),
            "severity": severity.value,
            "category": category.value,
            "timestamp": datetime.now().isoformat(),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        if severity == ErrorSeverity.CRITICAL:
            self.logger.critical(json.dumps(error_data))
        elif severity == ErrorSeverity.HIGH:
            self.logger.error(json.dumps(error_data))
        elif severity == ErrorSeverity.MEDIUM:
            self.logger.warning(json.dumps(error_data))
        else:
            self.logger.info(json.dumps(error_data))

    def _add_to_history(
        self,
        error: Exception,
        severity: ErrorSeverity,
        category: ErrorCategory,
        context: Optional[Dict[str, Any]] = None
    ):
        """Add error to history"""
        error_data = {
            "message": str(error),
            "severity": severity.value,
            "category": category.value,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        self.error_history.append(error_data)
        
        # Maintain history size
        if len(self.error_history) > self.max_history:
            self.error_history.pop(0)

    def _get_handler(
        self,
        category: ErrorCategory,
        severity: ErrorSeverity
    ) -> Optional[Callable]:
        """Get the appropriate error handler"""
        return self.error_handlers.get(category, {}).get(severity)

    def _default_handler(
        self,
        error: Exception,
        severity: ErrorSeverity,
        category: ErrorCategory,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Default error handling behavior"""
        self.logger.warning(f"No specific handler for {category.value} - {severity.value}")
        
        if severity == ErrorSeverity.CRITICAL:
            self._handle_critical_error(error, context)
            return False
            
        return True

    def _handle_critical_system_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Handle critical system errors"""
        self.logger.critical("Critical system error occurred!")
        self.logger.critical(f"Error: {str(error)}")
        self.logger.critical(f"Context: {json.dumps(context or {})}")
        
        # Attempt to save game state
        if context and "game_state" in context:
            self._emergency_save(context["game_state"])
            
        return False

    def _handle_save_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Handle save system errors"""
        self.logger.error(f"Save error: {str(error)}")
        
        # Attempt backup save
        if context and "game_state" in context:
            return self._backup_save(context["game_state"])
            
        return False

    def _handle_state_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Handle state management errors"""
        self.logger.error(f"State error: {str(error)}")
        
        # Attempt state recovery
        if context and "state_manager" in context:
            return self._recover_state(context["state_manager"])
            
        return False

    def _handle_combat_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Handle combat system errors"""
        self.logger.warning(f"Combat error: {str(error)}")
        
        # Attempt to stabilize combat
        if context and "combat_system" in context:
            return self._stabilize_combat(context["combat_system"])
            
        return True

    def _emergency_save(self, game_state: Dict[str, Any]) -> bool:
        """Perform emergency save of game state"""
        try:
            emergency_save_path = os.path.join(
                self.log_directory,
                f"emergency_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            with open(emergency_save_path, "w") as f:
                json.dump(game_state, f, indent=4)
                
            self.logger.info(f"Emergency save created at: {emergency_save_path}")
            return True
            
        except Exception as e:
            self.logger.critical(f"Failed to create emergency save: {str(e)}")
            return False

    def _backup_save(self, game_state: Dict[str, Any]) -> bool:
        """Create backup save file"""
        try:
            backup_path = os.path.join(
                self.log_directory,
                f"backup_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            with open(backup_path, "w") as f:
                json.dump(game_state, f, indent=4)
                
            self.logger.info(f"Backup save created at: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create backup save: {str(e)}")
            return False

    def _recover_state(self, state_manager: Any) -> bool:
        """Attempt to recover game state"""
        try:
            # Attempt to rollback to last stable state
            if hasattr(state_manager, "rollback_state"):
                return state_manager.rollback_state()
                
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to recover state: {str(e)}")
            return False

    def _stabilize_combat(self, combat_system: Any) -> bool:
        """Attempt to stabilize combat system"""
        try:
            # Reset combat to neutral state
            if hasattr(combat_system, "reset_combat"):
                return combat_system.reset_combat()
                
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to stabilize combat: {str(e)}")
            return False

    def get_error_history(
        self,
        category: Optional[ErrorCategory] = None,
        severity: Optional[ErrorSeverity] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get filtered error history"""
        history = self.error_history
        
        if category:
            history = [e for e in history if e["category"] == category.value]
            
        if severity:
            history = [e for e in history if e["severity"] == severity.value]
            
        if limit:
            history = history[-limit:]
            
        return history

    def clear_history(self):
        """Clear error history"""
        self.error_history.clear()

    def export_logs(self, export_path: str) -> bool:
        """Export logs to file"""
        try:
            with open(export_path, "w") as f:
                json.dump(self.error_history, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Failed to export logs: {str(e)}")
            return False 