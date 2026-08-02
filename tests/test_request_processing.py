"""Integration tests for request processing."""

from fleet_sim.models import ChargingStation, PassengerRequest, Vehicle
from fleet_sim.request_processing import process_request


def test_process_request_completes_trip() -> None:
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
    ]

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
            x=1,
            y=9,
            charging_rate=6,
            total_ports=1,
        ),
    ]

    current_time = process_request(
        request,
        vehicles,
        charging_stations,
        current_time=0,
    )

    assert current_time == 19
    assert request.status == "completed"

    selected_vehicle = vehicles[1]

    assert selected_vehicle.x == -8
    assert selected_vehicle.y == 7
    assert selected_vehicle.battery == 51
    assert selected_vehicle.status == "idle"
    assert selected_vehicle.available_time == 19


def test_process_request_leaves_request_waiting_when_no_vehicle_is_feasible() -> None:
    vehicles = [
        Vehicle(
            vehicle_id=1,
            x=0,
            y=0,
            battery=2,
        ),
        Vehicle(
            vehicle_id=2,
            x=5,
            y=5,
            battery=1,
        ),
    ]

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
            x=1,
            y=9,
            charging_rate=6,
            total_ports=1,
        ),
    ]

    current_time = process_request(
        request,
        vehicles,
        charging_stations,
        current_time=5,
    )

    assert current_time == 5
    assert request.status == "waiting"

    assert vehicles[0].x == 0
    assert vehicles[0].y == 0
    assert vehicles[0].battery == 2

    assert vehicles[1].x == 5
    assert vehicles[1].y == 5
    assert vehicles[1].battery == 1
    assert vehicles[1].available_time == 0
