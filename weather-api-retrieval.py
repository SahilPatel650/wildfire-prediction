import requests

api_key = 'YOUR_API_KEY'
city = 'New York'  # Or specify coordinates (latitude and longitude)

base_url = 'http://api.openweathermap.org/data/2.5/weather?'

complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

response = requests.get(complete_url)

data = response.json()

if response.status_code == 200:
    # Extract data from the JSON response
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    weather_description = data['weather'][0]['description']
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Weather: {weather_description}")
else:
    print("Error fetching data")
