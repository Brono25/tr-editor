import yaml
from models.segment_data import Segment


class SegmentManager:
    def __init__(self, segment_data, console):
        self.segment_data = segment_data
        self.console = console

    def new_session(self):
        self.segment_data.reset()

    def delete_segment(self, session_data, segment_data):
        if not segment_data.num_segments:
            return
        curr_index = segment_data.curr_index
        transcript = session_data.transcript
        start, end, label, language, text = transcript.pop(curr_index)
        self.console.log(
            f"Removed line {curr_index}: ({start}, {end}) {label}, {language}, {text}"
        )

    def load_segment_data(self, session_name):
        try:
            with open(session_name, "r") as file:
                data_dict = yaml.safe_load(file)
                self.segment_data.update_from_dict(data_dict["segment_data"])
            return True
        except (FileNotFoundError, yaml.YAMLError, KeyError):
            return False

    def initialise_segment_data_from_transcript(self, transcript):
        self.segment_data.reset()
        self.segment_data.num_segments = len(transcript)
        if self.segment_data.num_segments > 1:
            self.segment_data.curr_segment = Segment(
                *transcript[self.segment_data.curr_index]
            )
            self.segment_data.next_segment = Segment(
                *transcript[self.segment_data.next_index]
            )

    def update_indexes(self, new_index, num_segments):
        p, c, n = self._get_prev_curr_next_indexes(new_index, num_segments)
        self.segment_data.prev_index = p
        self.segment_data.curr_index = c
        self.segment_data.next_index = n
        return p, c, n

    def update_segments_to_new_index(
        self, transcript, prev_index, curr_index, next_index
    ):
        self.segment_data.num_segments = len(transcript)

        if transcript:
            start, end, label, language, text = transcript[curr_index]
            self.segment_data.curr_segment.start = start
            self.segment_data.curr_segment.end = end
            self.segment_data.curr_segment.label = label
            self.segment_data.curr_segment.language = language
            self.segment_data.curr_segment.text = text

            if prev_index is not None:
                start, end, label, language, text = transcript[prev_index]
                self.segment_data.prev_segment.start = start
                self.segment_data.prev_segment.end = end
                self.segment_data.prev_segment.label = label
                self.segment_data.prev_segment.language = language
                self.segment_data.prev_segment.text = text
            else:
                self.segment_data.prev_segment.reset()

            if next_index is not None:
                start, end, label, language, text = transcript[next_index]
                self.segment_data.next_segment.start = start
                self.segment_data.next_segment.end = end
                self.segment_data.next_segment.label = label
                self.segment_data.next_segment.language = language
                self.segment_data.next_segment.text = text
            else:
                self.segment_data.next_segment.reset()
        else:
            self.segment_data.curr_segment.reset()

    def _get_prev_curr_next_indexes(self, index, num_segments):
        index = max(0, min(index, num_segments - 1))
        prev_index = index - 1 if index > 0 else None
        curr_index = index
        next_index = index + 1 if index < num_segments - 1 else None

        return prev_index, curr_index, next_index

    def edit_timestamps(self, transcript, index, new_start, new_end):
        self._edit_segment_timestamps(new_start, new_end)
        self._edit_transcript_timestamps(transcript, index, new_start, new_end)

    def _edit_segment_timestamps(self, new_start, new_end):
        self.segment_data.curr_segment.start = new_start
        self.segment_data.curr_segment.end = new_end

    def _edit_transcript_timestamps(self, transcript, index, new_start, new_end):
        transcript[index][0] = new_start
        transcript[index][1] = new_end

    def find_all_instances_of_overlap(self, transcript):
        self.console.log("\n" + "Running overlap test:")
        flag = False
        for i in range(len(transcript)):
            status = self.detect_overlap(transcript, curr_index=i)
            if status:
                self.console.log(" " * 5 + status)
                flag = True
        if not flag:
            self.console.log("No overlaps detected")

    def detect_overlap(self, transcript, curr_index):
        if not transcript:
            return None
        curr_start, _, curr_label, _, _ = transcript[curr_index]
        for index in range(curr_index - 1, -1, -1):
            _, end, label, _, _ = transcript[index]

            if label == curr_label:
                if end >= curr_start:
                    status = f"Line {index} overlaps line {curr_index}"
                    return status
        else:
            return None

    def insert_segment_at_index(self, transcript, segment, index):
        transcript.insert(index + 1, segment)
        p,c,n = self.update_indexes(index, len(transcript))
        self.update_segments_to_new_index(transcript, p, c, n)

        return transcript
