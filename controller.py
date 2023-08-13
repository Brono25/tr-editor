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
        if self.session_manager.open_session(session_name):
            self.segment_manager.open_session(session_name)
            self.view.open_session(session_name, self.session_data, self.segment_data)
            self.detect_overlap(self.segment_data.curr_index, self.session_data.transcript)


    def new_session(self, session_name):
        self.utils.set_session_name(session_name)
        self.session_manager.new_session()
        self.segment_manager.new_session()
        self.save_session(session_name)
        self.view.new_session(session_name, self.segment_data, self.session_data)
        self.view.update_overlaps_label(None)

    def open_transcript(self, transcript_filename):
        self.session_manager.open_transcript(transcript_filename)
        self.segment_manager.open_transcript(self.session_data.transcript)
        session_name = self.utils.get_session_name()
        self.save_session(session_name)
        self.view.open_transcript(session_name, self.session_data, self.segment_data)


    def increment_index(self):
        new_index = self.segment_data.curr_index + 1
        transcript = self.session_data.transcript
        self.segment_manager.change_segment(transcript, new_index)
        self.save_session(self.utils.get_session_name())
        self.view.change_segment(self.segment_data)
        self.detect_overlap(self.segment_data.curr_index, transcript)

    def decrement_index(self):
        new_index = self.segment_data.curr_index - 1
        transcript = self.session_data.transcript
        self.segment_manager.change_segment(transcript, new_index)
        self.save_session(self.utils.get_session_name())
        self.view.change_segment(self.segment_data)
        self.detect_overlap(self.segment_data.curr_index, transcript)

    def change_segment_input_box(self, new_index):
        transcript = self.session_data.transcript
        self.segment_manager.change_segment(transcript, new_index)
        self.save_session(self.utils.get_session_name())
        self.view.change_segment(self.segment_data)
        self.detect_overlap(self.segment_data.curr_index, transcript)

    def delete_segment(self):
        transcript = self.session_data.transcript
        self.segment_manager.delete_segment(self.session_data, self.segment_data)
        self.segment_manager.change_segment(transcript, self.segment_data.prev_index)
        self.save_session(self.utils.get_session_name())
        self.view.change_segment(self.segment_data)
        self.detect_overlap(self.segment_data.curr_index, transcript)

    def save_session(self, session_name):
        self.utils.save_session(self.session_data, self.segment_data, session_name)

    def data_dump(self):
        print(f"Index = {self.segment_data.curr_index}")
        if session_name := self.utils.get_session_name():
            session_name = os.path.basename(session_name)
            Debug.print_session_data(self.segment_data, f"{session_name} segment data:")
            Debug.print_session_data(self.session_data, f"{session_name} session data:")

    def detect_overlap(self, curr_index, transcript):
        overlap_status = self.segment_manager.detect_overlap(curr_index, transcript)
        self.view.update_overlaps_label(overlap_status)
