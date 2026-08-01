"""Base electric fleet simulator."""

from fleet_sim.charging import charge_vehicle
from fleet_sim.distance import manhattan_distance
from fleet_sim.models import ChargingStation, PassengerRequest, Vehicle
from fleet_sim.movement import move_vehicle_to
from fleet_sim.selection import find_nearest_charging_station


def main() -> None:
    """Run the base electric fleet simulation."""
    current_time = 0

    vehicle = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=10,
        ),
        Vehicle(
            vehicle_id=2,
            x=5,
            y=5,
            battery=15,
        ),
        Vehicle(
            vehicle_id=3,
            x=10,
            y=10,
            battery=20,
        ),
    ]

    vehicle = vehicle[0]  # Select the first vehicle for this simulation

    request = PassengerRequest(
        request_id=1,
        pickup_x=7,
        pickup_y=6,
        dropoff_x=-8,
        dropoff_y=7,
    )

    charging_stations = [
        ChargingStation(
            station_id=1,
            x=4,
            y=2,
            charging_rate=5,
            total_ports=2,
        ),
        ChargingStation(
            station_id=2,
            x=10,
            y=8,
            charging_rate=8,
            total_ports=4,
        ),
        ChargingStation(
            station_id=3,
            x=1,
            y=9,
            charging_rate=6,
            total_ports=1,
        ),
    ]

    nearest_station, nearest_station_distance = find_nearest_charging_station(
        vehicle.x,
        vehicle.y,
        charging_stations,
    )
    charging_station_x, charging_station_y = nearest_station.x, nearest_station.y
    distance_to_charger = nearest_station_distance

    print(
        f"Nearest charging station is at ({charging_station_x}, {charging_station_y})."
    )

    charging_target = 80

    distance_to_pickup = manhattan_distance(
        vehicle.x,
        vehicle.y,
        request.pickup_x,
        request.pickup_y,
    )

    distance_pickup_to_dropoff = manhattan_distance(
        request.pickup_x,
        request.pickup_y,
        request.dropoff_x,
        request.dropoff_y,
    )

    distance_dropoff_to_charger = manhattan_distance(
        request.dropoff_x,
        request.dropoff_y,
        charging_station_x,
        charging_station_y,
    )

    required_battery = (
        distance_to_pickup + distance_pickup_to_dropoff + distance_dropoff_to_charger
    )

    if vehicle.battery >= required_battery:
        print("The vehicle has enough battery to accept the trip.")

        vehicle.status = "to_pickup"

        current_time = move_vehicle_to(
            vehicle,
            request.pickup_x,
            request.pickup_y,
            current_time,
        )

        print("The vehicle reached the passenger.")

        vehicle.status = "with_passenger"
        request.status = "picked_up"

        current_time = move_vehicle_to(
            vehicle,
            request.dropoff_x,
            request.dropoff_y,
            current_time,
        )

        print("The passenger reached the drop-off location.")

        request.status = "completed"
        vehicle.status = "idle"

    else:
        print("The vehicle does not have enough battery to accept the trip.")

        if vehicle.battery >= distance_to_charger:
            print("The vehicle has enough battery to reach the charging station.")

            vehicle.status = "to_charger"

            current_time = move_vehicle_to(
                vehicle,
                charging_station_x,
                charging_station_y,
                current_time,
            )

            print("The vehicle reached the charging station.")
            vehicle.status = "charging"

            nearest_station.occupy_port()

            vehicle.battery, current_time = charge_vehicle(
                vehicle.battery,
                charging_target,
                nearest_station.charging_rate,
                current_time,
            )

            nearest_station.release_port()

            print("The vehicle finished charging.")
            vehicle.status = "idle"

        else:
            print(
                "The vehicle does not have enough battery "
                "to reach the charging station."
            )
            print("The vehicle is stranded.")
            vehicle.status = "stranded"
            request.status = "waiting"

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

    print(f"Request ID: {request.request_id}")
    print(f"Request Status: {request.status}")
    print(f"Pickup position: ({request.pickup_x}, {request.pickup_y})")
    print(f"Drop-off position: ({request.dropoff_x}, {request.dropoff_y})")

    print(f"Required Battery: {required_battery}")
    print(f"Distance to pickup: {distance_to_pickup}")
    print(f"Distance from pickup to drop-off: {distance_pickup_to_dropoff}")
    print(f"Distance from drop-off to charging station: {distance_dropoff_to_charger}")
    print(f"Distance to charging station: {distance_to_charger}")
    print(f"Charging station ID: {nearest_station.station_id}")
    print(f"Available charging ports: {nearest_station.available_ports}")
    print(f"Total charging ports: {nearest_station.total_ports}")
    print(f"Occupied charging ports: {nearest_station.occupied_ports}")
    print(f"Available charging ports: {nearest_station.available_ports}")
    print(f"Charging station position: ({charging_station_x}, {charging_station_y})")


if __name__ == "__main__":
    main()
