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
    total_ports: int
    occupied_ports: int = 0

    @property
    def available_ports(self) -> int:
        """Return the number of currently available charging ports"""
        return self.total_ports - self.occupied_ports

    def occupy_port(self) -> None:
        """Occupy one charging port."""
        if self.available_ports <= 0:
            raise ValueError("No charging ports are available.")

        self.occupied_ports += 1

    def release_port(self) -> None:
        """Release one charging port."""
        if self.occupied_ports <= 0:
            raise ValueError("No occupied charging ports can be released")

        self.occupied_ports -= 1
