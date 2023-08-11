from audio_player import AudioPlayer
import yaml
import os

# controlls the io of sessionsession_data


class SessionManager:
    def __init__(self, session_data):
        self.session_data = session_data

    def load_session_data_from_savefile(self, session_name):
        try:
            with open(session_name, "r") as file:
                session_data_dict = yaml.safe_load(file)
                self.session_data.update_from_dict(session_data_dict["session_data"])
            return True
        except (FileNotFoundError, yaml.YAMLError, KeyError):
            return False

    def load_transcript(self, transcript_filename):
        self.session_data.transcript_filename = transcript_filename
        self.session_data.transcript = []
        with open(self.session_data.transcript_filename, "r") as f:
            for line in f.readlines():
                line = line.rstrip()
                if line:
                    start, end, label, language, text = line.split("|")
                    element = [float(start), float(end), label, language, text]
                    self.session_data.transcript.append(element)
    
