import sys
import json
import numpy as np
from api_cache import get_elevation
import matplotlib.pyplot as plt
from matplotlib import colormaps
import ai_utils

def model_inference(data, model):
    preds = model.predict(np.expand_dims(data, axis=0))
    preds = np.squeeze(preds)
    preds = np.clip(preds, 0, 1)
    # for i in range(len(preds)):
    #     preds[i] = list(map(lambda x: {"selection": x}, preds[i]))
    return preds

if __name__ == "__main__":
    API_KEY = json.load(open('api_key.json'))['ELEVATION_API_KEY']
    # Parse the JSON string from the first argument
    grid_data_str = sys.argv[1]
    grid_data = json.loads(grid_data_str)
    img_path = sys.argv[2]
    #create a 3d array
    data = np.zeros((64, 64, 2))

    # Convert the JSON data into the 2D array
    for i in range(64):
        for j in range(64):
            # Extract latitude, longitude, and selected from the JSON data
            arr = grid_data[i][j]
            lat = arr['lat']
            lng = arr['lng']

            selected = arr['selected']
            weather_data = get_elevation(lat, lng, API_KEY)
            data[i, j, 0] = weather_data
            data[i, j, 1] = selected

    print(data.shape)
    data[:, :, 0] = ai_utils.normalize_elevation(data[:, :, 0])
    model = ai_utils.get_model((64, 64, 2))
    model.load_weights("training/models/no_frp_model.h5")
    preds = model_inference(data, model)
    print(preds)
    plt.imshow(preds, cmap=colormaps["Reds"])
    # plt.show()
    plt.savefig(img_path, bbox_inches="tight")
