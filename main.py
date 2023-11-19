import sys
import json
import numpy as np
from weather_data import generate_3d_array

if __name__ == "__main__":
    # Parse the JSON string from the first argument
    grid_data_str = sys.argv[1]
    grid_data = json.loads(grid_data_str)
    #write the grid data to a file

    # Convert the JSON data into the 2D array
    for i in range(64):
        for j in range(64):
            # Calculate the index in the 1D data array
            index = i * 64 + j

            # Extract latitude, longitude, and selected from the JSON data
            lat = grid_data[index]['lat']
            lng = grid_data[index]['lng']
            selected = grid_data[index]['selected']

            # Create a tuple and assign it to the 2D array
            array_2d[i, j] = (lat, lng, selected)
    
    model_input = generate_3d_array(array_2d)
    print(model_input)

            