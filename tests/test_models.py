"""Tests for simulation data models."""

import pytest

from fleet_sim.models import ChargingStation, ScheduledTrip


def test_charging_station_occupies_and_releases_port() -> None:
    station = ChargingStation(
        station_id=1,
        x=4,
        y=2,
        charging_rate=5,
        total_ports=2,
    )

    station.occupy_port()

    assert station.occupied_ports == 1
    assert station.available_ports == 1

    station.release_port()

    assert station.occupied_ports == 0
    assert station.available_ports == 2


def test_charging_station_rejects_vehicle_when_full() -> None:
    station = ChargingStation(
        station_id=1,
        x=4,
        y=2,
        charging_rate=5,
        total_ports=1,
    )

    station.occupy_port()

    with pytest.raises(
        ValueError,
        match="No charging ports are available.",
    ):
        station.occupy_port()

    assert station.occupied_ports == 1
    assert station.available_ports == 0


def test_charging_station_rejects_release_when_empty() -> None:
    station = ChargingStation(
        station_id=1,
        x=4,
        y=2,
        charging_rate=5,
        total_ports=2,
    )

    with pytest.raises(
        ValueError,
        match="No occupied charging ports can be released",
    ):
        station.release_port()

    assert station.occupied_ports == 0
    assert station.available_ports == 2


def test_scheduled_trip_stores_future_completion() -> None:
    trip = ScheduledTrip(
        vehicle_id=2,
        request_id=1,
        start_time=0,
        completion_time=19,
        final_x=-8,
        final_y=7,
        battery_used=19,
    )

    assert trip.vehicle_id == 2
    assert trip.request_id == 1
    assert trip.start_time == 0
    assert trip.completion_time == 19
    assert trip.final_x == -8
    assert trip.final_y == 7
    assert trip.battery_used == 19
