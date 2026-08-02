"""Priority queue for scheduled fleet events."""

import heapq

from fleet_sim.models import SimulationEvent


class EventQueue:
    """Store simulation events in completion-time order."""

    def __init__(self) -> None:
        self._events: list[tuple[int, int, SimulationEvent]] = []
        self._counter = 0

    def push(self, event: SimulationEvent) -> None:
        """Add a simulation event to the queue."""

        heapq.heappush(
            self._events,
            (
                event.completion_time,
                self._counter,
                event,
            ),
        )

        self._counter += 1

    def pop(self) -> SimulationEvent:
        """Remove and return the earliest simulation event."""

        if not self._events:
            raise IndexError("Cannot pop from an empty event queue.")

        _, _, event = heapq.heappop(self._events)
        return event

    def peek(self) -> SimulationEvent:
        """Return the earliest event without removing it."""

        if not self._events:
            raise IndexError("Cannot peek at an empty event queue.")

        return self._events[0][2]

    def pop_ready(self, current_time: int) -> list[SimulationEvent]:
        """Remove all events completed by the current time."""

        ready_events = []

        while not self.is_empty() and self.peek().completion_time <= current_time:
            ready_events.append(self.pop())

        return ready_events

    def is_empty(self) -> bool:
        """Return whether the queue contains no events."""

        return len(self._events) == 0

    def __len__(self) -> int:
        """Return the number of scheduled events."""

        return len(self._events)
