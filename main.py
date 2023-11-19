import sys
import json
import numpy as np
from api_cache import get_elevation
import matplotlib.pyplot as plt
from matplotlib import colormaps

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

            selected = arr['selected']
            print(i, j, lat, lng, selected)
            weather_data = get_elevation(lat, lng, API_KEY)
            three_d_array[i, j, 0] = weather_data
            three_d_array[i, j, 1] = selected

    grid_data[0] = ai_utils.normalize_elevation(grid_data[0])
    model = ai_utils.get_model((64, 64, 2))
    model.load_weights("training/models/model.h5")
    preds = model_inference(data, model)
    plt.imshow(preds, cmap=colormaps["Reds"])
    plt.show()
    plt.save_fig("web/static/images/prediction.png", bbox_inches="tight")
