"""Base electric fleet simulator."""

from fleet_sim.models import ChargingStation, PassengerRequest, Vehicle
from fleet_sim.request_processing import process_request


def main() -> None:
    """Run the base electric fleet simulation."""
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

    requests.sort(key=lambda r: r.arrival_time)
    for request in requests:
        if current_time < request.arrival_time:
            current_time = request.arrival_time
        print()
        print(f"Processing request {request.request_id} at time {current_time}")

        current_time = process_request(
            request,
            vehicles,
            charging_stations,
            current_time,
        )


if __name__ == "__main__":
    main()
