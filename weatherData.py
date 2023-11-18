import requests
import json

# Define your Google Elevation API key here
ELEVATION_API_KEY = "AIzaSyAhtNZsHIYxwfy2Ms5-lxAa9v-tOA_hF78"

# Define your Visual Crossing API key here
VISUAL_CROSSING_API_KEY = "GWL9ETYVUYCUBM8G78QPA4PPG"

def get_elevation(latitude, longitude):
    elevation_url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={ELEVATION_API_KEY}"
    elevation_response = requests.get(elevation_url)
    
    if elevation_response.status_code != 200:
        print('Unexpected Elevation API Status code:', elevation_response.status_code)
        return None

    elevation_data = elevation_response.json()
    print("Elevation API Response:", elevation_data)

    try:
        elevation_result = elevation_data['results'][0]['elevation']
        return elevation_result
    except (KeyError, IndexError):
        print("Unable to retrieve elevation data.")
        return None

def get_weather_data(latitude, longitude, start_date, end_date, fire_id):
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
            "datetime": weather_data['days'][0]['datetime'],
            "tempmax": weather_data['days'][0]['tempmax'],
            "tempmin": weather_data['days'][0]['tempmin'],
            "temp": weather_data['days'][0]['temp'],
            "humidity": weather_data['days'][0]['humidity'],
            "precip": weather_data['days'][0]['precip'],
            "windspeed": weather_data['days'][0]['windspeed'],
            "winddir": weather_data['days'][0]['winddir'],
            "elevation": get_elevation(latitude, longitude)
        }

        print("Extracted Weather Data:", extracted_data)

        return extracted_data

    except KeyError as e:
        print(f"KeyError: {e}. Please check the structure of the API response.")
        return None