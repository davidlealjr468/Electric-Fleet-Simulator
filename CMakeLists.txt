cmake_minimum_required(VERSION 3.20)

project(
    ElectricFleetSimulator
    VERSION 0.1.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(FLEET_SIM_BUILD_TESTS "Build the C++ test suite" ON)

if(FLEET_SIM_BUILD_TESTS)
    enable_testing()
endif()

add_subdirectory(cpp)