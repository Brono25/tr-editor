import yaml


class SessionManager:
    def __init__(self, session_data, console):
        self.session_data = session_data
        self.console = console

    def new_session(self):
        self.session_data.reset()

    def load_session_data(self, session_name):
        try:
            with open(session_name, "r") as file:
                session_data_dict = yaml.safe_load(file)
                self.session_data.update_from_dict(session_data_dict["session_data"])
            return True
        except (FileNotFoundError, yaml.YAMLError, KeyError):
            self.console.log("Error: file not opened")
            return False

    def import_transcript(self, transcript_filename):
        self.session_data.transcript_filename = transcript_filename
        self.session_data.transcript = []
        with open(self.session_data.transcript_filename, "r") as f:
            for line in f.readlines():
                line = line.rstrip()
                if line:
                    start, end, label, language, text = line.split("|")
                    element = [float(start), float(end), label, language, text]
                    self.session_data.transcript.append(element)

    def trim_transcript(self, trim_start, trim_end, transcript):
        result = []
        offset = trim_end - trim_start

        for seg in transcript:
            seg_start, seg_end, speaker, lang, text = seg

            action = self._trim_type(trim_start, trim_end, seg_start, seg_end)
            if action == "delete":
                continue
            elif action == "trim_middle":
                result.append([seg_start, seg_end - offset, speaker, lang, text])
            elif action == "trim_start":
                result.append(
                    [trim_end - offset, seg_end - offset, speaker, lang, text]
                )
            elif action == "trim_end":
                result.append([seg_start, trim_start, speaker, lang, text])
            elif seg_start >= trim_end:
                result.append(
                    [seg_start - offset, seg_end - offset, speaker, lang, text]
                )
            else:
                result.append(seg)
        return result

    def _trim_type(self, trim_start, trim_end, seg_start, seg_end):
        if trim_end <= trim_start or seg_end <= seg_start:
            raise ValueError("Invalid Range: end time must be greater than start time.")
        if trim_start >= seg_end or trim_end <= seg_start:
            return None
        if trim_start <= seg_start and trim_end >= seg_end:
            return "delete"
        elif trim_start > seg_start and trim_end < seg_end:
            return "trim_middle"
        elif trim_start <= seg_start and trim_end < seg_end:
            return "trim_start"
        elif trim_start > seg_start and trim_end >= seg_end:
            return "trim_end"
