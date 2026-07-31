"""Vehicle charging behavior."""


def charge_vehicle(
    vehicle_battery,
    charging_target,
    charging_rate,
    current_time,
):
    """Charge a vehicle to a target level and update simulation time."""

    while vehicle_battery < charging_target:
        vehicle_battery = min(
            vehicle_battery + charging_rate,
            charging_target,
        )

        current_time += 1
        print(f"Time {current_time}: vehicle charged to {vehicle_battery}")

    return vehicle_battery, current_time
