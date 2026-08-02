"""Tests for trip scheduling."""

from fleet_sim.models import PassengerRequest, Vehicle
from fleet_sim.scheduling import calculate_trip_duration


def test_calculate_trip_duration() -> None:
    vehicle = Vehicle(
        vehicle_id=2,
        x=5,
        y=5,
        battery=70,
    )

    request = PassengerRequest(
        request_id=1,
        pickup_x=7,
        pickup_y=6,
        dropoff_x=-8,
        dropoff_y=7,
        arrival_time=0,
    )

    duration = calculate_trip_duration(vehicle, request)

    assert duration == 19
