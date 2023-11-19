import sys
import json
import numpy as np
from weather_data import generate_3d_array
from api_cache import get_elevation

if __name__ == "__main__":
    API_KEY = json.load(open('api_key.json'))['ELEVATION_API_KEY']
    # Parse the JSON string from the first argument
    grid_data_str = sys.argv[1]
    grid_data = json.loads(grid_data_str)
    #create a 3d array
    three_d_array = np.zeros((64, 64, 2))


    #dump the data into json file
    with open('grid_data.json', 'w') as outfile:
        json.dump(grid_data, outfile)


    # Convert the JSON data into the 2D array
    for i in range(64):
        for j in range(64):
            # Extract latitude, longitude, and selected from the JSON data
            arr = grid_data[i][j]
            lat = arr['lat']
            lng = arr['lng']
            # if (lat is None) or (lng is None):
            #     #try getting the data from an adjacent cell
            #     if i == 0:
            #         lat = grid_data[i+1][j]['lat']
            #         lng = grid_data[i+1][j]['lng']
            #     elif i == 63:
            #         lat = grid_data[i-1][j]['lat']
            #         lng = grid_data[i-1][j]['lng']
            #     elif j == 0:
            #         lat = grid_data[i-2][j]['lat']
            #         lng = grid_data[i-2][j]['lng']
            #     elif j == 63:
            #         lat = grid_data[i-2][j]['lat']
            #         lng = grid_data[i-2][j]['lng']
            #     else:
            #         lat = grid_data[i-1][j]['lat']
            #         lng = grid_data[i-1][j]['lng']

            selected = arr['selected']
            print(i, j, lat, lng, selected)
            weather_data = get_elevation(lat, lng, API_KEY)
            three_d_array[i, j, 0] = weather_data
            three_d_array[i, j, 1] = selected


            # Create a tuple and assign it to the 2D array

print(three_d_array)
    #load api key from api_key.json


            