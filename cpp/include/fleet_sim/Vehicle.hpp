#pragma once

#include <string>

namespace fleet_sim 
{

enum class VehicleStatus
{
    Idle,
    DrivingToPassenger,
    CarryingPassenger,
    DrivingToCharger,
    Charging
};

class Vehicle
{
public:
    Vehicle(
        std::string id,
        double battery_capacity_kwh,
        double initial_battery_kwh,
        int initial_node
    );

    [[nodiscard]] const std::string& id() const noexcept;
    [[nodiscard]] double battery_capacity_kwh() const noexcept;
    [[nodiscard]] double battery_kwh() const noexcept;
    [[nodiscard]] double battery_percentage() const noexcept;
    [[nodiscard]] int current_node() const noexcept;
    [[nodiscard]] VehicleStatus status() const noexcept;
    [[nodiscard]] bool is_available() const noexcept;

    void consume_energy(double energy_kwh);
    void charge(double energy_kwh);
    void move_to(int destination_node);

    void set_status(VehicleStatus status) noexcept;

private:
    std::string id_;
    double battery_capacity_kwh_;
    double battery_kwh_;
    int current_node_;
    VehicleStatus status_;
};

} //namespace fleet_sim