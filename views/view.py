import tkinter as tk

from views.view_console import Console
from views.view_plot import PlotFrame
from views.view_segment import SegmentControlFrame
from views.view_session import SessionControlFrame
from views.view_text import TextFrame
from views.view_window import WindowControlFrame

DELTA = 500 / 1000
SDELTA = 10 / 1000
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
        self.root.title("TR-Editor")
        self.session_ctrl = SessionControlFrame(self)
        self.text_ctrl = TextFrame(self)
        self.segment_ctrl = SegmentControlFrame(self)
        self.window_ctrl = WindowControlFrame(self)
        self.plot_ctrl = PlotFrame(self)
        self.console = Console(self)

        self.function_map = {
            # Session Management
            "open_session": (self.controller.open_session, []),
            "new_session": (self.controller.new_session, []),
            "save_tr": (lambda file: self.controller.save_transcript(file), []),
            "save_rttm": (lambda file: self.controller.save_rttm(file), []),
            "save_audio": (lambda file: self.controller.save_audio(file), []),
            "data_dump": (self.controller.data_dump, []),
            "run_test": (self.controller.run_test, []),
            # Audio and Transcript Management
            "open_audio_file": (self.controller.open_audiofile, []),
            "open_transcript": (self.controller.open_transcript, []),
            # Audio Controls
            "play_audio": (self.controller.play_audio_window, []),
            "skip_play": (self.controller.play_skip_audio, []),
            "play_segment": (self.controller.play_segment, []),
            "stop_audio": (self.controller.stop_audio, []),
            # marker Changes
            "decrease_start": (self.controller.change_marker, [-DELTA]),
            "small_decrease_start": (self.controller.change_marker, [-SDELTA]),
            "increase_start": (self.controller.change_marker, [DELTA]),
            "small_increase_start": (self.controller.change_marker, [SDELTA]),
            "decrease_end": (self.controller.change_marker, [-DELTA, False]),
            "small_decrease_end": (self.controller.change_marker, [-SDELTA, False]),
            "increase_end": (self.controller.change_marker, [DELTA, False]),
            "small_increase_end": (self.controller.change_marker, [SDELTA, False]),
            # Segment Changes
            "decrement_index": (self.controller.change_segment_by_delta, [-1]),
            "increment_index": (self.controller.change_segment_by_delta, [1]),
            "change_seg_input": (lambda i: self.controller.go_to_segment(i), []),
            "proceed_delete": (self.controller.delete_segment, []),
            # Editing
            "trim": (self.controller.trim_audio_and_transcript, []),
            "save_timestamp_edits": (self.controller.edit_timestamps_using_markers, []),
            "transcript_edits": (
                lambda x, y: self.controller.edit_transcript_label_or_language(x, y),
                [],
            ),
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
            self.console.log(f"Function {function_name} not found.")

    def run(self):
        self.root.mainloop()

    # ======================================
    #          UPDATE FOR BUTTON
    # ======================================
    def update_for_open_session(self, session_name, session_data, seg_data, player):
        curr_index = seg_data.curr_index
        transcript = session_data.transcript
        transcript_filename = session_data.transcript_filename
        audio_filename = session_data.audio_filename

        self.set_session_labels(session_name, transcript_filename, audio_filename)
        self.text_ctrl.update_text(seg_data)
        self.segment_ctrl.set_input_text_box_label(curr_index)
        self.segment_ctrl.set_total_num_segments_label(len(transcript))
        self.update_button_state(session_data, seg_data, player)

        if not session_data.audio_filename:
            self.clear_plot()

    def update_for_new_session(self, session_name, seg_data, session_data, player):
        transcript = session_data.transcript
        transcript_filename = session_data.transcript_filename
        audio_filename = session_data.audio_filename

        self.set_session_labels(session_name, transcript_filename, audio_filename)
        self.text_ctrl.update_text(seg_data)
        self.update_button_state(session_data, seg_data, player)
        self.segment_ctrl.set_total_num_segments_label(len(transcript))
        self.segment_ctrl.set_input_text_box_label()
        self.clear_plot()

    def update_for_open_file(
        self, session_name, session_data, seg_data, win_data, player
    ):
        curr_index = seg_data.curr_index
        transcript = session_data.transcript
        transcript_filename = session_data.transcript_filename
        audio_filename = session_data.audio_filename
        self.set_session_labels(session_name, transcript_filename, audio_filename)
        self.text_ctrl.update_text(seg_data)
        self.segment_ctrl.set_total_num_segments_label(len(transcript))
        self.segment_ctrl.set_input_text_box_label(curr_index)
        self.update_button_state(session_data, seg_data, player)

        if player.audio_obj:
            self.update_plot(win_data, player)

    def update_for_change_segment(self, seg_data, win_data, player):
        curr_index = seg_data.curr_index
        num_segments = seg_data.num_segments

        self.text_ctrl.update_text(seg_data)
        self.segment_ctrl.set_input_text_box_label(curr_index)
        self.segment_ctrl.set_total_num_segments_label(num_segments)
        self.update_plot(win_data, player)

    def update_labels_for_save_timestamp_edits(self, seg_data):
        self.update_timestamp_labels(seg_data)

    def play_audio_button(self):
        self.controller.play_audio_segment()

    def set_session_labels(self, session_name, session_data):
        transcript_name = session_data.transcript_filename
        audio_name = session_data.audio_filename
        self.session_ctrl.update_transcript_label(transcript_name)
        self.session_ctrl.update_session_label(session_name)
        self.session_ctrl.update_audiofile_label(audio_name)

    def update_timestamp_labels(self, seg_data):  # XX
        self.text_ctrl.update_text(seg_data)

    def clear_plot(self):
        self.plot_ctrl.plot_audio()

    def update_plot(self, win_data, player):
        w_start = win_data.start
        w_end = win_data.end
        start_marker = win_data.start_marker
        end_marker = win_data.end_marker
        zoom_level = win_data.zoom_scaler
        prev_marker = win_data.prev_marker
        if not w_start and not w_end:
            w_start, w_end = 0, 0
        y, x = player.get_audio_time_vectors(w_start, w_end)
        self.plot_ctrl.plot_audio(x, y / zoom_level)

        self.plot_ctrl.plot_vertical_line(start_marker)
        self.plot_ctrl.plot_vertical_line(end_marker)

        self.plot_ctrl.plot_vertical_line(
            win_data.prev_marker, color="lightblue", linestyle="dashed", label="x1"
        )
        self.plot_ctrl.plot_vertical_line(
            win_data.next_marker, color="#FF6F61", linestyle="dashed", label="x2"
        )

    def update_button_state(self, session_data, seg_data, player):
        if session_data:
            self.session_ctrl.activate_open_buttons()
        if not player.audio_obj:
            self._de_activate_buttons()
        elif not session_data.audio_filename:
            self._de_activate_buttons()
        elif not seg_data.curr_segment:
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
