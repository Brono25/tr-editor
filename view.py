import os
import tkinter as tk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from view_plot import PlotFrame
from view_segment_control import SegmentControlFrame
from view_session_control import SessionControlFrame
from view_text import TextFrame
from view_window_control import WindowControlFrame

DELTA = 250 / 1000
SDELTA = 25 / 1000
ZOOM_DELTA = 0.1
# matplotlib.use("TkAgg")  # or another backend such as 'Qt5Agg'


class View:
    """
    Manages the user interface by controlling different frames and
    coordinating actions between them and the controller.
    """

    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.session_ctrl = SessionControlFrame(self)
        self.segment_ctrl = SegmentControlFrame(self)
        self.text_ctrl = TextFrame(self)
        self.window_ctrl = WindowControlFrame(self)
        self.plot_ctrl = PlotFrame(self)

        self.function_map = {
            # Session Management
            "open_session": (self.controller.open_session, []),
            "new_session": (self.controller.new_session, []),
            "data_dump": (self.controller.data_dump, []),
            # Audio and Transcript Management
            "open_audio_file": (self.controller.open_audiofile, []),
            "open_transcript": (self.controller.open_transcript, []),
            # Timestamp Changes
            "decrease_start": (self.controller.change_start_timestamp, [-DELTA]),
            "small_decrease_start": (self.controller.change_start_timestamp, [-SDELTA]),
            "increase_start": (self.controller.change_start_timestamp, [DELTA]),
            "small_increase_start": (self.controller.change_start_timestamp, [SDELTA]),
            "decrease_end": (self.controller.change_end_timestamp, [-DELTA]),
            "small_decrease_end": (self.controller.change_end_timestamp, [-SDELTA]),
            "increase_end": (self.controller.change_end_timestamp, [DELTA]),
            "small_increase_end": (self.controller.change_end_timestamp, [SDELTA]),
            "save_timestamp_edits": (self.controller.save_timestamp_edits, []),
            # Segment Changes
            "decrement_index": (self.controller.change_segment_by_delta, [-1]),
            "increment_index": (self.controller.change_segment_by_delta, [1]),
            "change_seg_input": (lambda i: self.controller.go_to_segment(i), []),
            "proceed_delete": (self.controller.delete_segment, []),
            # View Control
            "zoom_in": (lambda x: self.controller.zoom_plot(x), [-ZOOM_DELTA]),
            "zoom_out": (lambda x: self.controller.zoom_plot(x), [ZOOM_DELTA]),
        }

    def call_function(self, function_name, *args):
        func, default_args = self.function_map.get(function_name, (None, []))
        if func:
            func(*default_args, *args)
        else:
            print(f"Function {function_name} not found.")

    def run(self):
        self.root.mainloop()

    def update_for_open_session(self, session_name, session_data, segment_data):
        transcript = session_data.transcript
        self.segment_ctrl.update_segment_control_buttons(len(transcript))
        self._update_session_labels(session_name, session_data)
        self.session_ctrl.activate_open_buttons()
        self.segment_ctrl.update_play_stop_buttons(session_data.audio_filename)
        self.text_ctrl.update_text(segment_data)
        self.segment_ctrl.update_text_input(segment_data.curr_index)
        self.segment_ctrl.update_line_count_label(len(transcript))

    def update_for_new_session(self, session_name, segment_data, session_data):
        self._update_session_labels(session_name, session_data)
        self.text_ctrl.update_text(segment_data)
        self.session_ctrl.activate_open_buttons()
        self.segment_ctrl.deactivate_segment_control_buttons()
        self.segment_ctrl.deactivate_play_stop_buttons()
        self.segment_ctrl.update_line_count_label(len(session_data.transcript))
        self.segment_ctrl.update_text_input()
        self.text_ctrl.update_overlaps_label(None)
        self.clear_plot()

    def update_for_open_transcript(self, session_name, session_data, segment_data):
        self._update_session_labels(session_name, session_data)
        self.segment_ctrl.update_segment_control_buttons(len(session_data.transcript))
        self.text_ctrl.update_text(segment_data)
        self.segment_ctrl.update_line_count_label(len(session_data.transcript))
        self.segment_ctrl.update_text_input(segment_data.curr_index)

    def activate_audio_controls(self):
        self.segment_ctrl.activate_play_stop_buttons()

    def update_for_change_segment(self, segment_data):
        self.text_ctrl.update_text(segment_data)
        self.segment_ctrl.update_text_input(segment_data.curr_index)
        self.segment_ctrl.update_line_count_label(segment_data.num_segments)
        self.segment_ctrl.update_segment_control_buttons(segment_data.num_segments)

    def play_audio_button(self):
        self.controller.play_audio_segment()

    def _update_session_labels(self, session_name, session_data):
        transcript_name = session_data.transcript_filename
        audio_name = session_data.audio_filename
        self.session_ctrl.update_transcript_label(transcript_name)
        self.session_ctrl.update_session_label(session_name)
        self.session_ctrl.update_audiofile_label(audio_name)

    def update_overlaps_label(self, overlap_text):
        self.text_ctrl.update_overlaps_label(overlap_text)

    def update_timestamp_labels(self, segment_data):
        self.text_ctrl.update_text(segment_data)

    def plot_audio(self, x, y):
        self.plot_ctrl.plot_audio(x, y)

    def clear_plot(self):
        self.plot_ctrl.plot_audio()
