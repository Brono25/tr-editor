import os

from audio_player import AudioPlayer
from debug import Debug
from segment_data import SegmentData
from segment_manager import SegmentManager
from session_data import SessionData
from session_manager import SessionManager
from utilities import Utilities
from view import View


class Controller:
    def __init__(self):
        self.session_data = SessionData()
        self.segment_data = SegmentData()
        self.session_manager = SessionManager(self.session_data)
        self.segment_manager = SegmentManager(self.segment_data)
        self.utils = Utilities()
        self.view = View(self)
        self.audio_player = AudioPlayer()

        if session_name := self.utils.get_session_name():
            self.open_session(session_name)

    def open_session(self, session_name):
        self.utils.set_session_name(session_name)
        if self.session_manager.open_session(session_name):
            self.segment_manager.open_session(session_name)
            self.view.update_for_open_session(
                session_name, self.session_data, self.segment_data, self.audio_player
            )
            self.detect_overlap(
                self.segment_data.curr_index, self.session_data.transcript
            )
        if (audio_filename := self.session_data.audio_filename) is not None:
            self.open_audiofile(audio_filename)
        else:
            self.view.clear_plot()

    def new_session(self, session_name):
        self.utils.set_session_name(session_name)
        self.session_manager.new_session()
        self.segment_manager.new_session()
        self.save_session(session_name)
        self.view.update_for_new_session(
            session_name, self.segment_data, self.session_data, self.audio_player
        )

    def open_transcript(self, transcript_filename):
        self.session_manager.open_transcript(transcript_filename)
        self.segment_manager.open_transcript(self.session_data.transcript)
        session_name = self.utils.get_session_name()
        self.save_session(session_name)
        self.view.update_for_open_transcript(
            session_name, self.session_data, self.segment_data, self.audio_player
        )

    def open_audiofile(self, audio_filename):
        session_name = self.utils.get_session_name()
        self.session_data.audio_filename = audio_filename
        self.audio_player.load_audio_file(audio_filename)
        self.save_session(self.utils.get_session_name())
        self.segment_manager.update_window_timestamp(self.segment_data)
        normaliser = self.audio_player.audio_info.peak_amplitude
        self.segment_manager.initialise_window_data(self.segment_data, normaliser)
        self.view.update_for_open_transcript(
            session_name, self.session_data, self.segment_data, self.audio_player
        )
        self.view.update_plot(self.segment_data, self.audio_player)

    def change_segment_by_delta(self, delta):
        new_index = self.segment_data.curr_index + delta
        transcript = self.session_data.transcript
        self.segment_manager.change_segment(transcript, new_index)
        self.save_session(self.utils.get_session_name())
        self.view.update_for_change_segment(self.segment_data)
        self.detect_overlap(self.segment_data.curr_index, transcript)
        self.view.update_plot(self.segment_data, self.audio_player)
        self.audio_player.play_audio(
            self.segment_data.window.start, self.segment_data.window.end
        )

    def go_to_segment(self, new_index):
        delta = new_index - self.segment_data.curr_index
        self.change_segment_by_delta(delta)

    def delete_segment(self):
        self.segment_manager.delete_segment(self.session_data, self.segment_data)
        self.change_segment_by_delta(delta=0)

    def save_session(self, session_name):
        self.utils.save_session(self.session_data, self.segment_data, session_name)

    def play_audio_segment(self):
        start = self.segment_data.window.start
        end = self.segment_data.window.end
        self.audio_player.play_audio(start, end)

    def data_dump(self):
        print(f"Index = {self.segment_data.curr_index}")
        if session_name := self.utils.get_session_name():
            session_name = os.path.basename(session_name)
            Debug.print_session_data(self.segment_data, f"{session_name} segment data:")
            Debug.print_session_data(self.session_data, f"{session_name} session data:")

    def detect_overlap(self, curr_index, transcript):
        overlap_status = self.segment_manager.detect_overlap(curr_index, transcript)
        self.view.update_overlaps_label(overlap_status)

    def zoom_plot(self, delta):
        zoom_min, zoom_max = 0.1, 2
        zoom_scaler = self.segment_data.window.zoom_scaler + delta
        zoom_scaler = max(zoom_min, min(zoom_scaler + delta, zoom_max))
        self.segment_data.window.zoom_scaler = zoom_scaler
        self.view.update_plot(self.segment_data, self.audio_player)

    def change_window_start(self, delta):
        new_start = self.segment_data.window.start + delta
        new_start = max(0, min(new_start, self.segment_data.curr_segment.start))
        self.segment_data.window.start = new_start
        self.view.update_plot(self.segment_data, self.audio_player)

    def change_window_end(self, delta):
        new_start = self.segment_data.window.end + delta
        curr_end = self.segment_data.curr_segment.end
        new_start = max(curr_end, min(new_start, self.audio_player.audio_info.duration))
        self.segment_data.window.end = new_start
        self.view.update_plot(self.segment_data, self.audio_player)

    def change_start_timestamp(self, delta):
        duration = self.audio_player.audio_info.duration
        self.segment_manager.change_timestamp(delta, self.segment_data, duration,  is_start=True)
        if self.segment_data.curr_segment.start < self.segment_data.window.start:
            self.segment_data.window.start = self.segment_data.curr_segment.start
        self.view.update_plot(self.segment_data, self.audio_player)

    def change_end_timestamp(self, delta):
        duration = self.audio_player.audio_info.duration
        self.segment_manager.change_timestamp(delta, self.segment_data, duration, is_start=False)
        if self.segment_data.curr_segment.end > self.segment_data.window.end:
            self.segment_data.window.end = self.segment_data.curr_segment.end
        self.view.update_plot(self.segment_data, self.audio_player)

    def save_timestamp_edits(self):
        transcript = self.session_data.transcript
        self.segment_manager.copy_timestamp_edits_to_transcript(
            self.segment_data, transcript
        )
        self.save_session(self.utils.get_session_name())
        self.view.update_timestamp_labels(self.segment_data)
        self.detect_overlap(self.segment_data.curr_index, self.session_data.transcript)



