"""Tests for vehicle charging behavior."""

import pytest

from fleet_sim.charging import (
    charge_vehicle,
    complete_scheduled_charge,
    schedule_charge,
)
from fleet_sim.models import ChargingStation, Vehicle


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


def test_schedule_charge_reserves_port_and_vehicle() -> None:
    vehicle = Vehicle(
        vehicle_id=1,
        x=4,
        y=2,
        battery=52,
    )

    station = ChargingStation(
        station_id=1,
        x=4,
        y=2,
        charging_rate=6,
        total_ports=2,
    )

    charge = schedule_charge(
        vehicle=vehicle,
        station=station,
        start_time=10,
        target_battery=80,
    )

    assert charge.vehicle_id == 1
    assert charge.station_id == 1
    assert charge.start_time == 10
    assert charge.completion_time == 15
    assert charge.target_battery == 80

    assert vehicle.status == "charging"
    assert vehicle.available_time == 15

    assert station.occupied_ports == 1
    assert station.available_ports == 1


def test_schedule_charge_rejects_full_station() -> None:
    vehicle = Vehicle(
        vehicle_id=1,
        x=4,
        y=2,
        battery=40,
    )

    station = ChargingStation(
        station_id=1,
        x=4,
        y=2,
        charging_rate=5,
        total_ports=1,
        occupied_ports=1,
    )

    with pytest.raises(
        ValueError,
        match="No charging ports are available.",
    ):
        schedule_charge(
            vehicle=vehicle,
            station=station,
            start_time=10,
            target_battery=80,
        )

    assert vehicle.status == "idle"
    assert vehicle.available_time == 0
    assert station.occupied_ports == 1


def test_complete_scheduled_charge_updates_vehicle_and_station() -> None:
    vehicle = Vehicle(
        vehicle_id=1,
        x=4,
        y=2,
        battery=52,
    )

    station = ChargingStation(
        station_id=1,
        x=4,
        y=2,
        charging_rate=6,
        total_ports=2,
    )

    charge = schedule_charge(
        vehicle=vehicle,
        station=station,
        start_time=10,
        target_battery=80,
    )

    complete_scheduled_charge(
        charge=charge,
        vehicles=[vehicle],
        charging_stations=[station],
    )

    assert vehicle.battery == 80
    assert vehicle.status == "idle"
    assert vehicle.available_time == 15

    assert station.occupied_ports == 0
    assert station.available_ports == 2
