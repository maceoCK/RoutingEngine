from datetime import datetime
from typing import List, Dict, Tuple
import json

# Sample routing engine without a connected backend

def get_route(driver_coords: Tuple[float, float], remaining_capacity: int, destination_coords: Tuple[float, float], locations: List[Dict]) -> List[Dict]:
    # Filter locations that can fit within the remaining capacity
    filtered_locations = [loc for loc in locations if loc["partySize"] <= remaining_capacity]
    
    # Sort locations by request time
    sorted_locations = sorted(filtered_locations, key=lambda x: parse_time(x["requestTime"]))
    
    # Initialize the route and track the current capacity
    route = []
    current_capacity = remaining_capacity
    
    for loc in sorted_locations:
        party_size = loc["partySize"]
        if party_size <= current_capacity:
            route.append((loc["coordinates"], loc["partySize"]))
            current_capacity -= party_size
    
    # Append the destination coordinates to the route if provided
    if destination_coords:
        route.append(destination_coords)
    
    return route

def parse_time(request_time: str) -> datetime:
    return datetime.fromisoformat(request_time)

driver_coords = (37.7749, -122.4194)
remaining_capacity = 5
destination_coords = (37.8583, -122.3308)

try:
    with open("exampleLocations.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    print("The file exampleLocations.json was not found.")
    data = None
except json.JSONDecodeError:
    print("The file exampleLocations.json is not a valid JSON.")
    data = None

if data:
    route = get_route(driver_coords, remaining_capacity, destination_coords, data["locations"])
    print("\nRoute:")
    for idx, stop in enumerate(route):
        print(f"Stop {idx + 1}: {stop}")
else:
    print("Failed to load location data.")
