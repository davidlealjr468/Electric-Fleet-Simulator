import math

from fleet_sim.models import (
    ChargingStation, ScheduledCharge, ScheduledTrip
)
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

