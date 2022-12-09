import json
import uuid

from ..config.config import Config
from ..processor.processor import Processor
from ..utility.timer import timer


class FinalProcessor(Processor):

    def __init__(self, config: Config):
        super().__init__(config)
        self.name = "final_processor"

    @timer
    def apply(self, data) -> dict:
        # video = data["video"]
        # filename = data["filename"]
        #
        # video = video.set_duration(self.config.duration)
        # video = video.set_fps(self.config.fps)
        # video = video.without_audio()
        #
        # if filename is None:
        #     filename = uuid.uuid4()
        #
        # os.makedirs("media/", exist_ok=True)
        # video_path = "media/" + filename + ".mp4"
        # video.write_videofile(video_path, self.config.fps, "mpeg4", audio=False)
        # data["status"] = True
        #
        # data["video_path"] = video_path

        data_to_return = {"config": data["final_config"], "metrics": data["inference"][0]["model_accuracy"]}
        final_json = json.dumps(data_to_return)
        final_data_file = open("media/" + str(uuid.uuid4()) + ".json", "w")
        final_data_file.write(final_json)
        final_data_file.close()

        return data

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")
