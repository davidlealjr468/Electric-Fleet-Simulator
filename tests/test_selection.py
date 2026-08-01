"""Tests for vehicle and charging-station selection."""

import pytest

from fleet_sim.models import ChargingStation, Vehicle
from fleet_sim.selection import (
    find_nearest_available_vehicle,
    find_nearest_charging_station,
)


def test_find_nearest_charging_station() -> None:
    charging_stations = [
        ChargingStation(
            station_id=1,
            x=4,
            y=2,
            charging_rate=5,
            total_ports=2,
        ),
        ChargingStation(
            station_id=2,
            x=10,
            y=8,
            charging_rate=8,
            total_ports=4,
        ),
        ChargingStation(
            station_id=3,
            x=1,
            y=9,
            charging_rate=6,
            total_ports=1,
        ),
    ]

    station, distance = find_nearest_charging_station(
        0,
        0,
        charging_stations,
    )

    assert station.station_id == 1
    assert station.x == 4
    assert station.y == 2
    assert distance == 6


def test_find_nearest_charging_station_requires_stations() -> None:
    with pytest.raises(
        ValueError,
        match="At least one charging station is required.",
    ):
        find_nearest_charging_station(
            0,
            0,
            [],
        )


def test_find_nearest_available_vehicle() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=10,
        ),
        Vehicle(
            vehicle_id=2,
            x=5,
            y=5,
            battery=15,
        ),
        Vehicle(
            vehicle_id=3,
            x=-4,
            y=3,
            battery=20,
        ),
    ]

    vehicle, distance = find_nearest_available_vehicle(
        pickup_x=7,
        pickup_y=6,
        vehicles=vehicles,
    )

    assert vehicle.vehicle_id == 2
    assert vehicle.x == 5
    assert vehicle.y == 5
    assert distance == 3


def test_find_nearest_available_vehicle_skips_busy_vehicle() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=6,
            y=6,
            battery=80,
            status="with_passenger",
        ),
        Vehicle(
            vehicle_id=2,
            x=5,
            y=5,
            battery=70,
        ),
        Vehicle(
            vehicle_id=3,
            x=0,
            y=0,
            battery=100,
        ),
    ]

    vehicle, distance = find_nearest_available_vehicle(
        pickup_x=7,
        pickup_y=6,
        vehicles=vehicles,
    )

    assert vehicle.vehicle_id == 2
    assert distance == 3


def test_find_nearest_available_vehicle_requires_idle_vehicle() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=80,
            status="with_passenger",
        ),
        Vehicle(
            vehicle_id=2,
            x=5,
            y=5,
            battery=70,
            status="charging",
        ),
        Vehicle(
            vehicle_id=3,
            x=-4,
            y=3,
            battery=60,
            status="to_charger",
        ),
    ]

    with pytest.raises(
        ValueError,
        match="No available vehicles were found.",
    ):
        find_nearest_available_vehicle(
            pickup_x=7,
            pickup_y=6,
            vehicles=vehicles,
        )


def test_find_nearest_available_vehicle_skips_low_battery_vehicle() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=6,
            y=6,
            battery=0,
        ),
        Vehicle(
            vehicle_id=2,
            x=5,
            y=5,
            battery=10,
        ),
    ]

    vehicle, distance = find_nearest_available_vehicle(
        pickup_x=7,
        pickup_y=6,
        vehicles=vehicles,
    )

    assert vehicle.vehicle_id == 2
    assert distance == 3
