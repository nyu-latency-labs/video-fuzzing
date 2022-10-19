from PIL import Image
import numpy as np
import torch
from torchvision import transforms, models
from matplotlib.colors import hsv_to_rgb
import cv2

import json

import sys
name = sys.argv[1]
experiment = sys.argv[2]


classes = [line.rstrip('\n') for line in open('voc_classes.txt')]
num_classes = len(classes)

def get_palette():
    # prepare and return palette
    palette = [0] * num_classes * 3

    for hue in range(num_classes):
        if hue == 0: # Background color
            colors = (0, 0, 0)
        else:
            colors = hsv_to_rgb((hue / num_classes, 0.75, 0.75))

        for i in range(3):
            palette[hue * 3 + i] = int(colors[i] * 255)

    return palette

def colorize(labels):
    # generate colorized image from output labels and color palette
    result_img = Image.fromarray(labels).convert('P', colors=num_classes)
    result_img.putpalette(get_palette())
    return np.array(result_img.convert('RGB'))

def visualize_output(image, output):
    assert(image.shape[0] == output.shape[1] and \
           image.shape[1] == output.shape[2]) # Same height and width
    assert(output.shape[0] == num_classes)

    # get classification labels
    raw_labels = np.argmax(output, axis=0).astype(np.uint8)

    labels = set(raw_labels.flatten())
    labels.remove(0)
    # print(labels)

    # for i in labels:
    #     if i > 0:
    #         print(classes[i])

    # comput confidence score
    # confidence = float(np.max(output, axis=0).mean())

    # # generate segmented image
    # result_img = colorize(raw_labels)

    # # generate blended image
    # blended_img = cv2.addWeighted(image[:, :, ::-1], 0.5, result_img, 0.5, 0)

    # result_img = Image.fromarray(result_img)
    # blended_img = Image.fromarray(blended_img)

    # return confidence, result_img, blended_img, raw_labels
    return labels

def infer(image, count):
    orig_tensor = np.asarray(image)
    input_tensor = preprocess(image)
    input_tensor = input_tensor.unsqueeze(0)
    input_tensor = input_tensor.detach().cpu().numpy()

    from onnx import numpy_helper
    import os
    import onnxruntime as rt

    sess = rt.InferenceSession("../model/fcn.onnx")

    outputs = sess.get_outputs()
    output_names = list(map(lambda output: output.name, outputs))
    input_name = sess.get_inputs()[0].name

    detections = sess.run(output_names, {input_name: input_tensor})
    # print("Output shape:", list(map(lambda detection: detection.shape, detections)))
    # print(f"Frame number {count}")
    output, aux = detections

    # conf, result_img, blended_img, _ = visualize_output(orig_tensor, output[0])
    labels = visualize_output(orig_tensor, output[0])
    return [classes[i] for i in labels]


preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

import cv2
vidcap = cv2.VideoCapture(f'{name}.mp4')
success = True
count = 0

data = {}
results = []
while True:
  success,image = vidcap.read()
  if not success:
      break
  count += 1
  print('Read frame #: ', count)
  results.append(infer(image, count))

data["object_detection"] = results



with open(f"{experiment}_fcn_{name}.json", 'w') as f:
    json.dump(data, f)

print(data)


