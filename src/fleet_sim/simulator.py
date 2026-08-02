"""Base electric fleet simulator."""

from fleet_sim.event_queue import EventQueue
from fleet_sim.models import ChargingStation, PassengerRequest, ScheduledTrip, Vehicle
from fleet_sim.scheduling import (
    complete_ready_trips,
    schedule_request,
)


def main() -> None:
    """Run the base electric fleet simulation."""
    event_queue = EventQueue()
    current_time = 0

    vehicles = [
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
            battery=70,
        ),
        Vehicle(
            vehicle_id=3,
            x=10,
            y=10,
            battery=20,
        ),
    ]

    requests = [
        PassengerRequest(
            request_id=1,
            pickup_x=7,
            pickup_y=6,
            dropoff_x=-8,
            dropoff_y=7,
            arrival_time=0,
        ),
        PassengerRequest(
            request_id=2,
            pickup_x=2,
            pickup_y=3,
            dropoff_x=5,
            dropoff_y=1,
            arrival_time=10,
        ),
        PassengerRequest(
            request_id=3,
            pickup_x=-3,
            pickup_y=4,
            dropoff_x=1,
            dropoff_y=-2,
            arrival_time=35,
        ),
    ]

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

    ScheduledTrip(
        vehicle_id=2,
        request_id=1,
        start_time=0,
        completion_time=19,
        final_x=-8,
        final_y=7,
        battery_used=19,
    )

    requests.sort(key=lambda request: request.arrival_time)

    for request in requests:
        current_time = request.arrival_time

        complete_ready_trips(
            event_queue=event_queue,
            current_time=current_time,
            vehicles=vehicles,
            requests=requests,
        )

        print()
        print(f"Processing request {request.request_id} at time {current_time}")

        trip = schedule_request(
            request=request,
            vehicles=vehicles,
            charging_stations=charging_stations,
            event_queue=event_queue,
            current_time=current_time,
        )

        if trip is None:
            print(f"Request {request.request_id} remains waiting.")
        else:
            print(
                f"Request {request.request_id} assigned to vehicle {trip.vehicle_id}."
            )
            print(f"Scheduled completion time: {trip.completion_time}")

    while not event_queue.is_empty():
        current_time = event_queue.peek().completion_time

        complete_ready_trips(
            event_queue=event_queue,
            current_time=current_time,
            vehicles=vehicles,
            requests=requests,
        )

    print()
    print("Final simulation state")

    for vehicle in vehicles:
        print(
            f"Vehicle {vehicle.vehicle_id}: "
            f"position=({vehicle.x}, {vehicle.y}), "
            f"battery={vehicle.battery}, "
            f"status={vehicle.status}, "
            f"available_time={vehicle.available_time}"
        )

    for request in requests:
        print(f"Request {request.request_id}: status={request.status}")


if __name__ == "__main__":
    main()
