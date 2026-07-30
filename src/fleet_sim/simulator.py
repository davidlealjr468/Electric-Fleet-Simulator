"""Base electric fleet simulator."""


def move_vehicle_to(
    vehicle_x,
    vehicle_y,
    target_x,
    target_y,
    current_time,
    vehicle_battery,
):
    """Move a vehicle and update position, time, and battery."""

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


def manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)


def main() -> None:
    """Run the base electric fleet simulation."""
    current_time = 0

    vehicle_x = 0
    vehicle_y = 0
    vehicle_id = 1
    vehicle_battery = 100
    vehicle_status = "idle"

    pickup_x = 7
    pickup_y = 6

    dropoff_x = 8
    dropoff_y = 7

    charging_station_x = 4
    charging_station_y = 2

    distance_to_pickup = manhattan_distance(
        vehicle_x,
        vehicle_y,
        pickup_x,
        pickup_y,
    )

    distance_pickup_to_dropoff = manhattan_distance(
        pickup_x,
        pickup_y,
        dropoff_x,
        dropoff_y,
    )

    distance_to_charger = manhattan_distance(
        vehicle_x,
        vehicle_y,
        charging_station_x,
        charging_station_y,
    )

    distance_dropoff_to_charger = manhattan_distance(
        dropoff_x,
        dropoff_y,
        charging_station_x,
        charging_station_y,
    )

    required_battery = (
        distance_to_pickup
        + distance_pickup_to_dropoff
        + distance_dropoff_to_charger
    )

    vehicle_status = "to_pickup"

    if vehicle_battery >= required_battery:
        print("The vehicle has enough battery to accept the trip.")
        vehicle_x, vehicle_y, current_time, vehicle_battery = move_vehicle_to(
            vehicle_x,
            vehicle_y,
            pickup_x,
            pickup_y,
            current_time,
            vehicle_battery
        )

        print("The vehicle reached the passenger.")

        vehicle_status = "with_passenger"

        vehicle_x, vehicle_y, current_time, vehicle_battery = move_vehicle_to(
            vehicle_x,
        vehicle_y,
        dropoff_x,
        dropoff_y,
        current_time,
        vehicle_battery,
        )

        print("The passenger reached the drop-off location.")

        vehicle_status = "idle"
        distance_to_charger = manhattan_distance(
            vehicle_x,
            vehicle_y,
            charging_station_x,
            charging_station_y,
        )

    else:
        print("The vehicle does not have enough battery to accept the trip")


    print(f"Time: {current_time}")
    print(f"Vehicle ID: {vehicle_id}")
    print(f"Vehicle position: ({vehicle_x}, {vehicle_y})")
    print(f"Vehicle Status: {vehicle_status}")
    print(f"Battery Level: {vehicle_battery}")
    print(f"Required Battery: {required_battery}")
    print(f"Distance to pickup: {distance_to_pickup}")
    print(f"Distance to charging station: {distance_to_charger}")
    print(f"Distance from pickup to drop-off: {distance_pickup_to_dropoff}")
    print(f"Pickup position: ({pickup_x}, {pickup_y})")
    print(f"Drop-off position: ({dropoff_x}, {dropoff_y})")
    print(f"Distance from drop-off to charging station: {distance_dropoff_to_charger}")
    print(f"Charging station position: ({charging_station_x}, {charging_station_y})")


if __name__ == "__main__":
    main()
