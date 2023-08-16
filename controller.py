import os

from audio_player import AudioPlayer
from debug import Debug
from segment_data import SegmentData
from segment_manager import SegmentManager
from session_data import SessionData
from session_manager import SessionManager
from window_data import WindowData
from window_manager import WindowManager
from utilities import Utilities
from view import View


class Controller:
    def __init__(self):
        self.session_data = SessionData()
        self.segment_data = SegmentData()
        self.window_data = WindowData()
        self.session_manager = SessionManager(self.session_data)
        self.segment_manager = SegmentManager(self.segment_data)
        self.window_manager = WindowManager(self.window_data)
        self.utils = Utilities()
        self.view = View(self)
        self.audio_player = AudioPlayer()

        if session_name := self.utils.get_session_name():
            self.open_session(session_name)

    #======================================
    #              FILE IO
    #======================================

    def open_session(self, session_name):
        self.utils.set_session_name(session_name)
        if self.session_manager.load_session_data(session_name):
            self.segment_manager.load_segment_data(session_name)
            self.window_manager.load_window_data(session_name)
            self.view.update_for_open_session(
                session_name, self.session_data, self.segment_data, self.audio_player
            )

        if (audio_filename := self.session_data.audio_filename) is not None:
            self.open_audiofile(audio_filename)

    def new_session(self, session_name):
        self.audio_player.reset()
        self.utils.set_session_name(session_name)
        self.session_manager.new_session()
        self.segment_manager.new_session()
        self.window_manager.new_session()
        self.save_session(session_name)
        self.view.update_for_new_session(
            session_name, self.segment_data, self.session_data, self.audio_player
        )

    def open_transcript(self, transcript_filename):
        self.session_manager.import_transcript(transcript_filename)
        self.segment_manager.initialise_segment_data_from_transcript(self.session_data.transcript)
        session_name = self.utils.get_session_name()
        normaliser = self.audio_player.audio_info.peak_amplitude
        self.window_manager.initialise_window_data(self.segment_data, normaliser)
        self.save_session(session_name)
        self.view.update_for_open_transcript(
            session_name, self.session_data, self.segment_data,self.window_data,  self.audio_player
        )

    def open_audiofile(self, audio_filename):
        session_name = self.utils.get_session_name()
        self.session_data.audio_filename = audio_filename
        self.audio_player.load_audio_file(audio_filename)
        self.save_session(self.utils.get_session_name())
        #self.segment_manager.update_window_timestamp(self.segment_data)
        normaliser = self.audio_player.audio_info.peak_amplitude
        #self.segment_manager.initialise_window_data(self.segment_data, normaliser)
        self.view.update_for_open_transcript(
            session_name, self.session_data, self.segment_data, self.window_data, self.audio_player
        )
        
    #======================================
    #              SEGMENTS
    #======================================
    def change_segment_by_delta(self, delta):
        new_index = self.segment_data.curr_index + delta
        transcript = self.session_data.transcript
        session_name = self.utils.get_session_name()

        self.segment_manager.change_segment(transcript, new_index)
        self.segment_manager.update_overlap_status(self.segment_data, transcript)
        self.window_manager.reset_window_to_match_segment(self.segment_data)
        self.save_session(session_name)

        self.view.update_for_change_segment(self.segment_data, self.window_data, self.audio_player)
        self.audio_player.play_audio(self.window_data.start, self.window_data.end)
        
    def go_to_segment(self, new_index):
        delta = new_index - self.segment_data.curr_index
        self.change_segment_by_delta(delta)

    def delete_segment(self):
        self.segment_manager.delete_segment(self.session_data, self.segment_data)
        self.change_segment_by_delta(delta=0)

    def edit_timestamps_using_markers(self):
        transcript = self.session_data.transcript
        curr_index = self.segment_data.curr_index
        new_start = self.window_data.start_marker
        new_end = self.window_data.end_marker

        self.segment_manager.edit_timestamps(transcript, curr_index, new_start, new_end)
        self.window_manager.reset_window_to_match_segment(self.segment_data)
        self.segment_manager.update_overlap_status(self.segment_data, transcript)
        self.save_session(self.utils.get_session_name())

        self.view.update_labels_for_save_timestamp_edits(self.segment_data)
        self.view.update_plot(self.window_data, self.audio_player)

    #======================================
    #              AUDIO
    #======================================
    def play_audio_window(self):
        start = self.window_data.start
        end = self.window_data.end
        self.audio_player.play_audio(start, end)

    def play_skip_audio(self):
        skip_start = self.window_data.start_marker
        skip_end = self.window_data.end_marker
        start = self.window_data.start
        end = self.window_data.end
        self.audio_player.play_audio(start, end, skip_start, skip_end)

    def play_segment(self):
        start = self.window_data.start_marker
        end = self.window_data.end_marker
        self.audio_player.play_audio(start, end)

    def stop_audio(self):
        self.audio_player.stop_audio()

    #======================================
    #            PLOT WINDOW
    #======================================
    def change_window_start(self, delta):
        new_start = self.window_data.start + delta
        new_start = max(0, min(new_start, self.window_data.start_marker))
        self.window_data.start = new_start
        self.view.update_plot(self.window_data, self.audio_player)

    def change_window_end(self, delta):
        new_start = self.window_data.end + delta
        curr_end = self.window_data.end_marker
        new_start = max(curr_end, min(new_start, self.audio_player.audio_info.duration))
        self.window_data.end = new_start
        self.view.update_plot(self.window_data, self.audio_player)

    def change_start_marker(self, delta):
        duration = self.audio_player.audio_info.duration
        self.window_manager.change_marker_by_delta(delta, duration, is_start=True)
        if self.window_data.start_marker < self.window_data.start:
            self.window_data.start = self.window_data.start_marker
        self.view.update_plot(self.window_data, self.audio_player)

    def change_end_marker(self, delta):
        duration = self.audio_player.audio_info.duration
        self.window_manager.change_marker_by_delta(delta, duration, is_start=False)
        if self.window_data.end_marker > self.window_data.end:
            self.window_data.end = self.window_data.end_marker
        self.view.update_plot(self.window_data, self.audio_player)


    def zoom_plot(self, delta):
        zoom_min, zoom_max = 0.1, 2
        zoom_scaler = self.window_data.zoom_scaler + delta
        zoom_scaler = max(zoom_min, min(zoom_scaler + delta, zoom_max))
        self.window_data.zoom_scaler = zoom_scaler
        self.view.update_plot(self.window_data, self.audio_player)

    #======================================
    #                MISC
    #======================================
    def data_dump(self):
        print(f"Index = {self.segment_data.curr_index}")
        if session_name := self.utils.get_session_name():
            session_name = os.path.basename(session_name)
            Debug.print_session_data(self.window_data, f"{session_name} window data:")
            Debug.print_session_data(self.segment_data, f"{session_name} segment data:")
            Debug.print_session_data(self.session_data, f"{session_name} session data:")

    def save_session(self, session_name):
        self.utils.save_session(self.session_data, self.segment_data, self.window_data, session_name)

