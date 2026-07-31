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
