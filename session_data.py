
from data import Data
from audio_player import AudioPlayer
import yaml
import os

SESSION_SAVE_FILE = ".treditor_save"

class SessionData:
    def __init__(self):
        
        self.audio_player = AudioPlayer()
        self.active_session_file = self.get_previous_session_file()
        if previous_session := self.active_session_file:
            self.open_session(previous_session)

    def get_previous_session_file(self):
        save_file = SESSION_SAVE_FILE
        if not os.path.exists(save_file):
            with open(save_file, 'w') as f:
                pass
            return None
        with open(save_file, 'r') as f:
            session_path = f.read().strip()
        if session_path.endswith('.yml') and os.path.exists(session_path):
            return session_path
        else:
            return None

    def update_previous_session_file(self, session_name):
        save_file = SESSION_SAVE_FILE
        with open(save_file, 'w') as f:
            f.write(session_name)

    def open_session(self, filename):
        self.active_session_file = filename
        self.active_session_filename = os.path.basename(filename)
        self.update_previous_session_file(filename)
        self.session_data = self.get_session_data_from_file(filename)
        if file := self.session_data.audio_file_path:
            self.audio_player.load_audio_file(file)
            

    def new_session(self, filename):
        self.active_session_file = filename
        self.session_data = Data()
        self.update_session()


    def update_session(self):
        with open(self.active_session_file, 'w') as file:
            yaml.dump(self.session_data.to_dict(), file, default_flow_style=False, sort_keys=False)

        
    def get_session_data_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = yaml.safe_load(file)
                session_data = Data.from_dict(data)
                return session_data
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return None
        except yaml.YAMLError:
            print(f"Error: Failed to decode the YAML content in {filename}.")
            return None

    def open_audio_file(self, filename):
        self.session_data.audio_file_path = filename
        self.session_data.audio_filename = os.path.basename(filename)
        self.audio_player.load_audio_file(filename)
        self.update_session()


    def open_transcript(self, filename):
        self.session_data.transcript_path = filename
        self.session_data.transcript_filename = os.path.basename(filename)
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.rstrip()
                start, end, label, language, text = line.split('|')
                element = [float(start), float(end), label, language, text]
                self.session_data.transcript.append(element)

        self.update_session()

    def play_audio_segment(self):
        start = self.session_data.curr_state.start
        end = self.session_data.curr_state.end
        self.audio_player.play_audio(start, end)


    def dump_session(self, session_data):
        print(f"\nDumping {self.active_session_filename} data:\n-------------------------")
        for attr, value in session_data.__dict__.items():
            if isinstance(value, self.session_data.State): 
                print(f"{attr} (State Data):")
                for state_attr, state_value in value.__dict__.items():
                    print(f"\t{state_attr}: {state_value}")
            elif attr == 'transcript':
                print(f"{attr}:")
                for line in value:
                    print(f"    {line}")
            else:
                print(f"{attr}: {value}")
        print("-------------------------")
