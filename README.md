# Electric Fleet Simulator

## Overview

The Electric Fleet Simulator is a Python-based simulation project for modeling the operation of electric transportation fleets.

The simulator evaluates how electric vehicles:

- travel across a grid,
- serve passenger requests,
- consume battery energy,
- determine whether trips are feasible,
- select charging stations,
- recharge when battery levels are low,
- and transition between operational states.

The project is being developed incrementally to explore simulation architecture, electric-vehicle fleet operations, optimization algorithms, pathfinding, automated testing, performance analysis, and data-driven validation.

The long-term goal is to create a configurable fleet simulation platform capable of comparing vehicle-assignment, routing, charging, and repositioning strategies.

---

## Current Timeline

### Version 1 — Core Vehicle Simulation

1. **[Completed]** Create a two-dimensional grid-based simulation
2. **[Completed]** Implement Manhattan-distance calculations
3. **[Completed]** Add vehicle movement and simulation-time tracking
4. **[Completed]** Add battery consumption during movement
5. **[Completed]** Add passenger pickup and drop-off locations
6. **[Completed]** Add trip battery-feasibility calculations
7. **[Completed]** Add vehicle charging behavior
8. **[Completed]** Add multiple charging stations
9. **[Completed]** Select the nearest charging station
10. **[Completed]** Add charging-station input validation
11. **[Completed]** Add automated tests with `pytest`
12. **[Completed]** Split the simulator into focused Python modules
13. **[Completed]** Add a reusable `Vehicle` dataclass
14. **[Completed]** Update vehicle movement to operate on the `Vehicle` model
15. **[Completed]** Add a `PassengerRequest` dataclass
16. **[In Progress]** Integrate passenger-request state throughout the simulator

### Version 2 — Multi-Vehicle Fleet Operations

1. **[Planned]** Add a `ChargingStation` dataclass
2. **[Planned]** Support multiple vehicles
3. **[Planned]** Support multiple passenger requests
4. **[Planned]** Add vehicle-to-request assignment
5. **[Planned]** Track request waiting times
6. **[Planned]** Add rejected and cancelled request states
7. **[Planned]** Add charging-station capacity
8. **[Planned]** Add charging queues
9. **[Planned]** Add fleet-level operational metrics
10. **[Planned]** Save structured simulation event logs

### Version 3 — Routing and Optimization

1. **[Planned]** Add road obstacles and restricted grid cells
2. **[Planned]** Represent the road network as a graph
3. **[Planned]** Implement Dijkstra’s shortest-path algorithm
4. **[Planned]** Implement A* pathfinding
5. **[Planned]** Compare pathfinding runtime and solution quality
6. **[Planned]** Add weighted travel costs
7. **[Planned]** Add traffic-aware routing
8. **[Planned]** Add energy-aware route planning
9. **[Planned]** Add fleet repositioning strategies
10. **[Planned]** Compare greedy and optimization-based assignment methods

### Version 4 — Data, Analysis, and Validation

1. **[Planned]** Load simulation scenarios from configuration files
2. **[Planned]** Load vehicle, request, and station data from CSV files
3. **[Planned]** Generate random passenger demand
4. **[Planned]** Add reproducible simulation seeds
5. **[Planned]** Run Monte Carlo experiments
6. **[Planned]** Analyze passenger waiting-time distributions
7. **[Planned]** Analyze battery and charging behavior
8. **[Planned]** Compare fleet policies statistically
9. **[Planned]** Profile runtime and memory consumption
10. **[Planned]** Validate the simulator against transportation datasets

---

## Current Capabilities

The current simulator supports:

- one electric vehicle,
- one passenger request,
- multiple charging stations,
- grid-based vehicle movement,
- Manhattan-distance calculations,
- simulation-time tracking,
- battery consumption,
- passenger-trip feasibility checks,
- nearest charging-station selection,
- low-battery routing,
- configurable charging rates,
- configurable charging targets,
- stranded-vehicle detection,
- vehicle and passenger state models,
- automated unit tests,
- formatting and linting,
- continuous integration.

---

## Simulation Flow

The simulator first determines the nearest charging station and calculates the energy required to:

1. reach the passenger,
2. complete the passenger trip,
3. reach a charging station afterward.

```text
Vehicle starts idle
        |
        v
Find nearest charging station
        |
        v
Calculate total required battery
        |
        v
Can the vehicle safely complete the trip?
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
      |   Travel to charging station
      |       |
      |       v
      |   Charge to target level
      |       |
      |       v
      |   Return to idle
      |
      v
Travel to passenger
      |
      v
Pick up passenger
      |
      v
Travel to drop-off
      |
      v
Complete request
      |
      v
Return to idle
