from collections import defaultdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set
from queue import PriorityQueue
import threading
import logging
import uuid

from .event_types import GameEvent, EventPriority, EventCategory

logger = logging.getLogger(__name__)

EventHandler = Callable[[GameEvent], None]

class EventHistory:
    """Tracks and manages event history."""
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.events: List[GameEvent] = []
        self._lock = threading.Lock()

    def add_event(self, event: GameEvent) -> None:
        """Add an event to history with thread safety."""
        with self._lock:
            self.events.append(event)
            if len(self.events) > self.max_history:
                self.events.pop(0)

    def get_events(self, category: Optional[EventCategory] = None,
                  start_time: Optional[datetime] = None,
                  end_time: Optional[datetime] = None) -> List[GameEvent]:
        """Retrieve events with optional filtering."""
        with self._lock:
            filtered_events = self.events[:]

        if category:
            filtered_events = [e for e in filtered_events if e.category == category]
        if start_time:
            filtered_events = [e for e in filtered_events if e.timestamp >= start_time]
        if end_time:
            filtered_events = [e for e in filtered_events if e.timestamp <= end_time]

        return filtered_events

    def clear_history(self) -> None:
        """Clear event history."""
        with self._lock:
            self.events.clear()

class EventDispatcher:
    """Manages event dispatching with priority handling."""
    def __init__(self):
        self._handlers: Dict[EventCategory, Dict[EventPriority, Set[EventHandler]]] = defaultdict(
            lambda: defaultdict(set)
        )
        self._event_queue: PriorityQueue = PriorityQueue()
        self._history = EventHistory()
        self._running = False
        self._dispatch_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def subscribe(self, handler: EventHandler, category: EventCategory,
                 priority: EventPriority = EventPriority.NORMAL) -> None:
        """Subscribe a handler to events of a specific category and priority."""
        with self._lock:
            self._handlers[category][priority].add(handler)
            logger.debug(f"Handler {handler.__name__} subscribed to {category} with {priority} priority")

    def unsubscribe(self, handler: EventHandler, category: EventCategory,
                    priority: EventPriority = EventPriority.NORMAL) -> None:
        """Unsubscribe a handler from events."""
        with self._lock:
            if category in self._handlers and priority in self._handlers[category]:
                self._handlers[category][priority].discard(handler)
                logger.debug(f"Handler {handler.__name__} unsubscribed from {category}")

    def dispatch(self, event: GameEvent) -> None:
        """Dispatch an event to the priority queue."""
        event.event_id = str(uuid.uuid4())
        event.timestamp = datetime.now()
        # Priority queue orders by first element of tuple
        # Negative priority value ensures higher priority events are processed first
        self._event_queue.put((-event.priority.value, event))
        logger.debug(f"Event {event.event_id} of type {event.category} queued for dispatch")

    def start(self) -> None:
        """Start the event dispatch thread."""
        if not self._running:
            self._running = True
            self._dispatch_thread = threading.Thread(target=self._dispatch_loop, daemon=True)
            self._dispatch_thread.start()
            logger.info("Event dispatcher started")

    def stop(self) -> None:
        """Stop the event dispatch thread."""
        self._running = False
        if self._dispatch_thread:
            self._dispatch_thread.join()
            logger.info("Event dispatcher stopped")

    def _dispatch_loop(self) -> None:
        """Main event dispatch loop."""
        while self._running:
            try:
                if not self._event_queue.empty():
                    _, event = self._event_queue.get(timeout=0.1)
                    self._process_event(event)
                    self._event_queue.task_done()
            except Exception as e:
                logger.error(f"Error in dispatch loop: {e}")

    def _process_event(self, event: GameEvent) -> None:
        """Process a single event through all relevant handlers."""
        try:
            # Process handlers in priority order
            for priority in sorted(EventPriority, key=lambda p: p.value, reverse=True):
                if handlers := self._handlers[event.category].get(priority):
                    for handler in handlers:
                        try:
                            handler(event)
                        except Exception as e:
                            logger.error(f"Error in handler {handler.__name__}: {e}")

            event.handled = True
            self._history.add_event(event)
            logger.debug(f"Event {event.event_id} processed successfully")

        except Exception as e:
            logger.error(f"Error processing event {event.event_id}: {e}")

    def get_history(self, category: Optional[EventCategory] = None,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None) -> List[GameEvent]:
        """Retrieve event history with optional filtering."""
        return self._history.get_events(category, start_time, end_time)

    def clear_history(self) -> None:
        """Clear event history."""
        self._history.clear_history()

    @property
    def pending_events(self) -> int:
        """Get the number of pending events."""
        return self._event_queue.qsize()

    def get_handler_count(self, category: EventCategory) -> Dict[EventPriority, int]:
        """Get the number of handlers for each priority level of a category."""
        return {
            priority: len(handlers)
            for priority, handlers in self._handlers[category].items()
        } 