"""Tests for the scheduled event priority queue."""

import pytest

from fleet_sim.event_queue import EventQueue
from fleet_sim.models import ScheduledCharge, ScheduledTrip


def make_trip(
    request_id: int,
    completion_time: int,
) -> ScheduledTrip:
    return ScheduledTrip(
        vehicle_id=request_id,
        request_id=request_id,
        start_time=0,
        completion_time=completion_time,
        final_x=0,
        final_y=0,
        battery_used=1,
    )


def test_event_queue_returns_earliest_trip_first() -> None:
    queue = EventQueue()

    queue.push(make_trip(request_id=1, completion_time=20))
    queue.push(make_trip(request_id=2, completion_time=5))
    queue.push(make_trip(request_id=3, completion_time=12))

    assert queue.pop().request_id == 2
    assert queue.pop().request_id == 3
    assert queue.pop().request_id == 1


def test_event_queue_peek_does_not_remove_trip() -> None:
    queue = EventQueue()

    queue.push(make_trip(request_id=1, completion_time=10))

    trip = queue.peek()

    assert trip.request_id == 1
    assert len(queue) == 1


def test_event_queue_is_empty() -> None:
    queue = EventQueue()

    assert queue.is_empty()

    queue.push(make_trip(request_id=1, completion_time=10))

    assert not queue.is_empty()


def test_event_queue_preserves_order_for_equal_completion_times() -> None:
    queue = EventQueue()

    queue.push(make_trip(request_id=1, completion_time=10))
    queue.push(make_trip(request_id=2, completion_time=10))

    assert queue.pop().request_id == 1
    assert queue.pop().request_id == 2


def test_event_queue_rejects_pop_when_empty() -> None:
    queue = EventQueue()

    with pytest.raises(
        IndexError,
        match="Cannot pop from an empty event queue.",
    ):
        queue.pop()


def test_event_queue_returns_all_ready_trips() -> None:
    queue = EventQueue()

    queue.push(make_trip(request_id=1, completion_time=5))
    queue.push(make_trip(request_id=2, completion_time=12))
    queue.push(make_trip(request_id=3, completion_time=20))

    ready_trips = queue.pop_ready(current_time=15)

    assert [trip.request_id for trip in ready_trips] == [1, 2]
    assert len(queue) == 1
    assert queue.peek().request_id == 3


def test_event_queue_returns_no_trips_before_completion() -> None:
    queue = EventQueue()

    queue.push(make_trip(request_id=1, completion_time=10))

    ready_trips = queue.pop_ready(current_time=5)

    assert ready_trips == []
    assert len(queue) == 1


def test_event_queue_includes_trip_completed_at_current_time() -> None:
    queue = EventQueue()

    queue.push(make_trip(request_id=1, completion_time=10))

    ready_trips = queue.pop_ready(current_time=10)

    assert len(ready_trips) == 1
    assert ready_trips[0].request_id == 1
    assert queue.is_empty()


def test_event_queue_orders_trip_and_charge_events() -> None:
    queue = EventQueue()

    trip = ScheduledTrip(
        vehicle_id=1,
        request_id=1,
        start_time=0,
        completion_time=12,
        final_x=5,
        final_y=5,
        battery_used=10,
    )

    charge = ScheduledCharge(
        vehicle_id=2,
        station_id=1,
        start_time=0,
        completion_time=8,
        target_battery=80,
    )

    queue.push(trip)
    queue.push(charge)

    first_event = queue.pop()
    second_event = queue.pop()

    assert first_event is charge
    assert second_event is trip
