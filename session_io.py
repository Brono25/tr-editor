

from audio_player import AudioPlayer
import yaml
import os



class SessionIO:
    def __init__(self, session_data):

        self.session_data = session_data
        self.session_cache = ".session_cache"
        self.audio_player = AudioPlayer()
        self.active_session_name = self.get_previous_session_name_from_cache()
        if previous_session := self.active_session_name:
            try:
                self.open_session(previous_session)
            except FileNotFoundError:
                pass
                

    def get_previous_session_name_from_cache(self):
        save_file = self.session_cache
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

    def cache_session_name(self, session_name):
        save_file = self.session_cache
        with open(save_file, 'w') as f:
            f.write(session_name)

    def open_session(self, session_name):
        self.active_session_name = session_name
        self.cache_session_name(session_name)
        self.load_session_data(session_name)
        if file := self.session_data.audio_file_path:
            self.audio_player.load_audio_file(file)
            

    def create_empty_session(self, session_name):
        self.active_session_name = session_name
        self.cache_session_name(session_name)
        self.session_data.reset()
        self.save_session()


    def save_session(self):
        with open(self.active_session_name, 'w') as file:
            yaml.dump(self.session_data.to_dict(), file, default_flow_style=False, sort_keys=False)

        
    def load_session_data(self, session_name):
        try:
            with open(session_name, 'r') as file:
                data_dict = yaml.safe_load(file)
                self.session_data.update_from_dict(data_dict)
        except FileNotFoundError:
            print(f"Error load_session_data: {session_name} not found.")
        except yaml.YAMLError:
            print(f"Error load_session_data: Failed to decode the YAML content in {session_name}.")



    def open_audio_file(self, filename):
        self.session_data.audio_file_path = filename
        self.session_data.audio_filename = os.path.basename(filename)
        self.audio_player.load_audio_file(filename)
        self.save_session()


    def open_transcript(self, filename):
        self.session_data.transcript_path = filename
        self.session_data.transcript_filename = os.path.basename(filename)
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.rstrip()
                start, end, label, language, text = line.split('|')
                element = [float(start), float(end), label, language, text]
                self.session_data.transcript.append(element)

        self.save_session()


    def dump_session_data(self, session_data):
        print(f"\nDumping {self.active_session_name} data:\n-------------------------")
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
