import requests
import json
import os
import numpy as np


def relative_humidity_to_specific_humidity(temp_celsius, relative_humidity):
    # Constants for the Magnus-Tetens approximation
    A = 17.625
    B = 243.04  # in degrees Celsius

    # Calculate saturation vapor pressure in hPa
    E_s = 6.112 * np.exp(A * temp_celsius / (B + temp_celsius))

    # Calculate actual vapor pressure
    E = (relative_humidity / 100) * E_s

    # Convert to specific humidity in kg/kg
    # Using approximation: q ≈ 0.622 * E / (P - E)
    # Assuming standard atmospheric pressure P = 1013.25 hPa
    P = 1013.25  # in hPa
    q = 0.622 * E / (P - E)

    return q


def get_elevation(latitude, longitude, ELEVATION_API_KEY):
    cache_file = './weather_cache/elevation.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            cache = json.load(file)
    else:
        cache = {}
    
    cache_key = f"{latitude},{longitude}"

    # Check if data is in cache
    if cache_key in cache:
        print("Fetching from cache")
        return cache[cache_key]


    elevation_url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={ELEVATION_API_KEY}"
    elevation_response = requests.get(elevation_url)
    
    if elevation_response.status_code != 200:
        print('Unexpected Elevation API Status code:', elevation_response.status_code)
        return None

    elevation_data = elevation_response.json()

    try:
        elevation_result = elevation_data['results'][0]['elevation']
        cache[cache_key] = elevation_result
        with open(cache_file, 'w') as file:
            json.dump(cache, file)

        return elevation_result

    except (KeyError, IndexError):
        print("Unable to retrieve elevation data.")
        return None


def get_weather_data(latitude, longitude, start_date, end_date, VISUAL_CROSSING_API_KEY):

    cache_file = './weather_cache/visualcrossing.json'
    # Load existing cache data
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            cache = json.load(file)
    else:
        cache = {}

    # Cache key based on latitude and longitude
    cache_key = f"{latitude},{longitude}"

    # Check if data is in cache
    if cache_key in cache:
        print("Fetching from cache")
        return cache[cache_key]

    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude},{longitude}/{start_date}/{end_date}?key={VISUAL_CROSSING_API_KEY}&unitGroup=metric&include=days&contentType=json"

    response = requests.get(base_url)

    if response.status_code != 200:
        print('Unexpected Status code:', response.status_code)
        return None

    # Parse the results as JSON
    weather_data = response.json()

    try:
        # Extract the desired fields from the API response
        extracted_data = {
            "elevation": get_elevation(latitude, longitude)
        }

        cache[cache_key] = extracted_data
        with open(cache_file, 'w') as file:
            json.dump(cache, file)

        return extracted_data

    except KeyError as e:
        print(f"KeyError: {e}. Please check the structure of the API response.")
        return None

# def main():
#     # data = get_weather_data(33.77162950463133, -84.39199233135656, "2023-11-17", "2023-11-17")
#     print(relative_humidity_to_specific_humidity(21, 78))

# main()