#include "fleet_sim/Vehicle.hpp"

#include <algorithm>
#include <stdexcept>
#include <utility>

namespace fleet_sim
{

Vehicle::Vehicle(
    std::string id,
    const double battery_capacity_kwh,
    const double initial_battery_kwh,
    const int initial_node
)
    : id_(std::move(id)),
      battery_capacity_kwh_(battery_capacity_kwh),
      battery_kwh_(initial_battery_kwh),
      current_node_(initial_node),
      status_(VehicleStatus::Idle)
{
    if (id_.empty())
    {
        throw std::invalid_argument("Vehicle ID cannot be empty");
    }

    if (battery_capacity_kwh_ <= 0.0)
    {
        throw std::invalid_argument(
            "Battery capacity must be greater than zero"
        );
    }

    if (
        battery_kwh_ < 0.0 ||
        battery_kwh_ > battery_capacity_kwh_
    )
    {
        throw std::invalid_argument(
            "Initial battery energy must be between zero and capacity"
        );
    }
}

const std::string& Vehicle::id() const noexcept
{
    return id_;
}

double Vehicle::battery_capacity_kwh() const noexcept
{
    return battery_capacity_kwh_;
}

double Vehicle::battery_kwh() const noexcept
{
    return battery_kwh_;
}

double Vehicle::battery_percentage() const noexcept
{
    return 100.0 * battery_kwh_ / battery_capacity_kwh_;
}

int Vehicle::current_node() const noexcept
{
    return current_node_;
}

VehicleStatus Vehicle::status() const noexcept
{
    return status_;
}

bool Vehicle::is_available() const noexcept
{
    return status_ == VehicleStatus::Idle;
}

void Vehicle::consume_energy(const double energy_kwh)
{
    if (energy_kwh < 0.0)
    {
        throw std::invalid_argument(
            "Energy consumption cannot be negative"
        );
    }

    if (energy_kwh > battery_kwh_)
    {
        throw std::runtime_error(
            "Vehicle does not have enough battery energy"
        );
    }

    battery_kwh_ -= energy_kwh;
}

void Vehicle::charge(const double energy_kwh)
{
    if (energy_kwh < 0.0)
    {
        throw std::invalid_argument(
            "Charging energy cannot be negative"
        );
    }

    battery_kwh_ = std::min(
        battery_kwh_ + energy_kwh,
        battery_capacity_kwh_
    );
}

void Vehicle::move_to(const int destination_node)
{
    current_node_ = destination_node;
}

void Vehicle::set_status(const VehicleStatus status) noexcept
{
    status_ = status;
}

}  // namespace fleet_sim