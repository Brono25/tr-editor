import os
import tkinter as tk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from view_plot import PlotFrame
from view_segment_control import SegmentControlFrame
from view_session_control import SessionControlFrame
from view_text import TextFrame
from view_window_control import WindowControlFrame
from view_console import ConsoleFrame

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
        self.text_ctrl = TextFrame(self)
        self.segment_ctrl = SegmentControlFrame(self)
        self.window_ctrl = WindowControlFrame(self)
        self.plot_ctrl = PlotFrame(self)
        self.console = ConsoleFrame(self)
        for i in range(100):
            self.console.log("This is a log message.")
    

        self.function_map = {
            # Session Management
            "open_session": (self.controller.open_session, []),
            "new_session": (self.controller.new_session, []),
            "data_dump": (self.controller.data_dump, []),
            # Audio and Transcript Management
            "open_audio_file": (self.controller.open_audiofile, []),
            "open_transcript": (self.controller.open_transcript, []),
            # Audio Controls
            "play_audio": (self.controller.play_audio_window, []),
            "skip_play": (self.controller.play_skip_audio, []),
            "play_segment": (self.controller.play_segment, []),
            "stop_audio": (self.controller.stop_audio, []),
            # Timestamp Changes
            "decrease_start": (self.controller.change_start_marker, [-DELTA]),
            "small_decrease_start": (self.controller.change_start_marker, [-SDELTA]),
            "increase_start": (self.controller.change_start_marker, [DELTA]),
            "small_increase_start": (self.controller.change_start_marker, [SDELTA]),
            "decrease_end": (self.controller.change_end_marker, [-DELTA]),
            "small_decrease_end": (self.controller.change_end_marker, [-SDELTA]),
            "increase_end": (self.controller.change_end_marker, [DELTA]),
            "small_increase_end": (self.controller.change_end_marker, [SDELTA]),
            "save_timestamp_edits": (self.controller.edit_timestamps_using_markers, []),
            # Segment Changes
            "decrement_index": (self.controller.change_segment_by_delta, [-1]),
            "increment_index": (self.controller.change_segment_by_delta, [1]),
            "change_seg_input": (lambda i: self.controller.go_to_segment(i), []),
            "proceed_delete": (self.controller.delete_segment, []),
            # View Control
            "zoom_in": (lambda x: self.controller.zoom_plot(x), [-ZOOM_DELTA]),
            "zoom_out": (lambda x: self.controller.zoom_plot(x), [ZOOM_DELTA]),
            "window_start_decrease": (
                lambda x: self.controller.change_window_start(x),
                [-DELTA],
            ),
            "window_start_increase": (
                lambda x: self.controller.change_window_start(x),
                [DELTA],
            ),
            "window_end_decrease": (
                lambda x: self.controller.change_window_end(x),
                [-DELTA],
            ),
            "window_end_increase": (
                lambda x: self.controller.change_window_end(x),
                [DELTA],
            ),
        }

    def call_function(self, function_name, *args):
        func, default_args = self.function_map.get(function_name, (None, []))
        if func:
            func(*default_args, *args)
        else:
            print(f"Function {function_name} not found.")

    def run(self):
        self.root.mainloop()

    #======================================
    #          UPDATE FOR BUTTON
    #======================================
    def update_for_open_session(
        self, session_name, session_data, segment_data, audio_player
    ):
        curr_index = segment_data.curr_index
        transcript = session_data.transcript
        transcript_filename = session_data.transcript_filename
        audio_filename = session_data.audio_filename

        self.set_session_labels(session_name, transcript_filename, audio_filename)
        self.text_ctrl.update_text(segment_data)
        self.segment_ctrl.set_input_text_box_label(curr_index)
        self.segment_ctrl.set_total_num_segments_label(len(transcript))
        self.update_button_state(session_data, segment_data, audio_player)
        
        
        if not session_data.audio_filename:
            self.clear_plot()

    def update_for_new_session(
        self, session_name, segment_data, session_data, audio_player
    ):
        transcript = session_data.transcript
        transcript_filename = session_data.transcript_filename
        audio_filename = session_data.audio_filename

        self.set_session_labels(session_name, transcript_filename, audio_filename)
        self.text_ctrl.update_text(segment_data)
        self.update_button_state(session_data, segment_data, audio_player)
        self.segment_ctrl.set_total_num_segments_label(len(transcript))
        self.segment_ctrl.set_input_text_box_label()
        self.text_ctrl.update_overlaps_label(None)
        self.clear_plot()

    def update_for_open_transcript(
        self, session_name, session_data, segment_data, window_data, audio_player
    ):
        curr_index = segment_data.curr_index
        transcript = session_data.transcript
        transcript_filename = session_data.transcript_filename
        audio_filename = session_data.audio_filename
        self.set_session_labels(session_name, transcript_filename, audio_filename)
        self.text_ctrl.update_text(segment_data)
        self.segment_ctrl.set_total_num_segments_label(len(transcript))
        self.segment_ctrl.set_input_text_box_label(curr_index)
        self.update_button_state(session_data, segment_data, audio_player)
        
        if audio_player.audio_obj:
            self.update_plot(window_data, audio_player)

    def update_for_change_segment(self, segment_data, window_data, audio_player):
        curr_index = segment_data.curr_index
        num_segments = segment_data.num_segments

        self.text_ctrl.update_text(segment_data)
        self.segment_ctrl.set_input_text_box_label(curr_index)
        self.segment_ctrl.set_total_num_segments_label(num_segments)
        self.update_plot(window_data, audio_player)


        #

    def update_labels_for_save_timestamp_edits(self, segment_data):
        self.update_timestamp_labels(segment_data)
        

    def play_audio_button(self):
        self.controller.play_audio_segment()

    def set_session_labels(self, session_name, session_data):
        transcript_name = session_data.transcript_filename
        audio_name = session_data.audio_filename
        self.session_ctrl.update_transcript_label(transcript_name)
        self.session_ctrl.update_session_label(session_name)
        self.session_ctrl.update_audiofile_label(audio_name)

    def update_timestamp_labels(self, segment_data): #XX 
        self.text_ctrl.update_text(segment_data)


    def clear_plot(self):
        self.plot_ctrl.plot_audio()

    def update_plot(self, window_data, audio_player):
        w_start = window_data.start
        w_end = window_data.end
        start_marker = window_data.start_marker
        end_marker = window_data.end_marker
        zoom_level = window_data.zoom_scaler
        if not w_start and not w_end:
            w_start, w_end = 0, 0
        y, x = audio_player.get_audio_time_vectors(w_start, w_end)
        self.plot_ctrl.plot_audio(x, y / zoom_level)
        self.plot_ctrl.plot_segment_bounds(start_marker, end_marker)
        #self.plot_ctrl.plot_overlapped_line(segment_data.overlap_timestamp)

    def update_button_state(self, session_data, segment_data, audio_player):

        if session_data:
            self.session_ctrl.activate_open_buttons()
        if not audio_player.audio_obj:
            self._de_activate_buttons()
        elif not session_data.audio_filename:
            self._de_activate_buttons()
        elif not segment_data.curr_segment:
            self._de_activate_buttons()
        elif not session_data.transcript_filename:
            self._de_activate_buttons()
        elif not session_data.transcript:
            self._de_activate_buttons()
        else:
            self._activate_buttons()

    def _activate_buttons(self):
        self.session_ctrl.activate_open_buttons()
        self.window_ctrl.activate_buttons()
        self.segment_ctrl.activate_segment_control_buttons()

    def _de_activate_buttons(self):
        self.window_ctrl.deactivate_buttons()
        self.segment_ctrl.deactivate_segment_control_buttons()

    def set_session_labels(self, session_name, transcript_filename, audio_filename):
        self.session_ctrl.update_audiofile_label(audio_filename)
        self.session_ctrl.update_transcript_label(transcript_filename)
        self.session_ctrl.update_session_label(session_name)

 
