import numpy as np

class SegmentData:
    def __init__(self):
        self.segment_index = 0
        self.window_start = None
        self.window_end = None
        self.segment_start = None
        self.segment_end = None
        self.segment_label = None
        self.segment_text = None
        self.segment_language = None
        self.plot_yaxis = None
        self.plot_xaxis = None

    def to_dict(self):
        return {
            "segment_index": self.segment_index,
            "window_start": self.window_start,
            "window_end": self.window_end,
            "segment_start": self.segment_start,
            "segment_end": self.segment_end,
            "segment_label": self.segment_label,
            "segment_text": self.segment_text,
            "segment_language": self.segment_language,
            "plot_yaxis": self.plot_yaxis,
            "plot_xaxis": self.plot_xaxis,
        }

    def update_from_dict(self, data):
        self.segment_index = data.get("segment_index")
        self.window_start = data.get("window_start")
        self.window_end = data.get("window_end")
        self.segment_start = data.get("segment_start")
        self.segment_end = data.get("segment_end")
        self.segment_label = data.get("segment_label")
        self.segment_text = data.get("segment_text")
        self.segment_language = data.get("segment_language")
        self.plot_yaxis = data.get("plot_yaxis")
        self.plot_xaxis = data.get("plot_xaxis")
       
    def reset(self):
        self.segment_index = 0
        self.window_start = None
        self.window_end = None
        self.segment_start = None
        self.segment_end = None
        self.segment_label = None
        self.segment_text = None
        self.segment_language = None
        self.plot_yaxis = []
        self.plot_xaxis = []