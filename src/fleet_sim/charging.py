import math

from fleet_sim.models import ChargingStation, ScheduledCharge, Vehicle

"""Vehicle charging behavior."""


def charge_vehicle(
    vehicle_battery,
    charging_target,
    charging_rate,
    current_time,
):
    """Charge a vehicle to a target level and update simulation time."""

    if charging_rate <= 0:
        raise ValueError("Charging rate must be greater than zero.")

    if charging_target < vehicle_battery:
        raise ValueError("Charging target cannot be below the current battery level.")
    while vehicle_battery < charging_target:
        vehicle_battery = min(
            vehicle_battery + charging_rate,
            charging_target,
        )

        current_time += 1
        print(f"Time {current_time}: vehicle charged to {vehicle_battery}")

    return vehicle_battery, current_time


def calculate_charging_duration(
    current_battery: int,
    target_battery: int,
    charging_rate: int,
) -> int:
    """Calulate the nmber of time steps needed to reach a target battery."""
    if charging_rate <= 0:
        raise ValueError("Charging rate must be greater than zero.")

    if target_battery < current_battery:
        raise ValueError("Target battery cannot be below the current battery level.")

    battery_needed = target_battery - current_battery
    duration = math.ceil(battery_needed / charging_rate)
    return duration


def schedule_charge(
    vehicle: Vehicle,
    station: ChargingStation,
    start_time: int,
    target_battery: int,
) -> ScheduledCharge:
    """Reserve a charging port and schedule a future charge completion."""

    if station.available_ports <= 0:
        raise ValueError("No charging ports are available.")

    charging_duration = calculate_charging_duration(
        current_battery=vehicle.battery,
        target_battery=target_battery,
        charging_rate=station.charging_rate,
    )

    station.occupy_port()

    vehicle.status = "charging"
    vehicle.available_time = start_time + charging_duration

    return ScheduledCharge(
        vehicle_id=vehicle.vehicle_id,
        station_id=station.station_id,
        start_time=start_time,
        completion_time=start_time + charging_duration,
        target_battery=target_battery,
    )


def complete_scheduled_charge(
    charge: ScheduledCharge,
    vehicles: list[Vehicle],
    charging_stations: list[ChargingStation],
) -> None:
    """Complete a charging event and release the station port."""

    vehicle = next(
        vehicle for vehicle in vehicles if vehicle.vehicle_id == charge.vehicle_id
    )

    station = next(
        station
        for station in charging_stations
        if station.station_id == charge.station_id
    )

    vehicle.battery = charge.target_battery
    vehicle.status = "idle"
    vehicle.available_time = charge.completion_time

    station.release_port()
