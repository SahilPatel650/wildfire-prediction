import requests
import json
import os
# Define your Google Elevation API key here
ELEVATION_API_KEY = "AIzaSyAhtNZsHIYxwfy2Ms5-lxAa9v-tOA_hF78"

# Define your Visual Crossing API key here
VISUAL_CROSSING_API_KEY = "K47XQXT3QH58XJ6863YB5VAL4"


def get_elevation(latitude, longitude):
    elevation_url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={ELEVATION_API_KEY}"
    elevation_response = requests.get(elevation_url)
    
    if elevation_response.status_code != 200:
        print('Unexpected Elevation API Status code:', elevation_response.status_code)
        return None

    elevation_data = elevation_response.json()

    try:
        elevation_result = elevation_data['results'][0]['elevation']
        return elevation_result
    except (KeyError, IndexError):
        print("Unable to retrieve elevation data.")
        return None


def get_weather_data(latitude, longitude, start_date, end_date):

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

    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude},{longitude}/{start_date}/{end_date}?key={VISUAL_CROSSING_API_KEY}&unitGroup=us&include=days&contentType=json"

    response = requests.get(base_url)

    if response.status_code != 200:
        print('Unexpected Status code:', response.status_code)
        return None

    # Parse the results as JSON
    weather_data = response.json()

    try:
        # Extract the desired fields from the API response
        extracted_data = {
            "elevation": get_elevation(latitude, longitude),
            "winddir": weather_data['days'][0]['winddir'],
            "windspeed": weather_data['days'][0]['windspeed'],
            "tempmin": weather_data['days'][0]['tempmin'],
            "tempmax": weather_data['days'][0]['tempmax'],
            "humidity": weather_data['days'][0]['humidity'],
            "precip": weather_data['days'][0]['precip'],
        }

        cache[cache_key] = extracted_data
        with open(cache_file, 'w') as file:
            json.dump(cache, file)

        return extracted_data

    except KeyError as e:
        print(f"KeyError: {e}. Please check the structure of the API response.")
        return None
