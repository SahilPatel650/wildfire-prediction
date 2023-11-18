import requests
import sys
import json

response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/ventura%20county%20california/2017-12-01/2017-12-31?unitGroup=us&include=days&key=GWL9ETYVUYCUBM8G78QPA4PPG&contentType=json")

if response.status_code != 200:
    print('Unexpected Status code: ', response.status_code)
    sys.exit()

# Parse the results as JSON
jsonData = response.json()

# Specify the file path where you want to save the JSON data
output_file_path = 'output.json'

# Write the JSON data to the file
with open(output_file_path, 'w') as output_file:
    json.dump(jsonData, output_file, indent=2)

print(f"JSON data has been saved to {output_file_path}")
