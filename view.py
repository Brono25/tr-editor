import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from debug import Debug
import os
from view_session_control import SessionControlFrame
from view_segment_control import SegmentControlFrame
from view_plot import PlotFrame
from view_text import TextFrame
import matplotlib

matplotlib.use('TkAgg')  # or another backend such as 'Qt5Agg'


class View:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.session_control_frame = SessionControlFrame(self.root, controller)
        self.segment_control_frame = SegmentControlFrame(self.root, controller)
        self.text_frame = TextFrame(self.root)
        self.plot_frame = PlotFrame(self.root)

    def run(self):
        self.root.mainloop()

    def open_session(self, session_name, session_data, segment_data):
        transcript = session_data.transcript
        self.segment_control_frame.update_segment_control_buttons(len(transcript))
        self._update_session_labels(session_name, session_data)
        self.session_control_frame.activate_open_buttons()
        self.text_frame.update_text(segment_data)
        self.segment_control_frame.update_text_input(segment_data.curr_index)
        self.segment_control_frame.update_line_count_label(len(transcript))

    def new_session(self, session_name, segment_data, session_data):
        self._update_session_labels(session_name, session_data)
        self.text_frame.update_text(segment_data)
        self.session_control_frame.activate_open_buttons()
        self.segment_control_frame.deactivate_segment_control_buttons()
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

    def change_segment_input_box(self, new_index):
        self.controller.change_segment_input_box(new_index)

    def change_segment(self, segment_data):
        self.text_frame.update_text(segment_data)
        self.segment_control_frame.update_text_input(segment_data.curr_index)
        self.segment_control_frame.update_line_count_label(segment_data.num_segments)
        self.segment_control_frame.update_segment_control_buttons(segment_data.num_segments)


    def _update_session_labels(self, session_name, session_data):
        transcript_name = session_data.transcript_filename
        audio_name = session_data.audio_filename
        self.session_control_frame.update_transcript_label(transcript_name)
        self.session_control_frame.update_session_label(session_name)
        self.session_control_frame.update_audiofile_label(audio_name)
