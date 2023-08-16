class SessionData:
    def __init__(self):
        self.reset()

    def to_dict(self):
        return {
            "audio_filename": self.audio_filename,
            "transcript_filename": self.transcript_filename,
            "transcript": self.transcript,
        }

    def update_from_dict(self, data):
        self.audio_filename = data.get("audio_filename")
        self.transcript_filename = data.get("transcript_filename")
        self.transcript = data.get("transcript", [])

    def reset(self):
        self.audio_filename = None
        self.transcript_filename = None
        self.transcript = []
