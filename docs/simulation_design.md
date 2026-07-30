# Simulation Design (As of 7/30/26)

## Purpose

The Electric Fleet Simulator models how electric vehicles move through a city, serve passenger requests, consume battery energy, and use charging stations.

The project begins with a simplified grid-based model and will gradually expand to support multiple vehicles, multiple requests, optimization algorithms, pathfinding, validation, and performance analysis.

## Current Simulation Model

The current version contains:

- One electric vehicle
- One passenger request
- One charging station
- A two-dimensional grid
- Manhattan movement
- Battery consumption
- Battery-feasibility checks
- Vehicle charging

## Simulation State

The simulation state describes the system at a specific moment.

### Vehicle State

The vehicle currently stores:

- Vehicle ID
- x-coordinate
- y-coordinate
- Battery level
- Operating status

Current vehicle statuses include:

```text
idle
to_pickup
with_passenger
to_charger
charging
stranded
