



class WindowData:
    def __init__(self, start=None, end=None, zoom_scaler=1):
        self.start = start
        self.end = end
        self.start_marker = None
        self.end_marker = None
        self.zoom_scaler = zoom_scaler
        self.normaliser = None
        self.prev_marker = None 
        self.next_marker = None  

    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "start_marker": self.start_marker,
            "end_marker": self.end_marker,
            "zoom_scaler": self.zoom_scaler,
            "normaliser": self.normaliser,
            "prev_marker": self.prev_marker,
            "next_marker": self.next_marker,
        }

    def update_from_dict(self, data):
        self.start = data.get("start")
        self.end = data.get("end")
        self.start_marker = data.get("start_marker")
        self.end_marker = data.get("end_marker")
        self.zoom_scaler = data.get("zoom_scaler")
        self.normaliser = data.get("normaliser")
        self.prev_marker = data.get("prev_marker")
        self.next_marker = data.get("next_marker")

    def reset(self):
        self.start = None
        self.end = None
        self.start_marker = None
        self.end_marker = None
        self.zoom_scaler = 1
        self.normaliser = None
        self.prev_marker = None
        self.next_marker = None
