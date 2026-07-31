"""Data models for the fleet simulator."""

from dataclasses import dataclass


@dataclass
class Vehicle:
    """Represents a vehicle in the fleet simulator."""

    vehicle_id: int
    x: int
    y: int
    battery: int
    status: str = "idle"  # Possible statuses: idle, to_charger, charging, stranded


@dataclass
class PassengerRequest:
    """Represents a passenger trip request."""

    request_id: int
    pickup_x: int
    pickup_y: int
    dropoff_x: int
    dropoff_y: int
    status: str = "waiting"


@dataclass
class ChargingStation:
    """Represent an electric-vehicle charging station."""

    station_id: int
    x: int
    y: int
    charging_rate: int
