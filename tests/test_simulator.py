import pytest

from fleet_sim.distance import manhattan_distance
from fleet_sim.models import ChargingStation, Vehicle
from fleet_sim.movement import move_vehicle_to
from fleet_sim.selection import find_nearest_charging_station


def test_find_nearest_charging_station():
    charging_stations = [
        ChargingStation(
            station_id=1,
            x=4,
            y=2,
            charging_rate=5,
        ),
        ChargingStation(
            station_id=2,
            x=10,
            y=8,
            charging_rate=8,
        ),
        ChargingStation(
            station_id=3,
            x=1,
            y=9,
            charging_rate=6,
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


def test_find_nearest_charging_station_requires_stations():
    with pytest.raises(
        ValueError,
        match="At least one charging station is required.",
    ):
        find_nearest_charging_station(
            0,
            0,
            [],
        )


def test_manhattan_distance() -> None:
    distance = manhattan_distance(0, 0, 7, 6)

    assert distance == 13


def test_manhattan_distance_with_negative_coordinates() -> None:
    distance = manhattan_distance(-2, -3, 4, 5)

    assert distance == 14


def test_move_vehicle_right_and_up() -> None:
    vehicle = Vehicle(vehicle_id=1, x=0, y=0, battery=100)
    current_time = move_vehicle_to(
        vehicle=vehicle,
        target_x=7,
        target_y=6,
        current_time=0,
    )

    assert vehicle.x == 7
    assert vehicle.y == 6
    assert vehicle.battery == 87
    assert current_time == 13


def test_move_vehicle_left_and_down() -> None:
    vehicle = Vehicle(vehicle_id=1, x=8, y=7, battery=100)
    current_time = move_vehicle_to(
        vehicle=vehicle,
        target_x=4,
        target_y=2,
        current_time=15,
    )

    assert vehicle.x == 4
    assert vehicle.y == 2
    assert vehicle.battery == 91
    assert current_time == 24


def test_move_vehicle_to_same_location() -> None:
    vehicle = Vehicle(vehicle_id=1, x=4, y=2, battery=80)
    current_time = move_vehicle_to(
        vehicle=vehicle,
        target_x=4,
        target_y=2,
        current_time=10,
    )

    assert vehicle.x == 4
    assert vehicle.y == 2
    assert vehicle.battery == 80
    assert current_time == 10


def test_complete_passenger_trip() -> None:
    vehicle = Vehicle(vehicle_id=1, x=0, y=0, battery=100)

    current_time = move_vehicle_to(
        vehicle=vehicle,
        target_x=7,
        target_y=6,
        current_time=0,
    )

    current_time = move_vehicle_to(
        vehicle=vehicle,
        target_x=8,
        target_y=7,
        current_time=current_time,
    )

    distance_to_charger = manhattan_distance(
        vehicle.x,
        vehicle.y,
        4,
        2,
    )

    assert vehicle.x == 8
    assert vehicle.y == 7
    assert current_time == 15
    assert vehicle.battery == 85
    assert distance_to_charger == 9
