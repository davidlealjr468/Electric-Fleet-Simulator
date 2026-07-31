"""Base electric fleet simulator."""

from fleet_sim.charging import charge_vehicle
from fleet_sim.distance import manhattan_distance
from fleet_sim.movement import move_vehicle_to
from fleet_sim.selection import find_nearest_charging_station


def main() -> None:
    """Run the base electric fleet simulation."""
    current_time = 0

    vehicle_x = 0
    vehicle_y = 0
    vehicle_id = 1
    vehicle_battery = 10
    # vehicle_battery_capacity = 100
    vehicle_status = "idle"

    pickup_x = 7
    pickup_y = 6

    dropoff_x = -8
    dropoff_y = 7

    charging_stations = [
        (4, 2),
        (10, 8),
        (1, 9),
    ]

    nearest_station, nearest_station_distance = find_nearest_charging_station(
        vehicle_x, vehicle_y, charging_stations
    )
    charging_station_x, charging_station_y = nearest_station
    distance_to_charger = nearest_station_distance

    print(
        f"Nearest charging station is at ({charging_station_x}, {charging_station_y})."
    )
    charging_rate = 5  # Units per time step
    charging_target = 80

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

    distance_dropoff_to_charger = manhattan_distance(
        dropoff_x,
        dropoff_y,
        charging_station_x,
        charging_station_y,
    )

    required_battery = (
        distance_to_pickup + distance_pickup_to_dropoff + distance_dropoff_to_charger
    )

    if vehicle_battery >= required_battery:
        print("The vehicle has enough battery to accept the trip.")

        vehicle_status = "to_pickup"

        vehicle_x, vehicle_y, current_time, vehicle_battery = move_vehicle_to(
            vehicle_x, vehicle_y, pickup_x, pickup_y, current_time, vehicle_battery
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

    else:
        print("The vehicle does not have enough battery to accept the trip.")

        if vehicle_battery >= distance_to_charger:
            print("The vehicle has enough battery to reach the charging station.")

            vehicle_status = "to_charger"

            vehicle_x, vehicle_y, current_time, vehicle_battery = move_vehicle_to(
                vehicle_x,
                vehicle_y,
                charging_station_x,
                charging_station_y,
                current_time,
                vehicle_battery,
            )

            print("The vehicle reached the charging station.")
            vehicle_status = "charging"

            vehicle_battery, current_time = charge_vehicle(
                vehicle_battery,
                charging_target,
                charging_rate,
                current_time,
            )

            print("The vehicle finished charging.")
            vehicle_status = "idle"

        else:
            print(
                "The vehicle does not have enough battery "
                "to reach the charging station."
            )
            print("The vehicle is stranded.")
            vehicle_status = "stranded"

    distance_to_charger = manhattan_distance(
        vehicle_x,
        vehicle_y,
        charging_station_x,
        charging_station_y,
    )

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
