"""Run the electric fleet simulation."""

from fleet_sim.event_queue import EventQueue
from fleet_sim.models import ChargingStation, PassengerRequest, Vehicle
from fleet_sim.request_queue import RequestQueue
from fleet_sim.scheduling import (
    complete_ready_events,
    retry_waiting_requests,
    schedule_request,
)


def main() -> None:
    """Run the electric fleet simulation."""

    current_time = 0

    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=80,
        ),
        Vehicle(
            vehicle_id=2,
            x=8,
            y=5,
            battery=90,
        ),
        Vehicle(
            vehicle_id=3,
            x=-6,
            y=4,
            battery=75,
        ),
    ]

    requests = [
        PassengerRequest(
            request_id=1,
            pickup_x=1,
            pickup_y=0,
            dropoff_x=6,
            dropoff_y=0,
            arrival_time=0,
        ),
        PassengerRequest(
            request_id=2,
            pickup_x=8,
            pickup_y=6,
            dropoff_x=10,
            dropoff_y=10,
            arrival_time=2,
        ),
        PassengerRequest(
            request_id=3,
            pickup_x=-5,
            pickup_y=4,
            dropoff_x=-10,
            dropoff_y=-3,
            arrival_time=4,
        ),
        PassengerRequest(
            request_id=4,
            pickup_x=0,
            pickup_y=1,
            dropoff_x=3,
            dropoff_y=1,
            arrival_time=3,
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
            x=-8,
            y=-1,
            charging_rate=6,
            total_ports=1,
        ),
    ]

    event_queue = EventQueue()
    request_queue = RequestQueue()

    requests.sort(key=lambda request: request.arrival_time)

    for request in requests:
        current_time = request.arrival_time

        complete_ready_events(
            event_queue=event_queue,
            current_time=current_time,
            vehicles=vehicles,
            requests=requests,
            charging_stations=charging_stations,
        )

        retry_waiting_requests(
            request_queue=request_queue,
            vehicles=vehicles,
            charging_stations=charging_stations,
            event_queue=event_queue,
            current_time=current_time,
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
            request_queue.add(request)

            print(f"Request {request.request_id} added to the waiting queue.")
        else:
            print(
                f"Request {request.request_id} assigned to vehicle {trip.vehicle_id}."
            )
            print(f"Scheduled completion time: {trip.completion_time}")

    while not event_queue.is_empty():
        current_time = event_queue.peek().completion_time

        complete_ready_events(
            event_queue=event_queue,
            current_time=current_time,
            vehicles=vehicles,
            requests=requests,
            charging_stations=charging_stations,
        )

        retry_waiting_requests(
            request_queue=request_queue,
            vehicles=vehicles,
            charging_stations=charging_stations,
            event_queue=event_queue,
            current_time=current_time,
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

    if not request_queue.is_empty():
        print()
        print(f"{len(request_queue)} request(s) could not be completed.")


if __name__ == "__main__":
    main()
