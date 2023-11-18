import requests
import sys

import json
                

response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/ventura%20county%20california/2017-12-01/2017-12-31?unitGroup=us&include=days&key=GWL9ETYVUYCUBM8G78QPA4PPG&contentType=json")
if response.status_code!=200:
  print('Unexpected Status code: ', response.status_code)
  sys.exit()  


# Parse the results as JSON
jsonData = response.json()
        
