from moviepy.video.io.VideoFileClip import VideoFileClip
from torchvision.models.detection import ssd300_vgg16, SSD300_VGG16_Weights

from config.config import Config
from inference.model import Model


class SDD(Model):
    def __init__(self, config: Config):
        super().__init__(config)
        self.name = "model_sdd"
        self.weights = SSD300_VGG16_Weights.DEFAULT
        self.model = ssd300_vgg16(weights=self.weights, score_thresh=self.confidence).to(self.device).eval()
        self.pre_processor = self.weights.transforms()

    def apply(self, data: dict):
        clip = VideoFileClip(data["video_path"])
        clip_tensor = self.clip_to_tensor(clip)
        result = self.predict(clip_tensor)
        result["fps"] = clip.fps
        result["duration"] = clip.duration
        result["filename"] = data["filename"]
        bbox_clip = self.generate_bbox_video(clip_tensor, result)
        self.plot_latency_graph(result)
        accuracy = self.get_accuracy(data["metadata"], result["labels"])

        data["model_prediction"] = result
        data["model_bbox_clip"] = bbox_clip
        data["model_accuracy"] = accuracy
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
