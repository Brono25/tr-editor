import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from view_session_control import SessionControlFrame
from view_segment_control import SegmentControlFrame
from view_window_control import WindowControlFrame
from view_plot import PlotFrame
from view_text import TextFrame
import matplotlib
import os

INCREMENT = 0.25
SMALL_INCREMENT = 25 / 1000

matplotlib.use("TkAgg")  # or another backend such as 'Qt5Agg'


class View:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.session_control_frame = SessionControlFrame(self)
        self.segment_control_frame = SegmentControlFrame(self)
        self.text_frame = TextFrame(self)
        self.window_control_frame = WindowControlFrame(self)
        self.plot_frame = PlotFrame(self)

        # Mapping functions called within frames to corresponding controller 
        # methods for concise access
        self.function_map = {
            "open_session": lambda path: self.controller.open_session(path),
            "new_session": lambda file_path: self.controller.new_session(file_path),
            "open_session": lambda session_path: self.controller.open_session(session_path),
            "open_audio_file": lambda file_path: (self.controller.open_audiofile(file_path)),
            "open_transcript": lambda transcript_filename: self.controller.open_transcript(transcript_filename),
            "decrease_start": lambda: self.controller.change_start_timestamp(INCREMENT * (-1)),
            "small_decrease_start": lambda: self.controller.change_start_timestamp(SMALL_INCREMENT * (-1)),
            "increase_start": lambda: self.controller.change_start_timestamp(INCREMENT),
            "small_increase_start": lambda: self.controller.change_start_timestamp(SMALL_INCREMENT),
            "decrease_end": lambda: self.controller.change_end_timestamp(INCREMENT * (-1)),
            "small_decrease_end": lambda: self.controller.change_end_timestamp(SMALL_INCREMENT * (-1)),
            "increase_end": lambda: self.controller.change_end_timestamp(INCREMENT),
            "small_increase_end": lambda: self.controller.change_end_timestamp(SMALL_INCREMENT),
            "save_timestamp_edits": self.controller.save_timestamp_edits,
            "zoom_in": lambda: print("Zoom in clicked!"),
            "zoom_out": lambda: print("Zoom out clicked!"),
            "proceed_delete": self.controller.delete_segment,
            "data_dump": self.controller.data_dump,
        }

    def call_function(self, function_name):
        if function_name in self.function_map:
            self.function_map[function_name]()


    def run(self):
        self.root.mainloop()

    def open_session(self, session_name, session_data, segment_data):
        transcript = session_data.transcript
        self.segment_control_frame.update_segment_control_buttons(len(transcript))
        self._update_session_labels(session_name, session_data)
        self.session_control_frame.activate_open_buttons()
        self.segment_control_frame.update_play_stop_buttons(session_data.audio_filename)
        self.text_frame.update_text(segment_data)
        self.segment_control_frame.update_text_input(segment_data.curr_index)
        self.segment_control_frame.update_line_count_label(len(transcript))

    def new_session(self, session_name, segment_data, session_data):
        self._update_session_labels(session_name, session_data)
        self.text_frame.update_text(segment_data)
        self.session_control_frame.activate_open_buttons()
        self.segment_control_frame.deactivate_segment_control_buttons()
        self.segment_control_frame.deactivate_play_stop_buttons()
        self.segment_control_frame.update_line_count_label(len(session_data.transcript))
        self.segment_control_frame.update_text_input()

    def open_transcript(self, session_name, session_data, segment_data):
        self._update_session_labels(session_name, session_data)
        self.segment_control_frame.update_segment_control_buttons(
            len(session_data.transcript)
        )
        self.text_frame.update_text(segment_data)
        self.segment_control_frame.update_line_count_label(len(session_data.transcript))
        self.segment_control_frame.update_text_input(segment_data.curr_index)

    def open_audio(self):
            self.segment_control_frame.activate_play_stop_buttons()

    def change_segment_input_box(self, new_index):
        self.controller.change_segment_input_box(new_index)

    def change_segment(self, segment_data):
        self.text_frame.update_text(segment_data)
        self.segment_control_frame.update_text_input(segment_data.curr_index)
        self.segment_control_frame.update_line_count_label(segment_data.num_segments)
        self.segment_control_frame.update_segment_control_buttons(
            segment_data.num_segments
        )

    def play_audio_button(self):
        self.controller.play_audio_segment()

    def _update_session_labels(self, session_name, session_data):
        transcript_name = session_data.transcript_filename
        audio_name = session_data.audio_filename
        self.session_control_frame.update_transcript_label(transcript_name)
        self.session_control_frame.update_session_label(session_name)
        self.session_control_frame.update_audiofile_label(audio_name)

    def update_overlaps_label(self, overlap_text):
        self.text_frame.update_overlaps_label(overlap_text)

    def update_timestamp_labels(self, segment_data):
        self.text_frame.update_text(segment_data)

    def decrement_index(self):
        self.controller.decrement_index()

    def increment_index(self):
        self.controller.increment_index()


    def change_segment_input_box(self, input_value):
        self.controller.change_segment_input_box(input_value)
