from fleet_sim.models import Vehicle

"""Vehicle movement behavior."""


def move_vehicle_to(
    vehicle: Vehicle,
    target_x: int,
    target_y: int,
    current_time: int,
) -> int:
    """Move a vehicle and update its position, time, and battery."""

    while target_x > vehicle.x:
        vehicle.x += 1
        current_time += 1
        vehicle.battery -= 1
        print(f"Time {current_time}: vehicle moved right to ({vehicle.x}, {vehicle.y})")

    while target_x < vehicle.x:
        vehicle.x -= 1
        current_time += 1
        vehicle.battery -= 1
        print(f"Time {current_time}: vehicle moved left to ({vehicle.x}, {vehicle.y})")

    while target_y > vehicle.y:
        vehicle.y += 1
        current_time += 1
        vehicle.battery -= 1
        print(f"Time {current_time}: vehicle moved up to ({vehicle.x}, {vehicle.y})")

    while target_y < vehicle.y:
        vehicle.y -= 1
        current_time += 1
        vehicle.battery -= 1
        print(f"Time {current_time}: vehicle moved down to ({vehicle.x}, {vehicle.y})")

    return current_time
