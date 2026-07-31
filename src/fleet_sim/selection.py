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
        station_x, station_y = station

        station_distance = manhattan_distance(
            vehicle_x,
            vehicle_y,
            station_x,
            station_y,
        )

        if station_distance < nearest_station_distance:
            nearest_station = station
            nearest_station_distance = station_distance

    return nearest_station, nearest_station_distance
