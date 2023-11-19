import sys
import json
import numpy as np
from weather_data import generate_3d_array

if __name__ == "__main__":
    # Parse the JSON string from the first argument
    grid_data_str = sys.argv[1]
    grid_data = json.loads(grid_data_str)
    #write the grid data to a file
    array_2d = np.zeros((64, 64), dtype=object)

    #dump the data into json file
    with open('grid_data.json', 'w') as outfile:
        json.dump(grid_data, outfile)


    # Convert the JSON data into the 2D array
    for i in range(64):
        for j in range(64):
            # Calculate the index in the 1D data array
            index = i * 64 + j

            # Extract latitude, longitude, and selected from the JSON data
            arr = grid_data[i][j]
            lat = arr['lat']
            lng = arr['lng']
            selected = arr['selected']

            # Create a tuple and assign it to the 2D array
            array_2d[i, j] = (lat, lng, selected)
    
    #load api key from api_key.json
API_KEY = json.load(open('api_key.json'))['ELEVATION_API_KEY']
print(array_2d)

model_input = generate_3d_array(array_2d, API_KEY)
print(model_input)

            