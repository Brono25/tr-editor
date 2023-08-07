
from session_view import SessionView

import os

class SessionManager:
    def __init__(self, session_data, io):

        self.session_data = session_data
        self.io = io
        self.view = SessionView(self)  
        self.view.update_session_label(os.path.basename(self.io.active_session_name))

    def new_session(self, session_name):
        self.io.create_empty_session(session_name)
        self.view.update_session_label(os.path.basename(session_name))

    def open_session(self, session_name):
        self.io.load_session_data(session_name)
        self.view.update_session_label(os.path.basename(session_name))
        

    def data_dump(self):
        
        self.io.dump_session_data(self.session_data)

