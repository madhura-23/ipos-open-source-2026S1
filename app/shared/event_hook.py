"""
Minimal event hook interface for process and task updates.

Provides a small observer-style hook that service logic can call
when important actions happen, without depending on FastAPI, MCP,
or LLM code. Not a full event system — just a clean extension point.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ProcessEvent:
    """
    A simple, domain-neutral event describing a process or task update.

    Attributes:
        name:      Short label for the event e.g. "task.completed"
        payload:   Optional key/value context about the event.
        timestamp: UTC time the event was created.
    """
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class EventHook(ABC):
    """
    Abstract base for observer-style event hooks.

    Service logic calls ``handle(event)`` when an important action occurs.
    Concrete implementations can log, notify, audit, or summarise — all
    without the service knowing the details.

    Deliberately kept framework-free: no FastAPI, MCP, or LLM imports.
    """

    @abstractmethod
    def handle(self, event: ProcessEvent) -> None:
        """
        React to a process event.

        Args:
            event: The event describing what happened.
        """


class NullEventHook(EventHook):
    """
    No-op default implementation of EventHook.

    Safe to use anywhere a hook is required but nothing needs wiring yet.
    Replace with a real implementation when the feature is needed.
    """

    def handle(self, event: ProcessEvent) -> None:
        pass  # intentional no-op
