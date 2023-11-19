import re
import numpy as np
import tensorflow as tf

INPUT_FEATURES = ['elevation', 'PrevFireMask']
OUTPUT_FEATURES = ['FireMask']

stats = {
    "elevation": {"min": 563.0764, "max":1328.4357},
    "frp": {"min": 0.0, "max": 83.63587189},
    "PrevFireMask": {"min": 0.0, "max": 1.0},
    "FireMask": {"min": 0.0, "max": 1.0}
}

def _get_features_dict(sample_size, features):
    sample_shape = [sample_size, sample_size]
    features = set(features)
    columns = [
        tf.io.FixedLenFeature(shape=sample_shape, dtype=tf.float32) for _ in features
    ]
    return dict(zip(features, columns))

def get_frp_data(fire_data):
    frp_data = tf.zeros_like(fire_data)
    frp_data = frp_data + fire_data
    frp_data = (frp_data + tf.roll(fire_data, 1, axis=0) + tf.roll(fire_data, -1, axis=0) + tf.roll(fire_data, 1, axis=1) + tf.roll(fire_data, -1, axis=1)) / 50
    return frp_data

def norm(inp, min_val, max_val):
    return tf.math.divide_no_nan(inp - min_val, max_val - min_val)

def _parse_fn(example_proto, data_size, sample_size, num_in_channels, include_frp):
    input_features = ['elevation', 'PrevFireMask']
    output_features = ['FireMask']
    feature_names = input_features + output_features
    features_dict = _get_features_dict(data_size, feature_names)
    features = tf.io.parse_single_example(example_proto, features_dict)
    
    features["PrevFireMask"] = tf.clip_by_value(features["PrevFireMask"], stats["PrevFireMask"]["min"], stats["PrevFireMask"]["max"])
    features["FireMask"] = tf.clip_by_value(features["FireMask"], stats["FireMask"]["min"], stats["FireMask"]["max"])
    features["elevation"] = norm(
        tf.clip_by_value(features["elevation"], stats["elevation"]["min"], stats["elevation"]["max"]),
        stats["elevation"]["min"],
        stats["elevation"]["max"]
    )
    if include_frp:
        frp_data = get_frp_data(features["PrevFireMask"])
        frp_data = norm(
            tf.clip_by_value(frp_data, stats["frp"]["min"], stats["frp"]["max"]),
            stats["frp"]["min"],
            stats["frp"]["max"]
        )
        features["frp"] = frp_data

    print(features)

    # if include_frp:
    #     inputs_list.insert(
    #         0, norm(
    #             tf.clip_by_value(features.get("elevation"), stats["elevation"]["min"], stats["elevation"]["max"]),
    #             stats["frp"]["min"],
    #             stats["frp"]["max"]
    #         )
    #     )

    # print(fire_data.shape)
    # fire_data = tf.clip_by_value(fire_data, stats["PrevFireMask"]["min"], stats["PrevFireMask"]["max"])

    # elev_data = tf.clip_by_value(elev_data, stats["elevation"]["min"], stats["elevation"]["max"]) - stats["elevation"]["min"]
    # div_val = stats["elevation"]["max"] - stats["elevation"]["min"]
    # elev_data = tf.math.divide_no_nan(elev_data, div_val)
    # inputs_list = [elev_data, fire_data]

    # if include_frp:
    #     frp_data = get_frp_data(fire_data)
    #     frp_data = tf.clip_by_value(frp_data, stats["frp"]["min"], stats["frp"]["max"]) - stats["frp"]["min"]
    #     div_val = stats["frp"]["max"] - stats["frp"]["min"]
    #     frp_data = tf.math.divide_no_nan(frp_data, div_val)
    #     inputs_list = [inputs_list[0]] + [frp_data] + [inputs_list[1]]

    if include_frp:
        input_features.insert(1, "frp")
    inputs_list = [features[key] for key in input_features]
    inputs_stacked = tf.stack(inputs_list, axis=0)
    input_img = tf.transpose(inputs_stacked, [1, 2, 0])

    outputs_list = [features[key] for key in output_features]
    outputs_stacked = tf.stack(outputs_list, axis=0)
    output_img = tf.transpose(outputs_stacked, [1, 2, 0])
    
    return input_img, output_img

def get_dataset(file_pattern, data_size, sample_size,
                batch_size, num_in_channels, compression_type, include_frp):
    dataset = tf.data.Dataset.list_files(file_pattern)
    dataset = dataset.interleave(
        lambda x: tf.data.TFRecordDataset(x, compression_type=compression_type),
        num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    dataset = dataset.map(
        lambda x: _parse_fn(
            x, data_size, sample_size, num_in_channels, include_frp),
        num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    return dataset

if __name__ == "__main__":
    dataset = get_dataset(
        "./data/next_day_wildfire_spread_eval*",
        data_size=64,
        sample_size=64,
        batch_size=100,
        num_in_channels=2,
        compression_type=None,
        include_frp=True
    )
    print(np.unique(next(iter(dataset))[0].numpy()[0, :, :, -1]))