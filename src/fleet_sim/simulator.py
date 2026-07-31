"""Base electric fleet simulator."""

from fleet_sim.charging import charge_vehicle
from fleet_sim.distance import manhattan_distance
from fleet_sim.models import Vehicle
from fleet_sim.movement import move_vehicle_to
from fleet_sim.selection import find_nearest_charging_station


def main() -> None:
    """Run the base electric fleet simulation."""
    current_time = 0

    vehicle = Vehicle(
        vehicle_id=1,
        x=0,
        y=0,
        battery=10,
    )

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
        vehicle.x, vehicle.y, charging_stations
    )
    charging_station_x, charging_station_y = nearest_station
    distance_to_charger = nearest_station_distance

    print(
        f"Nearest charging station is at ({charging_station_x}, {charging_station_y})."
    )
    charging_rate = 5  # Units per time step
    charging_target = 80

    distance_to_pickup = manhattan_distance(
        vehicle.x,
        vehicle.y,
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

    current_time = move_vehicle_to(vehicle, pickup_x, pickup_y, current_time)

    if vehicle.battery >= required_battery:
        print("The vehicle has enough battery to accept the trip.")

        vehicle.status = "to_pickup"

        vehicle.x, vehicle.y, current_time, vehicle.battery = move_vehicle_to(
            vehicle.x, vehicle.y, pickup_x, pickup_y, current_time, vehicle.battery
        )

        print("The vehicle reached the passenger.")

        vehicle.status = "with_passenger"

        vehicle.x, vehicle.y, current_time, vehicle.battery = move_vehicle_to(
            vehicle.x,
            vehicle.y,
            dropoff_x,
            dropoff_y,
            current_time,
            vehicle.battery,
        )

        print("The passenger reached the drop-off location.")

        vehicle.status = "idle"

    else:
        print("The vehicle does not have enough battery to accept the trip.")

        if vehicle.battery >= distance_to_charger:
            print("The vehicle has enough battery to reach the charging station.")

            vehicle.status = "to_charger"

            vehicle.x, vehicle.y, current_time, vehicle.battery = move_vehicle_to(
                vehicle.x,
                vehicle.y,
                charging_station_x,
                charging_station_y,
                current_time,
                vehicle.battery,
            )

            print("The vehicle reached the charging station.")
            vehicle.status = "charging"

            vehicle.battery, current_time = charge_vehicle(
                vehicle.battery,
                charging_target,
                charging_rate,
                current_time,
            )

            print("The vehicle finished charging.")
            vehicle.status = "idle"

        else:
            print(
                "The vehicle does not have enough battery "
                "to reach the charging station."
            )
            print("The vehicle is stranded.")
            vehicle.status = "stranded"

    distance_to_charger = manhattan_distance(
        vehicle.x,
        vehicle.y,
        charging_station_x,
        charging_station_y,
    )

    print(f"Time: {current_time}")
    print(f"Vehicle ID: {vehicle.vehicle_id}")
    print(f"Vehicle position: ({vehicle.x}, {vehicle.y})")
    print(f"Vehicle Status: {vehicle.status}")
    print(f"Battery Level: {vehicle.battery}")
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
