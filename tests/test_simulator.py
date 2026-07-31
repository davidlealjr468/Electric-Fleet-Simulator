import pytest

from fleet_sim.distance import manhattan_distance
from fleet_sim.movement import move_vehicle_to
from fleet_sim.selection import find_nearest_charging_station


def test_find_nearest_charging_station():
    charging_stations = [
        (4, 2),
        (10, 8),
        (1, 9),
    ]

    station, distance = find_nearest_charging_station(
        0,
        0,
        charging_stations,
    )

    assert station == (4, 2)
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
    result = move_vehicle_to(
        vehicle_x=0,
        vehicle_y=0,
        target_x=7,
        target_y=6,
        current_time=0,
        vehicle_battery=100,
    )

    assert result == (7, 6, 13, 87)


def test_move_vehicle_left_and_down() -> None:
    result = move_vehicle_to(
        vehicle_x=8,
        vehicle_y=7,
        target_x=4,
        target_y=2,
        current_time=15,
        vehicle_battery=85,
    )

    assert result == (4, 2, 24, 76)


def test_move_vehicle_to_same_location() -> None:
    result = move_vehicle_to(
        vehicle_x=4,
        vehicle_y=2,
        target_x=4,
        target_y=2,
        current_time=10,
        vehicle_battery=80,
    )

    assert result == (4, 2, 10, 80)


def test_complete_passenger_trip() -> None:
    vehicle_x = 0
    vehicle_y = 0
    current_time = 0
    vehicle_battery = 100

    vehicle_x, vehicle_y, current_time, vehicle_battery = move_vehicle_to(
        vehicle_x,
        vehicle_y,
        7,
        6,
        current_time,
        vehicle_battery,
    )

    vehicle_x, vehicle_y, current_time, vehicle_battery = move_vehicle_to(
        vehicle_x,
        vehicle_y,
        8,
        7,
        current_time,
        vehicle_battery,
    )

    distance_to_charger = manhattan_distance(
        vehicle_x,
        vehicle_y,
        4,
        2,
    )

    assert vehicle_x == 8
    assert vehicle_y == 7
    assert current_time == 15
    assert vehicle_battery == 85
    assert distance_to_charger == 9
