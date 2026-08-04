#include "fleet_sim/Vehicle.hpp"

#include <gtest/gtest.h>

#include <stdexcept>

using fleet_sim::Vehicle;
using fleet_sim::VehicleStatus;

TEST(VehicleTest, InitializesWithExpectedState)
{
    const Vehicle vehicle(
        "vehicle-1",
        100.0,
        80.0,
        4
    );

    EXPECT_EQ(vehicle.id(), "vehicle-1");
    EXPECT_DOUBLE_EQ(vehicle.battery_capacity_kwh(), 100.0);
    EXPECT_DOUBLE_EQ(vehicle.battery_kwh(), 80.0);
    EXPECT_DOUBLE_EQ(vehicle.battery_percentage(), 80.0);
    EXPECT_EQ(vehicle.current_node(), 4);
    EXPECT_EQ(vehicle.status(), VehicleStatus::Idle);
    EXPECT_TRUE(vehicle.is_available());
}

TEST(VehicleTest, ConsumesEnergy)
{
    Vehicle vehicle(
        "vehicle-1",
        100.0,
        80.0,
        0
    );

    vehicle.consume_energy(15.0);

    EXPECT_DOUBLE_EQ(vehicle.battery_kwh(), 65.0);
}

TEST(VehicleTest, RejectsEnergyConsumptionBeyondBatteryLevel)
{
    Vehicle vehicle(
        "vehicle-1",
        100.0,
        20.0,
        0
    );

    EXPECT_THROW(
        vehicle.consume_energy(25.0),
        std::runtime_error
    );

    EXPECT_DOUBLE_EQ(vehicle.battery_kwh(), 20.0);
}

TEST(VehicleTest, ChargingDoesNotExceedCapacity)
{
    Vehicle vehicle(
        "vehicle-1",
        100.0,
        90.0,
        0
    );

    vehicle.charge(30.0);

    EXPECT_DOUBLE_EQ(vehicle.battery_kwh(), 100.0);
}

TEST(VehicleTest, UpdatesNode)
{
    Vehicle vehicle(
        "vehicle-1",
        100.0,
        80.0,
        2
    );

    vehicle.move_to(7);

    EXPECT_EQ(vehicle.current_node(), 7);
}

TEST(VehicleTest, AvailabilityDependsOnStatus)
{
    Vehicle vehicle(
        "vehicle-1",
        100.0,
        80.0,
        0
    );

    EXPECT_TRUE(vehicle.is_available());

    vehicle.set_status(VehicleStatus::CarryingPassenger);

    EXPECT_FALSE(vehicle.is_available());
}