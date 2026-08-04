#include "fleet_sim/ChargingStation.hpp"

#include <algorithm>
#include <stdexcept>
#include <utility>

namespace fleet_sim
{

ChargingStation::ChargingStation(
    std::string id,
    const int node,
    const std::size_t capacity,
    const double charging_rate_kwh_per_hour
)
    : id_(std::move(id)),
      node_(node),
      capacity_(capacity),
      charging_rate_kwh_per_hour_(charging_rate_kwh_per_hour)
{
    if (id_.empty())
    {
        throw std::invalid_argument(
            "Charging-station ID cannot be empty"
        );
    }

    if (capacity_ == 0)
    {
        throw std::invalid_argument(
            "Charging-station capacity must be greater than zero"
        );
    }

    if (charging_rate_kwh_per_hour_ <= 0.0)
    {
        throw std::invalid_argument(
            "Charging rate must be greater than zero"
        );
    }
}

const std::string& ChargingStation::id() const noexcept
{
    return id_;
}

int ChargingStation::node() const noexcept
{
    return node_;
}

std::size_t ChargingStation::capacity() const noexcept
{
    return capacity_;
}

double ChargingStation::charging_rate_kwh_per_hour() const noexcept
{
    return charging_rate_kwh_per_hour_;
}

std::size_t ChargingStation::active_vehicle_count() const noexcept
{
    return active_vehicles_.size();
}

std::size_t ChargingStation::waiting_vehicle_count() const noexcept
{
    return waiting_vehicles_.size();
}

bool ChargingStation::has_available_charger() const noexcept
{
    return active_vehicles_.size() < capacity_;
}

bool ChargingStation::is_vehicle_charging(
    const std::string& vehicle_id
) const
{
    return std::find(
        active_vehicles_.begin(),
        active_vehicles_.end(),
        vehicle_id
    ) != active_vehicles_.end();
}

bool ChargingStation::is_vehicle_waiting(
    const std::string& vehicle_id
) const
{
    return std::find(
        waiting_vehicles_.begin(),
        waiting_vehicles_.end(),
        vehicle_id
    ) != waiting_vehicles_.end();
}

void ChargingStation::request_charging(
    const std::string& vehicle_id
)
{
    if (vehicle_id.empty())
    {
        throw std::invalid_argument(
            "Vehicle ID cannot be empty"
        );
    }

    if (contains_vehicle(vehicle_id))
    {
        throw std::invalid_argument(
            "Vehicle is already registered at this station"
        );
    }

    if (has_available_charger())
    {
        active_vehicles_.push_back(vehicle_id);
        return;
    }

    waiting_vehicles_.push_back(vehicle_id);
}

void ChargingStation::complete_charging(
    const std::string& vehicle_id
)
{
    const auto vehicle = std::find(
        active_vehicles_.begin(),
        active_vehicles_.end(),
        vehicle_id
    );

    if (vehicle == active_vehicles_.end())
    {
        throw std::invalid_argument(
            "Vehicle is not actively charging"
        );
    }

    active_vehicles_.erase(vehicle);
    promote_waiting_vehicle();
}

const std::vector<std::string>&
ChargingStation::active_vehicles() const noexcept
{
    return active_vehicles_;
}

bool ChargingStation::contains_vehicle(
    const std::string& vehicle_id
) const
{
    return is_vehicle_charging(vehicle_id) ||
           is_vehicle_waiting(vehicle_id);
}

void ChargingStation::promote_waiting_vehicle()
{
    if (
        waiting_vehicles_.empty() ||
        !has_available_charger()
    )
    {
        return;
    }

    active_vehicles_.push_back(waiting_vehicles_.front());
    waiting_vehicles_.pop_front();
}

}  // namespace fleet_sim