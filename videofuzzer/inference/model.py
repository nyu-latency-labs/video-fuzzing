import copy
import logging
import time

import matplotlib.pyplot as plt
import numpy
import torch
from moviepy.video.VideoClip import VideoClip
from torchvision.utils import draw_bounding_boxes

from ..config.config import Config
from ..pipeline.pipelineunit import PipelineUnit
from ..utility.timer import timer


class Model(PipelineUnit):
    """
    A type of PipelineUnit used to add any custom processing to the pipeline.
    Examples are pre and post processor.
    """

    def __init__(self, config: Config):
        self.name = "model"
        self.config = config
        self.device = "cpu"
        # if torch.cuda.is_available():
        #     torch.cuda.empty_cache()
        self.confidence = config.model_confidence

    @timer
    def apply(self, data):
        raise NotImplementedError("Apply method not implemented.")

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

    def predict_frame(self, frame):
        raise NotImplementedError("Predict frame method not implemented.")

    def clip_to_tensor(self, clip):
        frames = torch.stack([torch.from_numpy(fr).to(self.device) for fr in clip.iter_frames(fps=self.config.fps)])
        return frames.permute(0, 3, 1, 2)

    def predict(self, frames):
        latencies = []
        prediction_boxes = []
        prediction_labels = []
        prediction_confidences = []
        for frame in frames:
            start_time = time.perf_counter()
            boxes, labels, confidences = self.predict_frame(frame)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            prediction_boxes.append(boxes)
            prediction_labels.append(labels)
            prediction_confidences.append(confidences)
            latencies.append(run_time * 1000)

        results = {
            "bboxes": prediction_boxes,
            "labels": prediction_labels,
            "confidences": prediction_confidences,
            "latencies": latencies
        }
        return results

    def generate_bbox_video(self, clip_tensor, data):
        bbox_frames = []
        for i in range(clip_tensor.size(dim=0)):
            bbox_frame = draw_bounding_boxes(clip_tensor[i], boxes=data["bboxes"][i],
                                             labels=data["labels"][i], colors="red", width=4)
            bbox_frames.append(bbox_frame)

        bbox_frames = torch.stack(bbox_frames)

        numpy_results = numpy.asarray(bbox_frames.permute(0, 2, 3, 1).detach().cpu())

        def make_frame(t):
            return numpy_results[round(t * data["fps"]), :]

        movie_clip = VideoClip(make_frame, duration=data["duration"]).set_fps(data["fps"])
        movie_clip.write_videofile("media/" + self.name + "_bboxes_" + data["filename"] + ".mp4", data["fps"], "mpeg4")
        return movie_clip

    def plot_latency_graph(self, data):
        fig = plt.figure()
        plt.plot(data["latencies"])
        plt.ylabel('latency (ms)')
        plt.savefig("media/" + self.name + "_latencygraph_" + data["filename"] + ".png")
        fig.clf()

    def get_accuracy(self, actuals, expected):
        hits = 0
        misses = 0
        expected = copy.deepcopy(expected)

        total_objects = 0
        total_objects_det = 0

        for obj in expected:
            total_objects += len(obj)

        for obj in actuals:
            total_objects_det += len(obj)

        miss_data = []
        hit_data = []
        for v1, v2 in zip(expected, actuals):
            miss = []
            hit = []
            for d1 in list(v1):
                if d1 not in v2:
                    miss_data.append(d1)
                    misses += 1
                else:
                    hit_data.append(d1)
                    hits += 1
                    v2.remove(d1)

            miss_data.append(miss)
            hit_data.append(hit)

        precision = (0 if total_objects_det == 0 else hits * 100 / total_objects_det)
        recall = 0 if total_objects == 0 else hits * 100 / total_objects
        print("---------------------------")
        print(f"# objects detected: {total_objects_det}")
        print(f"# objects actually present: {total_objects}")
        print(f"Hits: {hits}")
        print(f"Misses: {misses}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print("---------------------------")

        results = {
            "object_detected_count": total_objects_det,
            "total_objects": total_objects,
            "hits": hits,
            "misses": misses,
            "precision": precision,
            "recall": recall
        }

        return results
