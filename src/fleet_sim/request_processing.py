"""Passenger-request processing behavior."""

from fleet_sim.charging import charge_vehicle
from fleet_sim.distance import manhattan_distance
from fleet_sim.movement import move_vehicle_to
from fleet_sim.selection import (
    find_nearest_available_vehicle,
    find_nearest_charging_station,
)


def process_request(
    request,
    vehicles,
    charging_stations,
    current_time,
):
    """Process a passenger request."""
    dropoff_station, distance_to_dropoff_station = find_nearest_charging_station(
        request.dropoff_x,
        request.dropoff_y,
        charging_stations,
    )

    distance_pickup_to_dropoff = manhattan_distance(
        request.pickup_x,
        request.pickup_y,
        request.dropoff_x,
        request.dropoff_y,
    )

    minimum_battery_after_pickup = (
        distance_pickup_to_dropoff + distance_to_dropoff_station
    )

    try:
        vehicle, distance_to_pickup = find_nearest_available_vehicle(
            pickup_x=request.pickup_x,
            pickup_y=request.pickup_y,
            vehicles=vehicles,
            minimum_battery_after_pickup=minimum_battery_after_pickup,
            current_time=current_time,
        )
    except ValueError:
        print(
            f"No available vehicles can complete "
            f"the trip for request {request.request_id}."
        )
        request.status = "waiting"
        return current_time

    vehicle, distance_to_pickup = find_nearest_available_vehicle(
        pickup_x=request.pickup_x,
        pickup_y=request.pickup_y,
        vehicles=vehicles,
        minimum_battery_after_pickup=minimum_battery_after_pickup,
        current_time=current_time,
    )

    print(
        f"Nearest available vehicle is ID {vehicle.vehicle_id} "
        f"at ({vehicle.x}, {vehicle.y}) with battery level {vehicle.battery}."
    )

    nearest_station, nearest_station_distance = find_nearest_charging_station(
        vehicle.x,
        vehicle.y,
        charging_stations,
    )

    charging_station_x = nearest_station.x
    charging_station_y = nearest_station.y
    distance_to_charger = nearest_station_distance

    print(
        f"Nearest charging station is at ({charging_station_x}, {charging_station_y})."
    )

    charging_target = 80

    distance_dropoff_to_charger = distance_to_dropoff_station

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

        vehicle.available_time = current_time
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
    print(f"Charging station position: ({charging_station_x}, {charging_station_y})")

    return current_time
