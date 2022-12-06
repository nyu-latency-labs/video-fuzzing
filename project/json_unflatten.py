import os
import json
import csv


def get_data(input: list):
    nonrandom_data = {
      "fps": 5,
      "duration": 30,
      "allow_overlap": False,
      "step_size": 1,
      "media_root": "../resources",
      "background_path": "../resources/street.jpg",
      "max_cores": 32,
      "use_cache": True,
      "dimension": {
        "x": 1920,
        "y": 1080
      },

      "num_video_copies": 1,

      "model": ["yolo"],
      "model_confidence": 0.5,
      "model_generate_bbox": True
    }

    result = {**nonrandom_data, **unflatten(input)}
    return result


def unflatten(data: list):
    config = {
        "object_classes": {"type": "choice", "value": unflatten_object_classes(data[0:16])},
        "time_distribution": unflatten_distribution(data[16:26]),
        "object_distribution": unflatten_distribution(data[26:36]),
        "transformers": unflatten_transformers(data[36:40]),
        "compositor": unflatten_compositor(data[40:42]),
        "precision": data[42], "recall": data[43]
    }

    return config


def unflatten_object_classes(data):
    class_list = ["fire hydrant", "traffic light", "bicycle", "umbrella", "train", "skateboard", "bird",
                  "truck", "stop sign", "parking meter", "motorbike", "bus", "boat", "person", "car",
                  "bench"]

    result = []
    for val in range(len(data)):
        if data[val] == 1:
            result.append(class_list[val])

    return result


def unflatten_distribution(data: list):
    if data[0] == 1:
        return {"type": "linear", "value": data[1]}

    if data[2] == 1:
        return {"type": "normal", "mean": data[3], "std": data[4]}

    if data[5] == 1:
        return {"type": "alpine", "multiplier": data[6], "downscale": data[7]}

    if data[8] == 1:
        return {"type": "exponential", "lambda": data[9]}


def unflatten_transformers(data: list):
    result = []

    if data[0] == 1:
        result.append({"type": "rotate_transformer", "angle": data[1]})

    if data[2] == 1:
        result.append({"type": "resize_transformer", "ratio": data[3]})

    return result


def unflatten_compositor(data: dict):
    if data[0] == 1:
        return {"type": "moving_compositor"}
    else:
        return {"type": "grid_compositor"}

