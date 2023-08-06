import json

class Data:
    class State:
        def __init__(self):
            self.start = None
            self.end = None

        def to_dict(self):
            return {
                'start': self.start,
                'end': self.end
            }

        @classmethod
        def from_dict(cls, data):
            instance = cls()
            instance.start = data.get('start')
            instance.end = data.get('end')
            return instance

    def __init__(self):
        self.audio_file_path = None
        self.audio_filename = None
        self.transcript_path = None
        self.transcript_filename = None
        self.transcript = []
        self.curr_state = self.State()



    def to_dict(self):
        return {
            'audio_file_path': self.audio_file_path,
            'audio_filename': self.audio_filename,
            'transcript_path': self.transcript_path,
            'transcript_filename': self.transcript_filename,
            'curr_state': self.curr_state.to_dict(),
            'transcript': self.transcript,
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.audio_file_path = data.get('audio_file_path')
        instance.audio_filename = data.get('audio_filename')
        instance.transcript_path = data.get('transcript_path')
        instance.transcript_filename = data.get('transcript_filename')
        instance.curr_state = cls.State.from_dict(data.get('curr_state', {}))
        instance.transcript = data.get('transcript')
        return instance

