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
        self._load_segment(transcript, p, c, n)

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

    def _load_segment(self, transcript, prev_index, curr_index, next_index):
        self.segment_data.prev_index = prev_index
        self.segment_data.curr_index = curr_index
        self.segment_data.next_index = next_index
        self.segment_data.num_segments = len(transcript)

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
            self.segment_data.window = Window(
                start=segment_start,
                end=segment_end,
                plot_yaxis="TODO",
                plot_xaxis="TODO",
            )
        else:
            self.segment_data.curr_segment = Segment()

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

    def change_start_timestamp(self, delta, segment_data):
        curr_start = segment_data.curr_segment.start
        curr_end = segment_data.curr_segment.end
        new_start = curr_start + delta
        if new_start < 0:
            new_start = 0
        if new_start >= curr_end:
            new_start = curr_end
        segment_data.curr_segment.start = new_start

    def update_window_timestamp(self, segment_data, start, end):
        segment_data.window.start = start
        segment_data.window.end = end


    def change_end_timestamp(self, delta, segment_data):
        curr_start = segment_data.curr_segment.start
        curr_end = segment_data.curr_segment.end
        new_end = curr_end + delta
        if new_end > segment_data.num_segments:
            new_end = segment_data.num_segments
        if new_end <= curr_start:
            new_end = curr_start
        segment_data.curr_segment.end = new_end

    def copy_timstamp_edits_to_transcript(self, segment_data, session_data):
        session_data.transcript[segment_data.curr_index][
            0
        ] = segment_data.curr_segment.start
        session_data.transcript[segment_data.curr_index][
            1
        ] = segment_data.curr_segment.end
