import numpy as np


class Segment:
    def __init__(self, start=None, end=None, label=None, language=None, text=None):
        self.start = start
        self.end = end
        self.label = label
        self.text = text
        self.language = language

    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "label": self.label,
            "text": self.text,
            "language": self.language,
        }

    def update_from_dict(self, data):
        self.start = data.get("start")
        self.end = data.get("end")
        self.label = data.get("label")
        self.text = data.get("text")
        self.language = data.get("language")

    def reset(self):
        self.start = None
        self.end = None
        self.label = None
        self.text = None
        self.language = None


class SegmentData:
    def __init__(self):
        self.curr_index = 0
        self.prev_index = None
        self.next_index = 1
        self.num_segments = 0
        self.overlap_status = None
        self.overlap_timestamp = None
        self.curr_segment = Segment()
        self.prev_segment = Segment()
        self.next_segment = Segment()

    def to_dict(self):
        return {
            "curr_index": self.curr_index,
            "prev_index": self.prev_index,
            "next_index": self.next_index,
            "num_segments": self.num_segments,
            "overlap_status": self.overlap_status,
            "overlap_timestamp": self.overlap_timestamp,
            "curr_segment": self.curr_segment.to_dict(),
            "prev_segment": self.prev_segment.to_dict(),
            "next_segment": self.next_segment.to_dict(),
        }

    def update_from_dict(self, data):
        self.curr_index = data.get("curr_index")
        self.prev_index = data.get("prev_index")
        self.next_index = data.get("next_index")
        self.num_segments = data.get("num_segments")
        self.overlap_status = data.get("overlap_status")
        self.overlap_timestamp = data.get("overlap_timestamp")
        segment_data = data.get("curr_segment", {})
        self.curr_segment.update_from_dict(segment_data)
        prev_segment_data = data.get("prev_segment", {})
        self.prev_segment.update_from_dict(prev_segment_data)
        next_segment_data = data.get("next_segment", {})
        self.next_segment.update_from_dict(next_segment_data)

    def reset(self):
        self.curr_index = 0
        self.prev_index = None
        self.next_index = 1
        self.num_segments = 0
        self.overlap_status = None
        self.overlap_timestamp = None
        self.curr_segment.reset()
        self.prev_segment.reset()
        self.next_segment.reset()
