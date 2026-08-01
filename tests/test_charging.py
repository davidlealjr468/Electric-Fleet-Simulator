"""Tests for vehicle charging behavior."""

from fleet_sim.charging import charge_vehicle


def test_charge_vehicle_to_target() -> None:
    battery, current_time = charge_vehicle(
        vehicle_battery=4,
        charging_target=80,
        charging_rate=5,
        current_time=6,
    )

    assert battery == 80
    assert current_time == 22


def test_charge_vehicle_does_not_exceed_target() -> None:
    battery, current_time = charge_vehicle(
        vehicle_battery=79,
        charging_target=80,
        charging_rate=5,
        current_time=10,
    )

    assert battery == 80
    assert current_time == 11


def test_charge_vehicle_when_already_at_target() -> None:
    battery, current_time = charge_vehicle(
        vehicle_battery=80,
        charging_target=80,
        charging_rate=5,
        current_time=10,
    )

    assert battery == 80
    assert current_time == 10
