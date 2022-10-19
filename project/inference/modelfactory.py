from inference.fasterrcnn import FasterRCNN
from inference.fcos import FCOS
from inference.maskrcnn import MaskRCNN
from inference.retinanet import RetinaNet
from inference.sdd import SDD
from inference.yolo import Yolo

model_mapping = {
    "yolo": Yolo,
    "retinanet": RetinaNet,
    "fasterrcnn": FasterRCNN,
    "maskrcnn": MaskRCNN,
    "sdd": SDD,
    "fcos": FCOS
}


class ModelFactory:

    @classmethod
    def get_model(cls, config):
        if config.model in model_mapping:
            return model_mapping[config.model](config)
        return Yolo(config)
