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

class Window:
    def __init__(self, start=None, end=None, plot_xaxis=None, plot_yaxis=None):
        self.start = start
        self.end = end
        self.plot_yaxis = plot_yaxis
        self.plot_xaxis = plot_xaxis

    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "plot_yaxis": self.plot_yaxis,
            "plot_xaxis": self.plot_xaxis,
        }
    def update_from_dict(self, data):
        self.start = data.get("start")
        self.end = data.get("end")
        self.plot_yaxis = data.get("plot_yaxis")
        self.plot_xaxis = data.get("plot_xaxis")

    def reset(self):
        self.start = None
        self.end = None
        self.plot_yaxis = None
        self.plot_xaxis = None

class SegmentData:
    def __init__(self):
        self.curr_index = 0
        self.prev_index = None
        self.next_index = 1
        self.num_segments = 0
        self.window = Window()
        self.curr_segment = Segment()
        self.prev_segment = Segment()
        self.next_segment = Segment()  

    def to_dict(self):
        return {
            "curr_index": self.curr_index,
            "prev_index": self.prev_index,
            "next_index": self.next_index,
            "num_segments": self.num_segments,
            "window": self.window.to_dict(),
            "curr_segment": self.curr_segment.to_dict(),
            "prev_segment": self.prev_segment.to_dict(),  
            "next_segment": self.next_segment.to_dict()  
        }

    def update_from_dict(self, data):
        self.curr_index = data.get("curr_index")
        self.prev_index = data.get("prev_index")
        self.next_index = data.get("next_index")
        self.num_segments = data.get("num_segments")
        window_data = data.get("window", {})
        self.window.update_from_dict(window_data)
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
        self.next_segments = 0
        self.num_segments = 0
        self.window.reset()
        self.curr_segment.reset()
        self.prev_segment.reset()  
        self.next_segment.reset() 
