from datetime import datetime
from typing import List, Dict, Tuple
import json
import math

# Sample routing engine without a connected backend

def get_route(driver_coords: Tuple[float, float], remaining_capacity: int, destination_coords: Tuple[float, float], locations: List[Dict], time_weight: float, distance_weight: float) -> List[Dict]:
    filtered_locations = [loc for loc in locations if loc["partySize"] <= remaining_capacity]
    
    coordinates = [driver_coords] + [loc["coordinates"] for loc in filtered_locations] + [destination_coords]
    
    distance_matrix = get_distance_matrix(coordinates)
    
    scores = []
    for idx, loc in enumerate(filtered_locations):
        time_score = (parse_time(loc["requestTime"]) - parse_time(filtered_locations[0]["requestTime"])).total_seconds()
        distance_score = distance_matrix[0][idx + 1]
        score = time_weight * time_score + distance_weight * distance_score
        scores.append((score, loc))
    
    sorted_locations = [loc for _, loc in sorted(scores, key=lambda x: x[0])]
    
    route = []
    current_capacity = remaining_capacity
    
    for loc in sorted_locations:
        party_size = loc["partySize"]
        if party_size <= current_capacity:
            route.append(loc["coordinates"])
            current_capacity -= party_size
    
    # Append the destination coordinates to the route
    route.append(destination_coords)
    
    return route

def get_distance_matrix(locations: List[Tuple[float, float]]) -> List[List[float]]:
    n = len(locations)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            matrix[i][j] = haversine(locations[i], locations[j])
    
    return matrix

def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the great-circle distance between two points on the Earth using the Haversine formula.
    
    Parameters:
    coord1 (Tuple[float, float]): Latitude and longitude of the first point in decimal degrees.
    coord2 (Tuple[float, float]): Latitude and longitude of the second point in decimal degrees.
    
    Returns:
    float: Distance between the two points in kilometers.
    """
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    
    return distance

def parse_time(request_time: str) -> datetime:
    return datetime.fromisoformat(request_time)

driver_coords = (37.7749, -122.4194)
remaining_capacity = 5
destination_coords = (37.8583, -122.3308)
time_weight = 0.5  # Example weight for time
distance_weight = 0.5  # Example weight for distance

# Load data from JSON file
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
    route = get_route(driver_coords, remaining_capacity, destination_coords, data["locations"], time_weight, distance_weight)
    print("\nRoute:")
    for idx, stop in enumerate(route):
        print(f"Stop {idx + 1}: {stop}")
else:
    print("Failed to load location data.")
