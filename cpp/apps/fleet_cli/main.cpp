#include "fleet_sim/Vehicle.hpp"

#include <exception>
#include <iostream>

int main()
{
    try
    {
        fleet_sim::Vehicle vehicle(
            "vehicle-1",
            100.0,
            85.0,
            0
        );

        vehicle.consume_energy(12.5);
        vehicle.move_to(3);

        std::cout
            << "Vehicle: " << vehicle.id() << '\n'
            << "Current node: " << vehicle.current_node() << '\n'
            << "Battery: "
            << vehicle.battery_percentage()
            << "%\n";

        return 0;
    }
    catch (const std::exception& error)
    {
        std::cerr
            << "Fleet simulation error: "
            << error.what()
            << '\n';

        return 1;
    }
}