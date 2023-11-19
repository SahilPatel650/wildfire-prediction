import sys
import json

if __name__ == "__main__":
    # Parse the JSON string from the first argument
    grid_data_str = sys.argv[1]
    grid_data = json.loads(grid_data_str)
    #write the grid data to a file
    with open("grid_data.json", "w") as f:
        json.dump(grid_data, f)
        