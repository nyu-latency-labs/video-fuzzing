import logging
from moviepy.video.VideoClip import VideoClip

from Config.Config import Config
from Event.Event import EventType, Event
from Event.EventSimulator import EventSimulator
from Pipeline.PipelineUnit import PipelineUnit
from Utils.Timer import timer
from VideoGenerator.VideoGenerator import VideoGenerator


def generate_distribution(fn, count: int):
    distribution = []
    for i in range(count):
        k = fn()
        k = k if k >= 0 else 0
        distribution.append(int(k))

    logging.debug("distribution is: %s", distribution)
    return distribution


class PreProcessor(PipelineUnit):
    video_generator = None

    def __init__(self, config: Config):
        self.config = config
        self.video_generator = VideoGenerator(config.media_root)

    # Generate videos as per distributions (class, num, time)
    @timer
    def apply(self, data):

        object_distribution = data["object_distribution"]
        time_distribution = data["time_distribution"]
        object_types = data["object_types"]

        simulator = EventSimulator()

        # Add event for every step
        for i in range(0, self.config.duration, self.config.step_size):
            event = Event(EventType.INTERVAL, i, None, int(i / self.config.step_size))
            simulator.add_event(event)

        end_simulation_event = Event(EventType.END_SIMULATION, self.config.duration)
        simulator.add_event(end_simulation_event)
        final_clips = []

        # Event Simulation
        # Do not worry about trailing clips. They will be cut off at post-processing step
        current_event = simulator.get_event()
        while current_event is not None:

            if current_event.event_type is EventType.END_SIMULATION:
                while simulator.has_video_event():
                    self.remove_video(current_event, simulator)
                break

            if current_event.event_type is EventType.INTERVAL:
                logging.debug("Expected %s video at time: %s and got %s", object_distribution[current_event.data],
                              current_event.time, simulator.get_video_events_in_progress())
                while object_distribution[current_event.data] > simulator.get_video_events_in_progress():
                    self.add_new_video(current_event, final_clips, object_types, simulator, time_distribution)

                while object_distribution[current_event.data] < simulator.get_video_events_in_progress():
                    self.remove_video(current_event, simulator)

            if current_event.event_type is EventType.VIDEO_END:
                self.add_new_video(current_event, final_clips, object_types, simulator, time_distribution)

            current_event = simulator.get_event()

        data["clips"] = final_clips
        return data

    def remove_video(self, current_event, simulator):
        event = simulator.get_video_event()
        event.clip.set_end(current_event.time)
        logging.debug("Modified video with start time: %s and set end time to %s",
                      event.clip.start, event.clip.end)

    def add_new_video(self, current_event, final_clips, object_types, simulator, time_distribution):
        video = self.get_video(object_types.pop(0), time_distribution.pop(0), current_event.time)
        final_clips.append(video)
        video_event = Event(EventType.VIDEO_END, current_event.time + video.duration, video, current_event.data)
        simulator.add_event(video_event)

    def get_video(self, object_type: str, object_duration: int, start_time: int) -> VideoClip:
        return self.video_generator.get_video(object_type, object_duration, start_time)
