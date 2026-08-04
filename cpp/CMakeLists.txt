add_library(
    electric_fleet_core
    src/Vehicle.cpp
)

target_include_directories(
    electric_fleet_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_features(
    electric_fleet_core
    PUBLIC
        cxx_std_20
)

if(MSVC)
    target_compile_options(
        electric_fleet_core
        PRIVATE
            /W4
            /permissive-
    )
else()
    target_compile_options(
        electric_fleet_core
        PRIVATE
            -Wall
            -Wextra
            -Wpedantic
            -Wconversion
            -Wshadow
    )
endif()

add_executable(
    fleet_cli
    apps/fleet_cli/main.cpp
)

target_link_libraries(
    fleet_cli
    PRIVATE
        electric_fleet_core
)

if(FLEET_SIM_BUILD_TESTS)
    include(FetchContent)

    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG v1.17.0
    )

    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

    FetchContent_MakeAvailable(googletest)

    enable_testing()

    add_executable(
        fleet_cpp_tests
        tests/test_vehicle.cpp
    )

    target_link_libraries(
        fleet_cpp_tests
        PRIVATE
            electric_fleet_core
            GTest::gtest_main
    )

    include(GoogleTest)

    gtest_discover_tests(fleet_cpp_tests)
endif()