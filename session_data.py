class SessionData:
    class State:
        def __init__(self):
            self.start = None
            self.end = None

        def to_dict(self):
            return {
                'start': self.start,
                'end': self.end
            }

        def update_from_dict(self, data):
            self.start = data.get('start')
            self.end = data.get('end')

    def __init__(self):
        self.reset()

    def to_dict(self):
        return {
            'audio_filename': self.audio_filename,
            'transcript_filename': self.transcript_filename,
            'curr_state': self.curr_state.to_dict(),
            'transcript': self.transcript,
        }

    def update_from_dict(self, data):
        self.audio_filename = data.get('audio_filename')
        self.transcript_filename = data.get('transcript_filename')
        if 'curr_state' in data:
            self.curr_state.update_from_dict(data.get('curr_state', {}))
        self.transcript = data.get('transcript', [])

    def reset(self):
        self.audio_filename = None
        self.transcript_filename = None
        self.curr_state = self.State()
        self.transcript = []
