from moviepy.video.io.VideoFileClip import VideoFileClip
from torchvision.models.detection import fcos_resnet50_fpn, FCOS_ResNet50_FPN_Weights

from ..config.config import Config
from ..inference.model import Model
from ..utility.timer import timer


class FCOS(Model):
    def __init__(self, config: Config):
        super().__init__(config)
        self.name = "model_fcos"
        self.weights = FCOS_ResNet50_FPN_Weights.DEFAULT
        self.model = fcos_resnet50_fpn(weights=self.weights, score_thresh=self.confidence).to(self.device).eval()
        self.pre_processor = self.weights.transforms()

    @timer
    def apply(self, data: dict):
        clip = VideoFileClip(data["video_path"])
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
        preprocessed_input = [self.pre_processor(frame)]
        results = self.model(preprocessed_input)[0]
        labels = [self.weights.meta["categories"][i] for i in results["labels"]]
        confidences = results["scores"]
        boxes = results["boxes"]

        return boxes.to(self.device), labels, confidences
