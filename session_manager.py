
from tr_editor_gui import TrEditorGui
from session_data import SessionData
import os

class SessionManager:
    def __init__(self, session):
        self.session = session
        self.view = TrEditorGui(self)  

    def new_session(self, file_path):
        self.session.new_session(file_path)
        self.view.update_session_label(os.path.basename(file_path))

    def data_dump(self):
        data = self.session.session_data
        self.view.session_dump_session(data)

