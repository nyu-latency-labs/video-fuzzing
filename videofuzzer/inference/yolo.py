import numpy
import torch

from ..config.config import Config
from ..inference.model import Model
from ..utility.timer import timer


class Yolo(Model):
    instance = None

    def __init__(self, config: Config):
        super().__init__(config)
        self.model = None
        self.name = "model_yolo"

    @timer
    def apply(self, data: dict):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(self.device)
        clip = data["video"]
        clip_tensor = self.clip_to_tensor(clip)
        result = self.predict(clip_tensor)
        result["fps"] = clip.fps
        result["duration"] = clip.duration
        result["filename"] = data["filename"]
        if self.config.model_bbox_generate:
            self.generate_bbox_video(clip_tensor, result)
        self.plot_latency_graph(result)
        accuracy = self.get_accuracy(data["metadata"], result["labels"])

        model_data = {"model_prediction": result, "model_accuracy": accuracy}
        if "inference" not in data:
            data["inference"] = []
        data["inference"].append(model_data)
        return data

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

    def predict_frame(self, frame):
        numpy_frame = numpy.asarray(frame.permute(1, 2, 0).cpu())
        results = self.model([numpy_frame])
        labels = results.pandas().xyxy[0].name
        confidences = results.pandas().xyxy[0].confidence
        boxes = torch.tensor(results.pandas().xyxy[0].iloc[:, 0:4].values if not results.pandas().xyxy[0].empty else [])

        return boxes, labels.tolist(), confidences.tolist()
