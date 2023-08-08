

from audio_player import AudioPlayer
import yaml
import os

#Session name is always given to sessionIO or data but not stored or copied in sessionIO or dta
#filename is always full path


class SessionIO:
    def __init__(self, data):

        self.data = data
        self.session_cache = ".treditor_cache"
        self.initialise_cache()
        

    def initialise_cache(self):
        if not os.path.exists(self.session_cache):
            with open(self.session_cache, 'w') as f:
                pass

 
    def get_session_name_from_cache(self):
        with open(self.session_cache, 'r') as f:
            session_name = f.read().strip()
        if session_name.endswith('.yml') and os.path.exists(session_name):
            return session_name
        else:
            return ''

    def cache_session_name(self, session_name):
        save_file = self.session_cache
        with open(save_file, 'w') as f:
            f.write(session_name)


    def new_data(self, session_name):
        self.cache_session_name(session_name)
        self.data.reset()




    def save_data(self, session_name):
        with open(session_name, 'w') as file:
            yaml.dump(self.data.to_dict(), file, default_flow_style=False, sort_keys=False)

        
    def load_data(self, session_name):
        try:
            with open(session_name, 'r') as file:
                data_dict = yaml.safe_load(file)
                self.data.update_from_dict(data_dict)
        except FileNotFoundError:
            print(f"Error load_session_data: {session_name} not found.")
        except yaml.YAMLError:
            print(f"Error load_session_data: Failed to decode the YAML content in {session_name}.")


    def load_transcript_into_data(self, transcript_filename):
        self.data.transcript_filename = transcript_filename
        with open(self.data.transcript_filename, 'r') as f:
            for line in f.readlines():
                line = line.rstrip()
                start, end, label, language, text = line.split('|')
                element = [float(start), float(end), label, language, text]
                self.data.transcript.append(element)

        


    def dump_data(self, data, session_name):
        print(f"\nDumping {session_name} data:\n-------------------------")
        for attr, value in data.__dict__.items():
            if isinstance(value, self.data.State): 
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
