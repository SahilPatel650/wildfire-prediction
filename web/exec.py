import sys
import json
import numpy as np
import ai_utils

def model_inference(data, model):
    preds = model.predict(np.expand_dims(data, axis=0))
    preds = np.squeeze(preds)
    preds = np.clip(preds, 0, 1).tolist()
    for i in range(len(preds)):
        preds[i] = list(map(lambda x: {"selection": x}, preds[i]))
    return preds

if __name__ == "__main__":
    # Parse the JSON string from the first argument
    grid_data_str = sys.argv[1]
    grid_data = json.loads(grid_data_str)
    data = np.zeros((64, 64, 2)) # replace with elevation, fire_mask data
    data[0] = ai_utils.normalize(data[0])
    model = ai_utils.get_model((64, 64, 2))
    model.load_weights("web/model.h5")
    preds = model_inference(data, model)
    with open("model_output.json", "w") as f:
        json.dump(preds, f)

