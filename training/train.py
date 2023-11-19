import numpy as np
import tensorflow as tf
from get_data import get_dataset
import matplotlib.pyplot as plt
import sys

data = get_dataset(
    "data/next_day_wildfire_spread_train*",
    data_size=64,
    sample_size=32,
    batch_size=100,
    num_in_channels=8,
    clip_and_normalize=False,
    clip_and_rescale=False,
    random_crop=True,
    center_crop=False
)
# print(np.unique(next(iter(data))[0][0, :, :, -1].numpy()))
# print(next(iter(data))[0].shape)

if sys.argv[1] == "train":
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu", input_shape=(64, 64, 8)))
    model.add(tf.keras.layers.Conv2D(64, 3, padding="same", activation="relu", input_shape=(64, 64, 32)))
    model.add(tf.keras.layers.Conv2D(1, 2, padding="same", activation="sigmoid", input_shape=(64, 64, 64)))
    model.add(tf.keras.layers.Flatten())

    model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss="binary_crossentropy")
    model.summary()

    model.fit(data, epochs=1)
    model.save("model.h5")
else:
    model = tf.keras.models.load_model("trained.h5")

pred_x_y = next(iter(data))
pred_x = pred_x_y[0][:1]
pred_y = pred_x_y[1][:1]
# print(pred_x.shape)
# print(np.unique(pred_x.numpy()[0, :, :, -1]))
preds = model.predict(pred_x)[0]
# print(np.mean(preds))
preds = tf.map_fn(lambda x: 1.0 if x >= 0.1 else 0.0, preds)
# preds = tf.reshape(preds, (32, 32))
plt.imshow(pred_x[0,:,  :,-1])
plt.show()
# plt.imshow(tf.reshape(pred_y, (32, 32)))
plt.show()
plt.imshow(preds)
plt.show()
