"""Queue for passenger requests waiting for a vehicle."""

from collections import deque

from fleet_sim.models import PassengerRequest


class RequestQueue:
    """Store waiting passenger requests in arrival order."""

    def __init__(self) -> None:
        self._requests: deque[PassengerRequest] = deque()

    def add(self, request: PassengerRequest) -> None:
        """Add a request to the back of the queue."""

        self._requests.append(request)

    def pop(self) -> PassengerRequest:
        """Remove and return the oldest waiting request."""

        if not self._requests:
            raise IndexError("Cannot pop from an empty request queue.")

        return self._requests.popleft()

    def is_empty(self) -> bool:
        """Return whether the queue contains no requests."""

        return len(self._requests) == 0

    def __len__(self) -> int:
        """Return the number of waiting requests."""

        return len(self._requests)

    def drain(self) -> list[PassengerRequest]:
        """Remove and return all waiting requests in queue order."""

        requests = []

        while not self.is_empty():
            requests.append(self.pop())

        return requests
