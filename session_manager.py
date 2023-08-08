
from session_view import SessionView

import os

class SessionManager:
    def __init__(self, data, io):

        self.data = data
        self.io = io
        self.view = SessionView(self)  
        
        self.initialise_session()


        
    def initialise_session(self):
        self.session_name = self.io.get_session_name_from_cache()
        if self.session_name:
            self.io.load_data(self.session_name)
            self.update_labels()
            self.view.update_transcript_label(self.data.transcript_filename)
            self.view.activate_open_buttons()
            
    def new_session(self, session_name):
        self.session_name = session_name
        self.io.new_data(self.session_name)
        self.io.save_data(self.session_name)

        self.io.cache_session_name(self.session_name)
        self.update_labels()
        self.view.activate_open_buttons()


    def open_session(self, session_name):
        self.session_name = session_name
        self.io.cache_session_name(self.session_name)
        self.io.load_data(self.session_name)
        self.update_labels()
        self.view.activate_open_buttons()


    def open_transcript(self, transcript_filename):
        
        self.io.load_transcript_into_data(transcript_filename)
        self.io.save_data(self.session_name)
        self.update_labels()


    def update_labels(self):
        self.view.update_transcript_label(self.data.transcript_filename)
        self.view.update_session_label(self.session_name)
        self.view.update_audiofile_label(self.data.audio_filename)


    def data_dump(self):
    
        self.io.dump_data(self.data, self.session_name)

