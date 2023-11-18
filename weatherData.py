import requests
import numpy as np
import random

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

    try:
        elevation_result = elevation_data['results'][0]['elevation']
        return elevation_result
    except (KeyError, IndexError):
        print("Unable to retrieve elevation data.")
        return None

def get_weather_data(latitude, longitude, start_date, end_date):
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

        return extracted_data

    except KeyError as e:
        print(f"KeyError: {e}. Please check the structure of the API response.")
        return None

def generate_3d_array(location_array, start_date, end_date):
    # Define the dimensions of the 3D array
    num_arrays = 7
    array_size = (32, 32)

    # Create a 3D NumPy array filled with zeros
    three_d_array = np.zeros((num_arrays,) + array_size)

    # Iterate over each cell in the location array
    for i in range(len(location_array)):
        for j in range(len(location_array[i])):
            coordinates = location_array[i][j]

            if coordinates is not None:
                # If coordinates are present, fetch weather data and update the 7 32x32 arrays
                weather_data = get_weather_data(coordinates[0], coordinates[1], start_date, end_date)

                if weather_data is not None:
                    for k, key in enumerate(["elevation", "winddir", "windspeed", "tempmin", "tempmax", "humidity", "precip"]):
                        three_d_array[k, i, j] = weather_data[key]
            else:
                # If coordinates are not present, set all values in the 7 32x32 arrays to 0
                three_d_array[:, i, j] = 0

    return three_d_array

def generate_test_array():
    test_array = []

    for _ in range(32):
        row = []
        for _ in range(32):
            if random.choice([True, False]):
                # Randomly decide whether to include coordinates or None
                latitude = random.uniform(-90, 90)
                longitude = random.uniform(-180, 180)
                row.append((latitude, longitude))
            else:
                row.append(None)
        test_array.append(row)

    return test_array

# Example usage:
test_location_array = [
    [None, (38.9697, -77.385), None, None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, (38.9697, -77.385), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    # ... (the rest of the 32x32 array)
]

start_date = "2023-01-01"
end_date = "2023-01-31"
#test_location_array = generate_test_array()
resulting_3d_array = generate_3d_array(test_location_array, start_date, end_date)
print(f"Elevation at specified location: {resulting_3d_array[0, 0, 1]}")
