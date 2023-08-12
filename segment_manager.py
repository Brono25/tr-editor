import yaml
from segment_data import Segment, Window


class SegmentManager:
    def __init__(self, segment_data):
        self.segment_data = segment_data

    def open_session(self, session_name):
        return self._load_segment_data_from_savefile(session_name)

    def new_session(self):
        self.segment_data.reset()

    def open_transcript(self, transcript):
        self._initialise_segment_data_from_transcript(transcript)

    def _load_segment_data_from_savefile(self, session_name):
        try:
            with open(session_name, "r") as file:
                data_dict = yaml.safe_load(file)
                self.segment_data.update_from_dict(data_dict["segment_data"])
            return True
        except (FileNotFoundError, yaml.YAMLError, KeyError):
            return False

    def _initialise_segment_data_from_transcript(self, transcript):
        self.segment_data.reset()
        self.segment_data.num_segments = len(transcript)
        if self.segment_data.num_segments > 1:
            self.segment_data.curr_segment = Segment(
                *transcript[self.segment_data.curr_index]
            )
            self.segment_data.next_segment = Segment(
                *transcript[self.segment_data.next_index]
            )

            segment_start, segment_end, _, _, _ = transcript[
                self.segment_data.curr_index
            ]
            self.segment_data.window = Window(
                start=segment_start,
                end=segment_end,
                plot_yaxis="TODO",
                plot_xaxis="TODO",
            )

    def change_segment(self, transcript, prev_index, curr_index, next_index):
        self.segment_data.prev_index = prev_index
        self.segment_data.curr_index = curr_index
        self.segment_data.next_index = next_index

        self.segment_data.curr_segment = Segment(*transcript[curr_index])

        if prev_index is not None:
            self.segment_data.prev_segment = Segment(*transcript[prev_index])
        else:
            self.segment_data.prev_segment.reset()
        if next_index is not None:
            self.segment_data.next_segment = Segment(*transcript[next_index])
        else:
            self.segment_data.next_segment.reset()

        segment_start, segment_end, _, _, _ = transcript[curr_index]
        self.segment_data.window = Window(
            start=segment_start, end=segment_end, plot_yaxis="TODO", plot_xaxis="TODO"
        )

    def get_prev_curr_next_indexes(self, index):
        num_segments = self.segment_data.num_segments
        index = max(0, min(index, num_segments - 1))
        prev_index = index - 1 if index > 0 else None
        curr_index = index
        next_index = index + 1 if index < num_segments - 1 else None

        return prev_index, curr_index, next_index
