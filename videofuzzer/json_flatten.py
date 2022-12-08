import os
import json
import csv


def get_data(root: str):
    json_list = []
    for files in os.listdir(root):
        file_path = os.path.join(root, files)
        if os.path.isfile(file_path) and files.endswith("json"):
            json_list.append(file_path)

    final_data = []
    for file in json_list:
        with open(file) as json_file:
            data = json.load(json_file)
            if "config" in data and "metrics" in data:
                final_data.append(flatten(data))

    return final_data


def flatten(data: dict):
    object_classes = data["config"]["object_classes"]["value"]
    time_distrbution = data["config"]["time_distribution"]
    object_distrbution = data["config"]["object_distribution"]
    transformers = data["config"]["transformers"]
    compositor = data["config"]["compositor"]
    precision = data["metrics"]["precision"]
    recall = data["metrics"]["recall"]

    result = []
    result.extend(flatten_object_classes(set(object_classes)))
    result.extend(flatten_distribution(time_distrbution))
    result.extend(flatten_distribution(object_distrbution))
    result.extend(flatten_transformers(transformers))
    result.extend(flatten_compositor(compositor))
    result.append(precision)
    result.append(recall)
    return result


def flatten_object_classes(data: set):
    class_list = ["fire hydrant", "traffic light", "bicycle", "umbrella", "train", "skateboard", "bird",
                  "truck", "stop sign", "parking meter", "motorbike", "bus", "boat", "person", "car",
                  "bench"]

    result = []
    for val in class_list:
        result.append(1 if val in data else 0)

    return result


def flatten_distribution(data: dict):
    result = []
    if data["type"] == "linear":
        result.extend([1, data["value"]])
    else:
        result.extend([0, 0])

    if data["type"] == "normal":
        result.extend([1, data["mean"], data["std"]])
    else:
        result.extend([0, 0, 0])

    if data["type"] == "alpine":
        result.extend([1, data["multiplier"], data["downscale"]])
    else:
        result.extend([0, 0, 0])

    if data["type"] == "exponential":
        result.extend([1, data["lambda"]])
    else:
        result.extend([0, 0])

    return result


def flatten_transformers(data: list):
    result = []

    rotate_result = [0, 0]
    resize_result = [0, 0]
    for tx in data:
        if tx["type"] == "rotate_transformer":
            rotate_result = [1, tx["angle"]]

    for tx in data:
        if tx["type"] == "resize_transformer":
            resize_result = [1, tx["ratio"]]

    result.extend(rotate_result)
    result.extend(resize_result)
    return result


def flatten_compositor(data: dict):
    if data["type"] == "moving_compositor":
        return [0, 1]

    if data["type"] == "grid_compositor":
        return [1, 0]


result = get_data(str(os.getcwd()))
with open("new_file.csv", "w+") as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerows(result)
