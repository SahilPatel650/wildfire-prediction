import numpy as np
import random
from api_cache import get_elevation

def generate_3d_array(location_array, API_KEY):
    num_arrays = 2
    array_size = (64, 64)

    # Create a 3D NumPy array filled with zeros
    three_d_array = np.zeros((num_arrays,) + array_size)

    # Iterate over each cell in the location array
    for i in range(len(location_array)):
        for j in range(len(location_array[i])):
            
            coordinates = location_array[i][j]
            if coordinates is not None:
                print(coordinates)
                # If coordinates are present, fetch weather data and update the 7 32x32 arrays
                elevation_data = get_elevation(coordinates[0], coordinates[1], API_KEY)
                clicked_data = coordinates[2] or False

                if elevation_data is not None:
                    three_d_array[i, j, 0] = elevation_data
                if clicked_data is not None:
                    three_d_array[i,j,1] = clicked_data
            else:
                # If coordinates are not present, set all values in the 32x32 arrays to 0
                three_d_array[i, j, :] = 0

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
    [None, (38.9697, -77.385, False), None, None, (38.9697, -77.385, False), None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    
]

start_date = "2023-01-01"
end_date = "2023-01-31"
#test_location_array = generate_test_array()

resulting_3d_array = generate_3d_array(test_location_array, "AIzaSyAhtNZsHIYxwfy2Ms5-lxAa9v-tOA_hF78")
print(f"Elevation at specified location: {resulting_3d_array[0, 4, 0]}")
print(f"Clicked data at specified location: {resulting_3d_array[0, 4, 1]}")
