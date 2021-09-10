import string
import sys
import re
import json

CHARS_TO_REMOVE = "[\[\]'\"]"
expected = open(sys.argv[1], 'r')
actual = open(sys.argv[2], 'r')

expected_lines = json.load(expected)
actual_lines = json.load(actual)


def create_list(lines: string):
    result = []
    for line in lines:
        data1 = line.split("], ")
        for value in data1:
            arr = re.sub(CHARS_TO_REMOVE, "", value).split(", ")
            arr = list(filter(None, arr))
            result.append(arr)

    return result


expected_data = expected_lines['object_distribution']
actual_data = actual_lines['object_detection']

data_len = []

for d in expected_data:
    data_len.append(len(d))

missing_data = []
hitting_data = []
hits = 0
misses = 0

total_objects = 0
total_objects_det = 0

for obj in expected_data:
    total_objects += len(obj)

for obj in actual_data:
    total_objects_det += len(obj)

for v1, v2 in zip(expected_data, actual_data):
    miss = []
    hit = []
    for d1 in v1:
        if d1 not in v2:
            miss.append(d1)
            misses += 1
        else:
            hit.append(d1)
            hits += 1

    missing_data.append(miss)
    hitting_data.append(hit)


print(missing_data)
print("Total expected detections: " + str(total_objects))
print("Total actual detections: " + str(total_objects_det))
print("Total hits: " + str(hits))
print("Total misses: " + str(misses))
print("Precision: " + ("0" if total_objects_det == 0 else str(hits*100/total_objects_det)))
print("Recall: " + str(hits*100/total_objects))

# print(data_len)