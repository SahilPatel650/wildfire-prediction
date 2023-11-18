import requests
import json

# Define your API key here
API_KEY = "GWL9ETYVUYCUBM8G78QPA4PPG"

def get_weather_data(latitude, longitude, start_date, end_date, fire_id):
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude},{longitude}/{start_date}/{end_date}?key={API_KEY}&unitGroup=us&include=days&contentType=json"

    response = requests.get(base_url)

    if response.status_code != 200:
        print('Unexpected Status code:', response.status_code)
        return None

    # Parse the results as JSON
    weather_data = response.json()

    # Construct the output file name
    output_file = f"{fire_id}-weatherdata.json"

    # Write the JSON data to the specified output file
    with open(output_file, 'w') as output_file:
        json.dump(weather_data, output_file, indent=2)

    print(f"Weather data has been saved to {output_file}")
    return weather_data

def main():
    # Input parameters
    latitude = input("Enter latitude (e.g., 38.9697): ")
    longitude = input("Enter longitude (e.g., -77.385): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    fire_id = input("Enter fire ID: ")

    # Get weather data and save it to the output file
    weather_data = get_weather_data(latitude, longitude, start_date, end_date, fire_id)

    # You can use weather_data in your further processing if needed

if __name__ == "__main__":
    main()
