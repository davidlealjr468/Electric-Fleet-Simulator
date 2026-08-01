import pytest

from fleet_sim.charging import charge_vehicle

"""Tests for vehicle charging behavior."""


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


def test_charge_vehicle_rejects_nonpositive_charging_rate() -> None:
    with pytest.raises(
        ValueError,
        match="Charging rate must be greater than zero.",
    ):
        charge_vehicle(
            vehicle_battery=20,
            charging_target=80,
            charging_rate=0,
            current_time=5,
        )


def test_charge_vehicle_rejects_target_below_current_battery() -> None:
    with pytest.raises(
        ValueError,
        match="Charging target cannot be below the current battery level.",
    ):
        charge_vehicle(
            vehicle_battery=80,
            charging_target=60,
            charging_rate=5,
            current_time=10,
        )
