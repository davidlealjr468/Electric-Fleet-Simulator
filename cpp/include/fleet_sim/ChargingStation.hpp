#pragma once

#include <cstddef>
#include <deque>
#include <string>
#include <vector>

namespace fleet_sim
{

class ChargingStation
{
public:
    ChargingStation(
        std::string id,
        int node,
        std:: size_t capacity,
        double charging_rate_kwh_per_hour
    );

    [[nodiscard]] const std::string& id() const noexcept;
    [[nodiscard]] int node() const noexcept;
    [[nodiscard]] std::size_t capacity() const noexcept;
    [[nodiscard]] double charging_rate_kwh_per_hour() const noexcept;

    [[nodiscard]] std::size_t active_vehicle_count() const noexcept;
    [[nodiscard]] std::size_t waiting_vehicle_count() const noexcept;

    [[nodiscard]] bool has_available_charger() const noexcept;
    [[nodiscard]] bool is_vehicle_charging(
        const std::string& vehicle_id
    ) const;

    [[nodiscard]] bool is_vehicle_waiting(
        const std::string& vehicle_id
    ) const;

    void request_charging(const std::string& vehicle_id);
    void complete_charging(const std::string& vehicle_id);

    [[nodiscard]] const std::vector<std::string>& 
    active_vehicles() const noexcept;

private:
    std::string id_;
    int node_;
    std::size_t capacity_;
    double charging_rate_kwh_per_hour_;

    std::vector<std::string> active_vehicles_;
    std::deque<std::string> waiting_vehicles_;

    [[nodiscard]] bool contains_vehicle(
        const std:: string& vehicle_id
    ) const;

    void promote_waiting_vehicle();
};

} //namespace fleet_sim