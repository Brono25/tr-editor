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
        self.segment_index = 0

        if session_name := self.utils.get_session_name():
            self.open_session(session_name)

    def open_session(self, session_name):
        self.utils.set_session_name(session_name)
        if self.session_manager.load_session_data(session_name):
            if self.segment_manager.load_segment_data(session_name):

                self.update_labels()
                self.view.activate_open_buttons()

    def new_session(self, session_name):
        self.utils.set_session_name(session_name)
        self.session_data.reset()
        self.segment_data.reset()
        self.save_session(session_name)
        self.update_labels()
        self.view.activate_open_buttons()

    def open_transcript(self, transcript_filename):
        self.session_manager.load_transcript(transcript_filename)
        self.save_session(self.utils.get_session_name())
        self.update_labels()
        self.load_segment(self.segment_index)

    def update_labels(self):
        self.view.update_transcript_label(self.session_data.transcript_filename)
        self.view.update_session_label(self.utils.get_session_name())
        self.view.update_audiofile_label(self.session_data.audio_filename)

    def data_dump(self):
        print(f"Index = {self.segment_index}")
        if session_name := self.utils.get_session_name():
            session_name = os.path.basename(session_name)
            Debug.print_session_data(self.segment_data, f"{session_name} segment data:")
            Debug.print_session_data(self.session_data, f"{session_name} session data:")

    def save_session(self, session_name):
        self.utils.save_session(self.session_data, self.segment_data, session_name)


