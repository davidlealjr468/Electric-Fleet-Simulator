"""Tests for trip scheduling."""

from fleet_sim.event_queue import EventQueue
from fleet_sim.models import (
    ChargingStation,
    PassengerRequest,
    Vehicle,
)
from fleet_sim.request_queue import RequestQueue
from fleet_sim.scheduling import (
    assign_trip,
    calculate_trip_duration,
    complete_ready_trips,
    complete_scheduled_trip,
    retry_waiting_requests,
    schedule_request,
    schedule_trip,
)


def test_calculate_trip_duration() -> None:
    vehicle = Vehicle(
        vehicle_id=2,
        x=5,
        y=5,
        battery=70,
    )

    request = PassengerRequest(
        request_id=1,
        pickup_x=7,
        pickup_y=6,
        dropoff_x=-8,
        dropoff_y=7,
        arrival_time=0,
    )

    duration = calculate_trip_duration(vehicle, request)

    assert duration == 19


def test_schedule_trip_creates_future_event() -> None:
    vehicle = Vehicle(
        vehicle_id=2,
        x=5,
        y=5,
        battery=70,
    )

    request = PassengerRequest(
        request_id=1,
        pickup_x=7,
        pickup_y=6,
        dropoff_x=-8,
        dropoff_y=7,
        arrival_time=0,
    )

    trip = schedule_trip(
        vehicle=vehicle,
        request=request,
        start_time=0,
    )

    assert trip.vehicle_id == 2
    assert trip.request_id == 1
    assert trip.start_time == 0
    assert trip.completion_time == 19
    assert trip.final_x == -8
    assert trip.final_y == 7
    assert trip.battery_used == 19


def test_schedule_trip_does_not_immediately_move_vehicle() -> None:
    vehicle = Vehicle(
        vehicle_id=2,
        x=5,
        y=5,
        battery=70,
    )

    request = PassengerRequest(
        request_id=1,
        pickup_x=7,
        pickup_y=6,
        dropoff_x=-8,
        dropoff_y=7,
    )

    schedule_trip(
        vehicle=vehicle,
        request=request,
        start_time=0,
    )

    assert vehicle.x == 5
    assert vehicle.y == 5
    assert vehicle.battery == 70


def test_complete_scheduled_trip_updates_vehicle_and_request() -> None:
    vehicle = Vehicle(
        vehicle_id=2,
        x=5,
        y=5,
        battery=70,
        status="with_passenger",
        available_time=19,
    )

    request = PassengerRequest(
        request_id=1,
        pickup_x=7,
        pickup_y=6,
        dropoff_x=-8,
        dropoff_y=7,
        status="assigned",
    )

    trip = schedule_trip(
        vehicle=vehicle,
        request=request,
        start_time=0,
    )

    complete_scheduled_trip(
        trip=trip,
        vehicles=[vehicle],
        requests=[request],
    )

    assert vehicle.x == -8
    assert vehicle.y == 7
    assert vehicle.battery == 51
    assert vehicle.status == "idle"
    assert vehicle.available_time == 19
    assert request.status == "completed"


def test_assign_trip_marks_vehicle_and_request_as_active() -> None:
    vehicle = Vehicle(
        vehicle_id=2,
        x=5,
        y=5,
        battery=70,
    )

    request = PassengerRequest(
        request_id=1,
        pickup_x=7,
        pickup_y=6,
        dropoff_x=-8,
        dropoff_y=7,
        arrival_time=0,
    )

    trip = assign_trip(
        vehicle=vehicle,
        request=request,
        start_time=0,
    )

    assert vehicle.status == "with_passenger"
    assert vehicle.available_time == 19
    assert request.status == "assigned"

    assert vehicle.x == 5
    assert vehicle.y == 5
    assert vehicle.battery == 70

    assert trip.completion_time == 19


def test_complete_ready_trips_only_completes_finished_events() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=50,
        ),
        Vehicle(
            vehicle_id=2,
            x=5,
            y=5,
            battery=70,
        ),
    ]

    requests = [
        PassengerRequest(
            request_id=1,
            pickup_x=1,
            pickup_y=0,
            dropoff_x=3,
            dropoff_y=0,
        ),
        PassengerRequest(
            request_id=2,
            pickup_x=6,
            pickup_y=5,
            dropoff_x=10,
            dropoff_y=5,
        ),
    ]

    queue = EventQueue()

    first_trip = assign_trip(
        vehicle=vehicles[0],
        request=requests[0],
        start_time=0,
    )

    second_trip = assign_trip(
        vehicle=vehicles[1],
        request=requests[1],
        start_time=0,
    )

    queue.push(first_trip)
    queue.push(second_trip)

    complete_ready_trips(
        event_queue=queue,
        current_time=3,
        vehicles=vehicles,
        requests=requests,
    )

    assert requests[0].status == "completed"
    assert vehicles[0].status == "idle"

    assert requests[1].status == "assigned"
    assert vehicles[1].status == "with_passenger"

    assert len(queue) == 1


