from view import View
from session_data import SessionData
from utilities import Utilities
from segment_data import SegmentData
from session_manager import SessionManager
from segment_data import SegmentData
from segment_manager import SegmentManager
from debug import Debug

import os


class Controller:
    def __init__(self):
        self.session_data = SessionData()
        self.segment_data = SegmentData()
        self.session_manager = SessionManager(self.session_data)
        self.segment_manager = SegmentManager(self.segment_data)
        self.utils = Utilities()
        self.view = View(self)

        self.view_seg_ctrl = self.view.segment_control_frame
        self.view_sess_ctrl = self.view.session_control_frame
        self.view_plot = self.view.plot_frame
        self.view_text = self.view.text_frame

        if session_name := self.utils.get_session_name():
            self.open_session(session_name)
       

    def open_session(self, session_name):
        self.utils.set_session_name(session_name)
        if self.session_manager.load_session_data_from_savefile(session_name):
            if self.segment_manager.load_segment_data_from_savefile(session_name):
                self.update_labels()
                self.view_sess_ctrl.activate_open_buttons()
                self.view_seg_ctrl.update_line_count_label(len(self.session_data.transcript))
        self.view_seg_ctrl.update_segment_control_buttons(self.session_data)
        self.view_text.update_text(self.segment_data)

    def new_session(self, session_name):
        self.utils.set_session_name(session_name)
        self.session_data.reset()
        self.segment_data.reset()
        self.save_session(session_name)
        self.update_labels()
        self.view_text.update_text(self.segment_data)
        self.view_sess_ctrl.activate_open_buttons()
        self.view_seg_ctrl.deactivate_segment_control_buttons()
        self.view_seg_ctrl.update_line_count_label(len(self.session_data.transcript))

    def open_transcript(self, transcript_filename):
        self.session_manager.load_transcript(transcript_filename)
        self.segment_manager.initialise_segment_data_from_transcript(
            self.session_data.transcript
        )
        self.save_session(self.utils.get_session_name())
        self.update_labels()
        self.view_seg_ctrl.update_segment_control_buttons(self.session_data)
        self.view_text.update_text(self.segment_data)
        self.view_seg_ctrl.update_line_count_label(len(self.session_data.transcript))

    def update_labels(self):
        self.view_sess_ctrl.update_transcript_label(self.session_data.transcript_filename)
        self.view_sess_ctrl.update_session_label(self.utils.get_session_name())
        self.view_sess_ctrl.update_audiofile_label(self.session_data.audio_filename)

    def data_dump(self):
        print(f"Index = {self.segment_data.curr_index}")
        if session_name := self.utils.get_session_name():
            session_name = os.path.basename(session_name)
            Debug.print_session_data(self.segment_data, f"{session_name} segment data:")
            Debug.print_session_data(self.session_data, f"{session_name} session data:")

    def change_segment_index(self, index):
        p_i, c_i, n_i = self.segment_manager.get_prev_curr_next_indexes(index)
        self.segment_manager.change_segment(self.session_data.transcript, p_i, c_i, n_i)
        self.save_session(self.utils.get_session_name())
        self.view_text.update_text(self.segment_data)

    def increment_index(self):
        new_index = self.segment_data.curr_index + 1
        p_i, c_i, n_i = self.segment_manager.get_prev_curr_next_indexes(new_index)
        self.segment_manager.change_segment(self.session_data.transcript, p_i, c_i, n_i)
        self.save_session(self.utils.get_session_name())
        self.view_text.update_text(self.segment_data)
        self.view_seg_ctrl.update_text_input(c_i)

    def decrement_index(self):
        new_index = self.segment_data.curr_index - 1
        p_i, c_i, n_i = self.segment_manager.get_prev_curr_next_indexes(new_index)
        self.segment_manager.change_segment(self.session_data.transcript, p_i, c_i, n_i)
        self.save_session(self.utils.get_session_name())
        self.view_text.update_text(self.segment_data)
        self.view_seg_ctrl.update_text_input(c_i)

    def save_session(self, session_name):
        self.utils.save_session(self.session_data, self.segment_data, session_name)
