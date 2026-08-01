"""Charging-station selection behavior."""

from fleet_sim.distance import manhattan_distance


def find_nearest_charging_station(
    vehicle_x,
    vehicle_y,
    charging_stations,
):
    """Find the nearest charging station to the vehicle's current position."""

    if not charging_stations:
        raise ValueError("At least one charging station is required.")

    nearest_station = None
    nearest_station_distance = float("inf")

    for station in charging_stations:
        station_distance = manhattan_distance(
            vehicle_x,
            vehicle_y,
            station.x,
            station.y,
        )

        if station_distance < nearest_station_distance:
            nearest_station = station
            nearest_station_distance = station_distance

    return nearest_station, nearest_station_distance


def find_nearest_available_vehicle(
    pickup_x,
    pickup_y,
    vehicles,
):
    """Find the nearest idle vehicle to a passenger pickup location."""
    nearest_vehicle = None
    nearest_vehicle_distance = float("inf")

    for vehicle in vehicles:
        if vehicle.status != "idle":
            continue

        vehicle_distance = manhattan_distance(
            vehicle.x,
            vehicle.y,
            pickup_x,
            pickup_y,
        )

        if vehicle_distance < nearest_vehicle_distance:
            nearest_vehicle = vehicle
            nearest_vehicle_distance = vehicle_distance

    if nearest_vehicle is None:
        raise ValueError("No available vehicles were found.")

    return nearest_vehicle, nearest_vehicle_distance
