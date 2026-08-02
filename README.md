# Electric Fleet Simulator

[![CI](https://github.com/davidlealjr468/Electric-Fleet-Simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/davidlealjr468/Electric-Fleet-Simulator/actions)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-45%20passing-brightgreen)](#testing)
[![License](https://img.shields.io/badge/license-not%20specified-lightgrey)](#license)

An event-driven Python simulator for studying electric vehicle fleet operations, including passenger demand, vehicle dispatch, battery feasibility, charging infrastructure, concurrent trips, and waiting-request behavior.

## Overview

The simulator models a fleet of electric vehicles operating on a two-dimensional Manhattan grid.

Passenger requests arrive at specific simulation times. The system assigns each request to the nearest feasible vehicle while accounting for:

- vehicle availability,
- vehicle status,
- distance to the passenger,
- trip distance,
- remaining battery,
- and access to a charging station after drop-off.

Multiple vehicles can operate concurrently. When every suitable vehicle is busy, the passenger request enters a first-in, first-out waiting queue and is retried when a vehicle becomes available.

## Current Capabilities

### Fleet operations

- Multiple electric vehicles
- Multiple passenger requests
- Request arrival times
- Concurrent vehicle assignments
- Vehicle availability tracking
- Passenger waiting queue
- Automatic retrying of waiting requests
- Final vehicle and request state reporting

### Vehicle selection

The selected vehicle must:

1. Be idle
2. Be available at the current simulation time
3. Have enough battery to reach the pickup
4. Have enough battery to complete the passenger trip
5. Have enough remaining battery to reach a charging station

Among all feasible vehicles, the nearest one is selected.

### Event-driven scheduling

Trips are represented as future events rather than being completed immediately.

The simulator uses:

- `heapq` for completion-time event ordering
- `deque` for first-in, first-out passenger waiting
- scheduled trip start and completion times
- automatic processing of completed trips

### Charging infrastructure

- Multiple charging stations
- Configurable charging rates
- Charging-port capacity
- Port occupancy tracking
- Nearest-station selection
- Charging input validation

Charging behavior exists in the project, but full charging-event integration with the main event scheduler is still under development.

## Example Simulation

```text
Processing request 1 at time 0
Request 1 assigned to vehicle 1.
Scheduled completion time: 6

Processing request 2 at time 2
Request 2 assigned to vehicle 2.
Scheduled completion time: 9

Processing request 4 at time 3
Request 4 assigned to vehicle 3.
Scheduled completion time: 15

Processing request 3 at time 4
Request 3 added to the waiting queue.

Waiting request 3 assigned to vehicle 1 at time 6.
Scheduled completion time: 33
```

This example demonstrates three vehicles working concurrently while a fourth passenger waits until a vehicle becomes available.

## Simulation Flow

```text
Passenger request arrives
          |
          v
Complete trips ready by the current time
          |
          v
Retry passengers already waiting
          |
          v
Find nearest feasible vehicle
       /       \
      /         \
Vehicle found   No vehicle available
     |                  |
     v                  v
Assign trip       Add request to queue
     |
     v
Schedule future completion event
     |
     v
Vehicle remains busy
     |
     v
Completion event is processed
     |
     v
Vehicle returns to idle
     |
     v
Retry waiting requests
```

## Project Structure

```text
Electric-Fleet-Simulator/
├── .github/
│   └── workflows/           # Continuous integration
├── analysis/                # Analysis work
├── benchmarks/              # Performance benchmarks
├── configs/                 # Future simulation configurations
├── data/                    # Scenario and input data
├── docs/                    # Project documentation
├── src/
│   └── fleet_sim/
│       ├── __init__.py
│       ├── __main__.py
│       ├── charging.py
│       ├── distance.py
│       ├── event_queue.py
│       ├── models.py
│       ├── movement.py
│       ├── request_processing.py
│       ├── request_queue.py
│       ├── scheduling.py
│       ├── selection.py
│       └── simulator.py
├── tests/
│   ├── test_charging.py
│   ├── test_distance.py
│   ├── test_event_queue.py
│   ├── test_models.py
│   ├── test_movement.py
│   ├── test_request_processing.py
│   ├── test_request_queue.py
│   ├── test_scheduling.py
│   └── test_selection.py
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Core Models

### `Vehicle`

Stores:

- vehicle ID,
- current position,
- battery level,
- operating status,
- and next available time.

### `PassengerRequest`

Stores:

- request ID,
- pickup location,
- drop-off location,
- arrival time,
- and request status.

### `ChargingStation`

Stores:

- station ID,
- location,
- charging rate,
- total ports,
- and occupied ports.

### `ScheduledTrip`

Stores:

- assigned vehicle,
- passenger request,
- start time,
- completion time,
- destination,
- and battery usage.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/davidlealjr468/Electric-Fleet-Simulator.git
cd Electric-Fleet-Simulator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux, macOS, or WSL:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install the project

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Install the development tools:

```bash
python -m pip install -r requirements-dev.txt
```

## Running the Simulator

```bash
python -m fleet_sim
```

The terminal output displays:

- request arrival times,
- immediate vehicle assignments,
- waiting-queue activity,
- scheduled completion times,
- final vehicle states,
- and final passenger-request states.

## Testing

Run the complete test suite:

```bash
pytest
```

Run with explicit verbose output:

```bash
pytest -v
```

Run one test module:

```bash
pytest tests/test_scheduling.py -v
```

The current suite covers:

- charging,
- Manhattan distance,
- event ordering,
- data models,
- vehicle movement,
- passenger request processing,
- request queues,
- trip scheduling,
- and vehicle selection.

## Code Quality

Format the code:

```bash
ruff format .
```

Run lint checks:

```bash
ruff check .
```

Run the full local verification workflow:

```bash
ruff format .
ruff check .
pytest
python -m fleet_sim
```

GitHub Actions provides continuous integration for repository changes.

## Architecture

The project separates simulation responsibilities into focused modules:

| Module | Responsibility |
|---|---|
| `models.py` | Fleet data models |
| `distance.py` | Manhattan-distance calculations |
| `movement.py` | Grid-based vehicle movement |
| `charging.py` | Battery charging behavior |
| `selection.py` | Vehicle and station selection |
| `request_processing.py` | Sequential passenger-trip processing |
| `scheduling.py` | Event-based trip assignment and completion |
| `event_queue.py` | Completion-time priority queue |
| `request_queue.py` | FIFO waiting-passenger queue |
| `simulator.py` | Main simulation scenario and event loop |

## Development Roadmap

### Completed

- [x] Two-dimensional grid simulation
- [x] Manhattan-distance calculations
- [x] Vehicle battery consumption
- [x] Passenger pickup and drop-off
- [x] Multiple vehicles
- [x] Multiple passenger requests
- [x] Request arrival times
- [x] Vehicle assignment
- [x] Concurrent trips
- [x] Event-based trip scheduling
- [x] Vehicle availability tracking
- [x] Passenger waiting queue
- [x] Automatic request retries
- [x] Multiple charging stations
- [x] Charging-port capacity
- [x] Automated tests
- [x] Continuous integration

### In progress

- [ ] Integrate charging into the event scheduler
- [ ] Route low-battery vehicles to charging stations
- [ ] Add charging-station waiting queues
- [ ] Improve simulation logging

### Planned

- [ ] Passenger waiting-time metrics
- [ ] Vehicle utilization metrics
- [ ] Fleet energy-consumption metrics
- [ ] Configuration-file loading
- [ ] CSV scenario loading
- [ ] Random passenger-demand generation
- [ ] Reproducible simulation seeds
- [ ] Road-network graph representation
- [ ] Dijkstra and A* routing
- [ ] Traffic-aware routing
- [ ] Fleet repositioning
- [ ] Policy comparison and optimization
- [ ] Monte Carlo experiments
- [ ] Visualization and 3D-engine integration

## Current Limitations

- The environment is a simplified two-dimensional grid.
- Distance is calculated using Manhattan distance.
- Vehicles move at one grid unit per simulation-time unit.
- Traffic and road restrictions are not modeled.
- Charging is not yet a first-class event in the main scheduler.
- Requests that are permanently infeasible remain waiting.
- Visualization is paused while the simulation core is developed.

## Project Goal

The long-term goal is to create a configurable simulation platform for comparing electric-fleet strategies involving:

- dispatch,
- routing,
- charging,
- passenger waiting,
- repositioning,
- fleet sizing,
- energy usage,
- and operational performance.

## License

A license has not yet been added to this repository.