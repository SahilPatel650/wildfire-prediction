import requests

def get_weather_forecast(latitude, longitude):
    base_url = "https://api.weather.gov/points/{},{}".format(latitude, longitude)

    # Step 1: Get forecast office from the API
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        forecast_office = data['properties']['forecastOffice']

        # Step 2: Get the forecast from the forecast office
        forecast_url = "{}/forecast".format(forecast_office)
        response = requests.get(forecast_url)
        if response.status_code == 200:
            forecast_data = response.json()
            return forecast_data
        else:
            print("Error getting forecast data. Status code:", response.status_code)
    else:
        print("Error getting forecast office. Status code:", response.status_code)

# Example: Get the weather forecast for a specific location
latitude = 37.7749  # Replace with your latitude
longitude = -122.4194  # Replace with your longitude

forecast = get_weather_forecast(latitude, longitude)
if forecast:
    # Display the forecast data
    print("Weather Forecast for {}: {}".format(forecast['properties']['periods'][0]['name'],
                                               forecast['properties']['periods'][0]['detailedForecast']))
