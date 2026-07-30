# Electric Fleet Simulator

A Python-based electric vehicle fleet simulator for exploring vehicle movement, passenger trips, battery feasibility, charging behavior, fleet orchestration, and optimization algorithms.

The project is being developed incrementally to build a strong understanding of simulation architecture, state management, testing, performance analysis, and real-world electric fleet operations.

## Current Features

- Simulates a vehicle moving through a two-dimensional grid
- Tracks simulation time at each movement step
- Models passenger pickup and drop-off locations
- Tracks vehicle operating states:
  - `idle`
  - `to_pickup`
  - `with_passenger`
  - `to_charger`
  - `charging`
  - `stranded`
- Calculates Manhattan distance between locations
- Tracks battery consumption during vehicle movement
- Determines whether a vehicle has enough battery to:
  - Reach the passenger
  - Complete the passenger trip
  - Reach a charging station afterward
- Redirects low-battery vehicles to a charging station
- Detects when a vehicle cannot reach a charging station
- Charges vehicles at a configurable rate
- Prevents charging beyond the configured target level

## Simulation Flow

The current simulation follows this decision process:

```text
Vehicle starts idle
        |
        v
Calculate required battery
        |
        v
Is the passenger trip feasible?
       / \
     Yes  No
      |    |
      |    v
      |  Can the vehicle reach a charger?
      |        / \
      |      Yes  No
      |       |    |
      |       |    v
      |       |  Vehicle becomes stranded
      |       v
      |   Drive to charging station
      |       |
      |       v
      |   Charge to target level
      |       |
      |       v
      |   Return to idle
      |
      v
Drive to passenger
      |
      v
Complete passenger trip
      |
      v
Return to idle


Electric-Fleet-Simulator/
├── .github/
│   └── workflows/       # CI workflows
├── analysis/            # Simulation result analysis
├── benchmarks/          # Runtime and performance benchmarks
├── configs/             # Simulation configuration files
├── data/                # Input and reference datasets
├── docs/                # Project documentation
├── src/
│   └── fleet_sim/
│       └── simulator.py
├── tests/               # Automated tests
├── README.md
└── pyproject.toml
