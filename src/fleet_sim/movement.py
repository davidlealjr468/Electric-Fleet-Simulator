"""Vehicle movement behavior."""


def move_vehicle_to(
    vehicle_x,
    vehicle_y,
    target_x,
    target_y,
    current_time,
    vehicle_battery,
):
    """Move a vehicle and update its position, time, and battery."""

    while target_x > vehicle_x:
        vehicle_x += 1
        current_time += 1
        vehicle_battery -= 1
        print(f"Time {current_time}: vehicle moved right to ({vehicle_x}, {vehicle_y})")

    while target_x < vehicle_x:
        vehicle_x -= 1
        current_time += 1
        vehicle_battery -= 1
        print(f"Time {current_time}: vehicle moved left to ({vehicle_x}, {vehicle_y})")

    while target_y > vehicle_y:
        vehicle_y += 1
        current_time += 1
        vehicle_battery -= 1
        print(f"Time {current_time}: vehicle moved up to ({vehicle_x}, {vehicle_y})")

    while target_y < vehicle_y:
        vehicle_y -= 1
        current_time += 1
        vehicle_battery -= 1
        print(f"Time {current_time}: vehicle moved down to ({vehicle_x}, {vehicle_y})")

    return vehicle_x, vehicle_y, current_time, vehicle_battery