def test_schedule_request_uses_another_vehicle_when_first_is_busy() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=100,
        ),
        Vehicle(
            vehicle_id=2,
            x=10,
            y=0,
            battery=100,
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
            pickup_x=9,
            pickup_y=0,
            dropoff_x=8,
            dropoff_y=0,
            arrival_time=2,
        ),
    ]

    charging_stations = [
        ChargingStation(
            station_id=1,
            x=5,
            y=0,
            charging_rate=5,
            total_ports=2,
        ),
    ]

    queue = EventQueue()

    first_trip = schedule_request(
        request=requests[0],
        vehicles=vehicles,
        charging_stations=charging_stations,
        event_queue=queue,
        current_time=0,
    )

    second_trip = schedule_request(
        request=requests[1],
        vehicles=vehicles,
        charging_stations=charging_stations,
        event_queue=queue,
        current_time=2,
    )

    assert first_trip is not None
    assert second_trip is not None

    assert first_trip.vehicle_id == 1
    assert second_trip.vehicle_id == 2

    assert vehicles[0].status == "with_passenger"
    assert vehicles[1].status == "with_passenger"

    assert requests[0].status == "assigned"
    assert requests[1].status == "assigned"

    assert len(queue) == 2


def test_retry_waiting_requests_assigns_request_when_vehicle_is_available() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=100,
        ),
    ]

    request = PassengerRequest(
        request_id=1,
        pickup_x=1,
        pickup_y=0,
        dropoff_x=3,
        dropoff_y=0,
        arrival_time=0,
    )

    charging_stations = [
        ChargingStation(
            station_id=1,
            x=4,
            y=0,
            charging_rate=5,
            total_ports=2,
        ),
    ]

    request_queue = RequestQueue()
    event_queue = EventQueue()

    request_queue.add(request)

    retry_waiting_requests(
        request_queue=request_queue,
        vehicles=vehicles,
        charging_stations=charging_stations,
        event_queue=event_queue,
        current_time=5,
    )

    assert request_queue.is_empty()
    assert request.status == "assigned"
    assert vehicles[0].status == "with_passenger"
    assert len(event_queue) == 1

    def test_retry_waiting_requests_keeps_unserviceable_request_waiting() -> None:
        vehicles = [
            Vehicle(
                vehicle_id=1,
                x=0,
                y=0,
                battery=1,
            ),
        ]

        request = PassengerRequest(
            request_id=1,
            pickup_x=5,
            pickup_y=0,
            dropoff_x=10,
            dropoff_y=0,
            arrival_time=0,
        )

        charging_stations = [
            ChargingStation(
                station_id=1,
                x=11,
                y=0,
                charging_rate=5,
                total_ports=2,
            ),
        ]

        request_queue = RequestQueue()
        event_queue = EventQueue()

        request_queue.add(request)

        retry_waiting_requests(
            request_queue=request_queue,
            vehicles=vehicles,
            charging_stations=charging_stations,
            event_queue=event_queue,
            current_time=5,
        )

        assert len(request_queue) == 1
        assert request.status == "waiting"
        assert vehicles[0].status == "idle"
        assert event_queue.is_empty()


def test_waiting_request_is_assigned_after_vehicle_completes() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=100,
        ),
    ]

    requests = [
        PassengerRequest(
            request_id=1,
            pickup_x=1,
            pickup_y=0,
            dropoff_x=5,
            dropoff_y=0,
            arrival_time=0,
        ),
        PassengerRequest(
            request_id=2,
            pickup_x=5,
            pickup_y=0,
            dropoff_x=7,
            dropoff_y=0,
            arrival_time=2,
        ),
    ]

    charging_stations = [
        ChargingStation(
            station_id=1,
            x=8,
            y=0,
            charging_rate=5,
            total_ports=2,
        ),
    ]

    event_queue = EventQueue()
    request_queue = RequestQueue()

    first_trip = schedule_request(
        request=requests[0],
        vehicles=vehicles,
        charging_stations=charging_stations,
        event_queue=event_queue,
        current_time=0,
    )

    assert first_trip is not None
    assert first_trip.completion_time == 5

    second_trip = schedule_request(
        request=requests[1],
        vehicles=vehicles,
        charging_stations=charging_stations,
        event_queue=event_queue,
        current_time=2,
    )

    assert second_trip is None

    request_queue.add(requests[1])

    complete_ready_trips(
        event_queue=event_queue,
        current_time=5,
        vehicles=vehicles,
        requests=requests,
    )

    retry_waiting_requests(
        request_queue=request_queue,
        vehicles=vehicles,
        charging_stations=charging_stations,
        event_queue=event_queue,
        current_time=5,
    )

    assert request_queue.is_empty()
    assert requests[0].status == "completed"
    assert requests[1].status == "assigned"
    assert vehicles[0].status == "with_passenger"
    assert len(event_queue) == 1

    next_trip = event_queue.peek()

    assert next_trip.request_id == 2
    assert next_trip.start_time == 5
    assert next_trip.completion_time == 7
