"""Tests for the waiting passenger request queue."""

import pytest

from fleet_sim.models import PassengerRequest
from fleet_sim.request_queue import RequestQueue


def make_request(request_id: int) -> PassengerRequest:
    return PassengerRequest(
        request_id=request_id,
        pickup_x=0,
        pickup_y=0,
        dropoff_x=1,
        dropoff_y=1,
    )


def test_request_queue_returns_oldest_request_first() -> None:
    queue = RequestQueue()

    queue.add(make_request(1))
    queue.add(make_request(2))
    queue.add(make_request(3))

    assert queue.pop().request_id == 1
    assert queue.pop().request_id == 2
    assert queue.pop().request_id == 3


def test_request_queue_is_empty() -> None:
    queue = RequestQueue()

    assert queue.is_empty()

    queue.add(make_request(1))

    assert not queue.is_empty()


def test_request_queue_reports_length() -> None:
    queue = RequestQueue()

    queue.add(make_request(1))
    queue.add(make_request(2))

    assert len(queue) == 2


def test_request_queue_rejects_pop_when_empty() -> None:
    queue = RequestQueue()

    with pytest.raises(
        IndexError,
        match="Cannot pop from an empty request queue.",
    ):
        queue.pop()


def test_request_queue_drain_returns_all_requests_in_order() -> None:
    queue = RequestQueue()

    queue.add(make_request(1))
    queue.add(make_request(2))
    queue.add(make_request(3))

    requests = queue.drain()

    assert [request.request_id for request in requests] == [1, 2, 3]
    assert queue.is_empty()


def test_request_queue_drain_empty_queue_returns_empty_list() -> None:
    queue = RequestQueue()

    requests = queue.drain()

    assert requests == []
