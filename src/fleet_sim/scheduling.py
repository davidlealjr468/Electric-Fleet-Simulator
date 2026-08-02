"""Functions for scheduling vehicle trips."""

from fleet_sim.distance import manhattan_distance
from fleet_sim.event_queue import EventQueue
from fleet_sim.models import (
    ChargingStation,
    PassengerRequest,
    ScheduledTrip,
    Vehicle,
)
from fleet_sim.request_queue import RequestQueue
from fleet_sim.selection import (
    find_nearest_available_vehicle,
    find_nearest_charging_station,
)


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


def schedule_trip(
    vehicle: Vehicle,
    request: PassengerRequest,
    start_time: int,
) -> ScheduledTrip:
    """Schedule a passenger trip to complete in the future."""
    trip_duration = calculate_trip_duration(vehicle, request)

    return ScheduledTrip(
        vehicle_id=vehicle.vehicle_id,
        request_id=request.request_id,
        start_time=start_time,
        completion_time=start_time + trip_duration,
        final_x=request.dropoff_x,
        final_y=request.dropoff_y,
        battery_used=trip_duration,
    )


def complete_scheduled_trip(
    trip: ScheduledTrip,
    vehicles: list[Vehicle],
    requests: list[PassengerRequest],
) -> None:
    """Apply a completed trip to its vehicle and request."""

    vehicle = next(
        vehicle for vehicle in vehicles if vehicle.vehicle_id == trip.vehicle_id
    )

    request = next(
        request for request in requests if request.request_id == trip.request_id
    )

    vehicle.x = trip.final_x
    vehicle.y = trip.final_y
    vehicle.battery -= trip.battery_used
    vehicle.status = "idle"
    vehicle.available_time = trip.completion_time

    request.status = "completed"


def assign_trip(
    vehicle: Vehicle,
    request: PassengerRequest,
    start_time: int,
) -> ScheduledTrip:
    """Assign a request to a vehicle and schedule its completion."""

    trip = schedule_trip(
        vehicle=vehicle,
        request=request,
        start_time=start_time,
    )

    vehicle.status = "with_passenger"
    vehicle.available_time = trip.completion_time
    request.status = "assigned"

    return trip


def complete_ready_trips(
    event_queue: EventQueue,
    current_time: int,
    vehicles: list[Vehicle],
    requests: list[PassengerRequest],
) -> None:
    """Complete every scheduled trip ready by the current time."""

    ready_trips = event_queue.pop_ready(current_time)

    for trip in ready_trips:
        complete_scheduled_trip(
            trip=trip,
            vehicles=vehicles,
            requests=requests,
        )


def schedule_request(
    request: PassengerRequest,
    vehicles: list[Vehicle],
    charging_stations: list[ChargingStation],
    event_queue: EventQueue,
    current_time: int,
) -> ScheduledTrip | None:
    """Assign an arriving request and queue its completion event."""

    dropoff_station, distance_dropoff_to_station = find_nearest_charging_station(
        vehicle_x=request.dropoff_x,
        vehicle_y=request.dropoff_y,
        charging_stations=charging_stations,
    )

    distance_pickup_to_dropoff = manhattan_distance(
        request.pickup_x,
        request.pickup_y,
        request.dropoff_x,
        request.dropoff_y,
    )

    minimum_battery_after_pickup = (
        distance_pickup_to_dropoff + distance_dropoff_to_station
    )

    try:
        vehicle, _ = find_nearest_available_vehicle(
            pickup_x=request.pickup_x,
            pickup_y=request.pickup_y,
            vehicles=vehicles,
            minimum_battery_after_pickup=minimum_battery_after_pickup,
            current_time=current_time,
        )
    except ValueError:
        request.status = "waiting"
        return None

    trip = assign_trip(
        vehicle=vehicle,
        request=request,
        start_time=current_time,
    )

    event_queue.push(trip)

    return trip


def retry_waiting_requests(
    request_queue: RequestQueue,
    vehicles: list[Vehicle],
    charging_stations: list[ChargingStation],
    event_queue: EventQueue,
    current_time: int,
) -> None:
    """Retry all waiting requests in their original queue order."""

    waiting_requests = request_queue.drain()

    for request in waiting_requests:
        trip = schedule_request(
            request=request,
            vehicles=vehicles,
            charging_stations=charging_stations,
            event_queue=event_queue,
            current_time=current_time,
        )

        if trip is None:
            request_queue.add(request)
