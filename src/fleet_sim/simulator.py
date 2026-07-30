# This is the base version of the electric fleet simulator.



current_time = 0

#Vehicles State
vehicle_x = 0
vehicle_y = 0
vehicle_id = 1
vehicle_battery = 100
vehicle_status = "idle"

#Passenger pickup and drop-off locations
pickup_x = 7
pickup_y = 6


dropoff_x = 8
dropoff_y = 7

#Charging Station location
charging_station_x = 4
charging_station_y = 2


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def move_vehicle_to(
        vehicle_x,
        vehicle_y,
        target_x,
        target_y,
        current_time,
        vehicle_battery,
):

    while target_x > vehicle_x: 
        vehicle_x += 1
        current_time += 1
        vehicle_battery -= 1
        print(f"Time {current_time}: vehicle moved right to ({vehicle_x}, {vehicle_y})")

    while target_x < vehicle_x: 
        vehicle_x -= 1
        current_time += 1
        vehicle_battery -= 1
        print(f"Time {current_time}: vehicle moved left to ({vehicle_x}, {vehicle_y})")

    while target_y > vehicle_y:
        vehicle_y += 1
        current_time += 1
        vehicle_battery -= 1
        print(f"Time {current_time}: vehicle moved up to ({vehicle_x}, {vehicle_y})")

    while target_y < vehicle_y:
        vehicle_y -= 1
        current_time += 1
        vehicle_battery -= 1
        print(f"Time {current_time}: vehicle moved down to ({vehicle_x}, {vehicle_y})")

    return vehicle_x, vehicle_y, current_time, vehicle_battery


vehicle_status = "to_pickup"

vehicle_x, vehicle_y, current_time, vehicle_battery = move_vehicle_to(
    vehicle_x,
    vehicle_y,
    pickup_x,
    pickup_y,
    current_time,
    vehicle_battery,
)

print("The vehicle reached the passenger.")

vehicle_status = "with_passenger"

vehicle_x, vehicle_y, current_time, vehicle_battery = move_vehicle_to(
    vehicle_x,
    vehicle_y,
    dropoff_x,
    dropoff_y,
    current_time,
    vehicle_battery,
)

print("The passenger reached the drop-off location.")
vehicle_status = "idle"


distance_to_charger = manhattan_distance(
    vehicle_x, 
    vehicle_y, 
    charging_station_x, 
    charging_station_y
)

print(f"Time: {current_time}")
print(f"Vehicle position: ({vehicle_x}, {vehicle_y})")
print(f"Vehicle Status: {vehicle_status}")
print(f"Battery Level: {vehicle_battery}")
print(f"Distance to charging station: {distance_to_charger}")
print(f"Charging station position: ({charging_station_x}, {charging_station_y})")
