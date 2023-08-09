import yaml


class SegmentManager:
    def __init__(self, segment_data):
        self.segment_data = segment_data

    def load_segment_data(self, session_name):
        try:
            with open(session_name, "r") as file:
                data_dict = yaml.safe_load(file)
                self.segment_data.update_from_dict(data_dict["segment_data"])
            return True
        except (FileNotFoundError, yaml.YAMLError, KeyError):
            return False


    def load_segment_data_from_transcript(self, segment_index, transcript):
        
        segment = transcript[segment_index]
        (
            segment_start,
            segment_end,
            segment_label,
            segment_language,
            segment_text,
        ) = segment
        self.segment_data.segment_index = segment_index
        self.segment_data.segment_start = segment_start
        self.segment_data.segment_end = segment_end
        self.segment_data.segment_label = segment_label
        self.segment_data.segment_language = segment_language
        self.segment_data.segment_text = segment_text
        self.segment_data.window_start = segment_start
        self.segment_data.window_end = segment_end
        self.segment_data.plot_yaxis = "TODO"
        self.segment_data.plot_xaxis = "TODO"
    
