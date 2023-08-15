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

    def delete_segment(self, session_data, segment_data):
        if not segment_data.num_segments:
            return
        curr_index = segment_data.curr_index
        transcript = session_data.transcript
        start, end, label, language, text = transcript.pop(curr_index)
        print(
            f"Removed line {curr_index}: ({start}, {end}) {label}, {language}, {text}"
        )

    def change_segment(self, transcript, new_index):
        p, c, n = self._get_prev_curr_next_indexes(new_index, len(transcript))
        self._update_segment(transcript, p, c, n)
        start = self.segment_data.curr_segment.start
        end = self.segment_data.curr_segment.end
        self._set_window_bounds(start, end)

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
            self.segment_data.window = Window(segment_start, segment_end)

    def _update_segment(self, transcript, prev_index, curr_index, next_index):
        self.segment_data.prev_index = prev_index
        self.segment_data.curr_index = curr_index
        self.segment_data.next_index = next_index
        self.segment_data.num_segments = len(transcript)
        zoom_scaler = self.segment_data.window.zoom_scaler
        if transcript:
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
            self.segment_data.window = Window(segment_start, segment_end, zoom_scaler)
        else:
            self.segment_data.curr_segment = Segment()

    def _set_window_bounds(self, start, end):
        self.segment_data.window.start = start
        self.segment_data.window.end = end

    def _get_prev_curr_next_indexes(self, index, num_segments):
        index = max(0, min(index, num_segments - 1))
        prev_index = index - 1 if index > 0 else None
        curr_index = index
        next_index = index + 1 if index < num_segments - 1 else None

        return prev_index, curr_index, next_index

    def detect_overlap(self, curr_index, transcript):
        if not transcript:
            return
        curr_start, _, curr_label, _, _ = transcript[curr_index]
        for index in range(curr_index - 1, -1, -1):
            start, end, label, language, text = transcript[index]

            if label == curr_label:
                if end >= curr_start:
                    return f"Line {index}: ({start:.2f}, {end:.2f}) : {label} : {language} : {text}"
        else:
            return None

    def change_timestamp(self, delta, segment_data, duration, is_start):
        curr_start = segment_data.curr_segment.start
        curr_end = segment_data.curr_segment.end

        if is_start:
            new_start = max(0, min(curr_end, curr_start + delta))
            segment_data.curr_segment.start = new_start
        else:
            new_end = max(curr_start, min(duration, curr_end + delta))
            segment_data.curr_segment.end = new_end

    def update_window_timestamp(self, segment_data):
        segment_data.window.start = segment_data.curr_segment.start
        segment_data.window.end = segment_data.curr_segment.end

    def copy_timestamp_edits_to_transcript(self, segment_data, transcript):
        curr_index = segment_data.curr_index
        transcript[curr_index][0] = segment_data.curr_segment.start
        transcript[curr_index][1] = segment_data.curr_segment.end

    def initialise_window_data(self, segment_data, max_value):
        segment_data.window.start = segment_data.curr_segment.start
        segment_data.window.end = segment_data.curr_segment.end
        segment_data.window.normaliser = max_value
        segment_data.window.zoom_scaler = 1
