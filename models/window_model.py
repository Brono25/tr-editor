import yaml


class WindowManager:
    def __init__(self, window_data):
        self.window_data = window_data

    def load_window_data(self, session_name):
        try:
            with open(session_name, "r") as file:
                data_dict = yaml.safe_load(file)
                self.window_data.update_from_dict(data_dict["window_data"])
            return True
        except (FileNotFoundError, yaml.YAMLError, KeyError):
            return False

    def new_session(self):
        self.window_data.reset()

    def reset_window_to_match_segment(self, segment_data):
        self.window_data.start = segment_data.curr_segment.start
        self.window_data.end = segment_data.curr_segment.end
        self.window_data.start_marker = segment_data.curr_segment.start
        self.window_data.end_marker = segment_data.curr_segment.end

    def initialise_window_data(self, segment_data, normaliser):
        self.window_data.start = segment_data.curr_segment.start
        self.window_data.end = segment_data.curr_segment.end
        self.window_data.start_marker = segment_data.curr_segment.start
        self.window_data.end_marker = segment_data.curr_segment.end
        self.window_data.normaliser = normaliser
        self.window_data.zoom_scaler = 1

    def change_marker_by_delta(self, delta, duration, is_start):
        curr_start = self.window_data.start_marker
        curr_end = self.window_data.end_marker

        if is_start:
            new_start = max(0, min(curr_end, curr_start + delta))
            self.window_data.start_marker = new_start
        else:
            new_end = max(curr_start, min(duration, curr_end + delta))
            self.window_data.end_marker = new_end

    def set_prev_next_markers(self, curr_index, transcript):
        self._set_next_start_marker(curr_index, transcript)
        self._set_prev_end_marker(curr_index, transcript)

    def _set_prev_end_marker(self, curr_index, transcript):
        if not transcript:
            return None
        _, _, curr_label, _, _ = transcript[curr_index]
        for index in range(curr_index - 1, -1, -1):
            _, end_marker, label, _, _ = transcript[index]
            if label == curr_label:
                self.window_data.prev_marker = end_marker
                return end_marker
        self.window_data.prev_marker = None
        return None

    def _set_next_start_marker(self, curr_index, transcript):
        if not transcript or curr_index >= len(transcript) - 1:
            self.window_data.next_marker = None
            return None

        _, _, curr_label, _, _ = transcript[curr_index]
        for index in range(curr_index + 1, len(transcript)):
            start_marker, _, label, _, _ = transcript[index]
            if label == curr_label:
                self.window_data.next_marker = start_marker
                return start_marker
        self.window_data.next_marker = None
        return None
