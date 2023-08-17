import yaml
import os


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
        with open(filename, "w") as file:
            for seg in transcript:
                start, end, label, language, text = seg
                line = f"{start}|{end}|{label}|{language}|{text}"
                file.write(line + "\n")
        self.console.log(f"Saved transcript to {filename}")

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
