import logging
from math import ceil
from typing import List

from config.config import Config
from distribution_generator.dgfactory import DGFactory
from distribution_generator.distributiongenerator import DistributionGenerator
from event.event import EventType, Event
from event.eventsimulator import EventSimulator
from processor.processor import Processor
from utils.timer import timer
from video_generator.video import Video
from video_generator.videogenerator import VideoGenerator


def generate_distribution(distribution_generator: DistributionGenerator, count: int) -> List[int]:
    distribution = []
    for i in range(count):
        k = distribution_generator.next()
        k = k if k >= 0 else 0
        distribution.append(int(k))

    logging.debug("distribution is: %s", distribution)
    return distribution


class PreProcessor(Processor):
    video_generator: VideoGenerator = None

    def __init__(self, config: Config):
        super().__init__(config)
        self.video_generator = VideoGenerator(config.media_root)
        self.name = "pre_processor"

    # Generate videos as per distributions (class, num, time)
    @timer
    def apply(self, data: dict) -> dict:
        object_distribution_generator = generate_distribution(data["object_distribution"],
                                                              ceil(self.config.duration / self.config.step_size))

        data["fix_value"] = self.config.duration
        time_distribution_generator = data["time_distribution"]

        object_type_generator = data["object_type_distribution"]

        simulator = EventSimulator()

        # Add event for every step
        for i in range(0, self.config.duration, self.config.step_size):
            event = Event(EventType.INTERVAL, i, None, int(i / self.config.step_size))
            simulator.add(event)

        end_simulation_event = Event(EventType.END_SIMULATION, self.config.duration)
        simulator.add(end_simulation_event)
        final_clips: List[Video] = []

        # Event Simulation
        # Do not worry about trailing clips. They will be cut off at post-processing step
        current_event = simulator.get()
        while current_event is not None:

            if current_event.event_type is EventType.END_SIMULATION:
                while simulator.has_video_event():
                    self.remove_video(current_event, simulator)
                break

            if current_event.event_type is EventType.INTERVAL:
                logging.debug("Expected %s video at time: %s and got %s",
                              object_distribution_generator[current_event.data],
                              current_event.time, simulator.get_video_events_in_progress())
                while object_distribution_generator[current_event.data] > simulator.get_video_events_in_progress():
                    self.add_video(current_event, final_clips, object_type_generator, simulator,
                                   time_distribution_generator)

                while object_distribution_generator[current_event.data] < simulator.get_video_events_in_progress():
                    self.remove_video(current_event, simulator)

            if current_event.event_type is EventType.VIDEO_END:
                self.add_video(current_event, final_clips, object_type_generator, simulator,
                               time_distribution_generator)

            current_event = simulator.get()

        data["clips"] = final_clips
        return data

    def remove_video(self, current_event: Event, simulator: EventSimulator):
        event = simulator.get_video_event()
        event.clip.set_end(current_event.time)

        logging.debug(f"Removing video with start time: {event.clip.start} and set end time to {event.clip.end}")

    def add_video(self, current_event: Event, final_clips: List[Video], object_type_generator: DistributionGenerator,
                  simulator: EventSimulator, time_distribution_generator: DistributionGenerator):
        video = self.get_video(object_type_generator.next(), int(time_distribution_generator.next()), current_event.time)
        final_clips.append(video)
        video_event = Event(EventType.VIDEO_END, current_event.time + video.duration, video, current_event.data)
        simulator.add(video_event)

        logging.debug(f"Adding video with start time: {video.start} and set end time to {video.end}")

    def get_video(self, object_type: str, object_duration: int, start_time: int) -> Video:
        return self.video_generator.get(object_type, object_duration, start_time)

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")
