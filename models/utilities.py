import yaml
import os
from pydub import AudioSegment
import shutil

class Utilities:
    def __init__(self, console):
        self.session_cache = ".treditor_cache.yml"
        self.console = console
        self.initialise_cache()

    def save_session(self, session_data, segment_data, window_data, session_name):
        data = {
            "window_data": window_data.to_dict(),
            "segment_data": segment_data.to_dict(),
            "session_data": session_data.to_dict(),
        }
        with open(session_name, "w") as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)



    def backup_save(self, session_data, segment_data, window_data, session_name):
        # Get the directory of the transcript file
        transcript_dir = os.path.dirname(session_data.transcript_filename)

        # Ensure the .backup directory exists in the same directory as the transcript file
        backup_dir = os.path.join(transcript_dir, '.backup')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Split the session name into the base name and extension
        base_name, extension = os.path.splitext(os.path.basename(session_name))

        # Determine the next available backup number
        backup_number = 0
        while True:
            backup_file_name = os.path.join(backup_dir, f'{base_name}_{backup_number}{extension}')
            if not os.path.exists(backup_file_name):
                break
            backup_number += 1

        # Use the save_session method to save the session to the backup file
        self.save_session(session_data, segment_data, window_data, backup_file_name)

        print(f"Backup saved to {backup_file_name}")






    def get_session_name(self):
        with open(self.session_cache, "r") as f:
            cache_data = yaml.safe_load(f)
            session_name = cache_data.get("curr_session_name", "")
            if (
                session_name
                and isinstance(session_name, str)
                and session_name.endswith(".yml")
                and os.path.exists(session_name)
            ):
                return session_name
            else:
                return ""

    def set_session_name(self, session_name):
        with open(self.session_cache, "r") as f:
            cache_data = yaml.safe_load(f)
        cache_data["curr_session_name"] = session_name
        with open(self.session_cache, "w") as f:
            yaml.dump(cache_data, f)

    def initialise_cache(self):
        initial_data = {"curr_session_name": None}

        if os.path.exists(self.session_cache):
            with open(self.session_cache, "r") as f:
                existing_data = yaml.safe_load(f)
                if existing_data is None or not all(
                    key in existing_data for key in initial_data.keys()
                ):
                    remake_file = True
                else:
                    remake_file = False

            if remake_file:
                with open(self.session_cache, "w") as f:
                    yaml.dump(
                        initial_data, f, default_flow_style=False, sort_keys=False
                    )
        else:
            with open(self.session_cache, "w") as f:
                yaml.dump(initial_data, f, default_flow_style=False, sort_keys=False)

    def save_transcript_to_file(self, transcript, filename):
        if filename.endswith(".rttm"):
            filename = filename[:-5]

        with open(filename, "w") as file:
            for seg in transcript:
                start, end, label, language, text = seg
                line = f"{start:.3f}|{end:.3f}|{label}|{language}|{text}"
                file.write(line + "\n")
        self.console.log(f"Saved transcript to {filename}")


    def save_audio(self, ply, filename):
        if filename.endswith('.wav'):
            filename = filename[:-4]

        try:
            ply.audio_obj.export(filename + '.wav', format="wav")
            self.console.log(f"Saved audio to {filename}.wav")
        except Exception as e:
            self.console.log(f"An error occurred while saving the audio: {e}")

    # RTTM format creation adapted from the following source:
    # Title: StackOverflow - RTTM file format
    # URL: https://stackoverflow.com/questions/30975084/rttm-file-format
    def save_transcript_as_rttm(self, transcript, filename):
        file_no_path, _ = os.path.splitext(os.path.basename(filename))
        with open(filename + ".rttm", "wb") as f:
            for seg in transcript:
                start, end, label, _, _ = seg
                duration = end - start
                n_digits = 3
                fields = [
                    "SPEAKER",
                    file_no_path,
                    "1",
                    self.format_float(start, n_digits),
                    self.format_float(duration, n_digits),
                    "<NA>",
                    "<NA>",
                    label,
                    "<NA>",
                    "<NA>",
                ]
                line = " ".join(fields)
                f.write(line.encode("utf-8"))
                f.write(b"\n")
        self.console.log(f"Saved RTTM to {file_no_path }.rttm")

    def format_float(self, number, n_digits):
        return f"{number:.{n_digits}f}"
