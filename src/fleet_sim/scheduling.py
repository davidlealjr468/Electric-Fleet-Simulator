"""Functions for scheduling vehicle trips."""

from fleet_sim.distance import manhattan_distance
from fleet_sim.models import PassengerRequest, Vehicle


def calculate_trip_duration(
    vehicle: Vehicle,
    request: PassengerRequest,
) -> int:
    """Calculate the time required to complete a passenger request."""

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

    return distance_to_pickup + distance_pickup_to_dropoff
