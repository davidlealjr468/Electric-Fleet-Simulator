"""Priority queue for scheduled fleet events."""

import heapq

from fleet_sim.models import ScheduledTrip


class EventQueue:
    """Store scheduled trips in completion-time order."""

    def __init__(self) -> None:
        self._events: list[tuple[int, int, ScheduledTrip]] = []
        self._counter = 0

    def push(self, trip: ScheduledTrip) -> None:
        """Add a scheduled trip to the queue."""

        heapq.heappush(
            self._events,
            (
                trip.completion_time,
                self._counter,
                trip,
            ),
        )

        self._counter += 1

    def pop(self) -> ScheduledTrip:
        """Remove and return the earliest scheduled trip."""

        if not self._events:
            raise IndexError("Cannot pop from an empty event queue.")

        _, _, trip = heapq.heappop(self._events)
        return trip

    def peek(self) -> ScheduledTrip:
        """Return the earliest scheduled trip without removing it."""

        if not self._events:
            raise IndexError("Cannot peek at an empty event queue.")

        return self._events[0][2]

    def is_empty(self) -> bool:
        """Return whether the queue contains no events."""

        return len(self._events) == 0

    def __len__(self) -> int:
        """Return the number of scheduled events."""

        return len(self._events)

    def pop_ready(self, current_time: int) -> list[ScheduledTrip]:
        """Remove and return all trips completed by the current time."""

        ready_trips = []

        while not self.is_empty() and self.peek().completion_time <= current_time:
            ready_trips.append(self.pop())

        return ready_trips
