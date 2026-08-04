#include "fleet_sim/ChargingStation.hpp"

#include <gtest/gtest.h>

#include <stdexcept>

using fleet_sim::ChargingStation;

TEST(ChargingStationTest, InitializesWithExpectedState)
{
    const ChargingStation station(
        "station-1",
        10,
        2,
        50.0
    );

    EXPECT_EQ(station.id(), "station-1");
    EXPECT_EQ(station.node(), 10);
    EXPECT_EQ(station.capacity(), 2);
    EXPECT_DOUBLE_EQ(
        station.charging_rate_kwh_per_hour(),
        50.0
    );

    EXPECT_EQ(station.active_vehicle_count(), 0);
    EXPECT_EQ(station.waiting_vehicle_count(), 0);
    EXPECT_TRUE(station.has_available_charger());
}

TEST(ChargingStationTest, AssignsVehicleToAvailableCharger)
{
    ChargingStation station(
        "station-1",
        10,
        2,
        50.0
    );

    station.request_charging("vehicle-1");

    EXPECT_TRUE(
        station.is_vehicle_charging("vehicle-1")
    );
    EXPECT_EQ(station.active_vehicle_count(), 1);
    EXPECT_EQ(station.waiting_vehicle_count(), 0);
}

TEST(ChargingStationTest, QueuesVehicleWhenStationIsFull)
{
    ChargingStation station(
        "station-1",
        10,
        1,
        50.0
    );

    station.request_charging("vehicle-1");
    station.request_charging("vehicle-2");

    EXPECT_TRUE(
        station.is_vehicle_charging("vehicle-1")
    );

    EXPECT_TRUE(
        station.is_vehicle_waiting("vehicle-2")
    );

    EXPECT_EQ(station.active_vehicle_count(), 1);
    EXPECT_EQ(station.waiting_vehicle_count(), 1);
    EXPECT_FALSE(station.has_available_charger());
}

TEST(ChargingStationTest, PromotesWaitingVehicleAfterCompletion)
{
    ChargingStation station(
        "station-1",
        10,
        1,
        50.0
    );

    station.request_charging("vehicle-1");
    station.request_charging("vehicle-2");

    station.complete_charging("vehicle-1");

    EXPECT_FALSE(
        station.is_vehicle_charging("vehicle-1")
    );

    EXPECT_TRUE(
        station.is_vehicle_charging("vehicle-2")
    );

    EXPECT_FALSE(
        station.is_vehicle_waiting("vehicle-2")
    );

    EXPECT_EQ(station.active_vehicle_count(), 1);
    EXPECT_EQ(station.waiting_vehicle_count(), 0);
}

TEST(ChargingStationTest, RejectsDuplicateVehicle)
{
    ChargingStation station(
        "station-1",
        10,
        1,
        50.0
    );

    station.request_charging("vehicle-1");

    EXPECT_THROW(
        station.request_charging("vehicle-1"),
        std::invalid_argument
    );
}

TEST(ChargingStationTest, RejectsCompletionForInactiveVehicle)
{
    ChargingStation station(
        "station-1",
        10,
        1,
        50.0
    );

    EXPECT_THROW(
        station.complete_charging("vehicle-1"),
        std::invalid_argument
    );
}
