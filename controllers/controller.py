import os

from controllers.audio_player import AudioPlayer
from models.debug import Debug
from models.segment_data import SegmentData
from models.segment_manager import SegmentManager
from models.session_data import SessionData
from models.session_manager import SessionManager
from models.window_data import WindowData
from models.window_manager import WindowManager
from models.utilities import Utilities
from views.view import View


class Controller:
    def __init__(self):
        self.view = View(self)
        self.console = self.view.console
        self.ses_data = SessionData()
        self.seg_data = SegmentData()
        self.win_data = WindowData()
        self.ses_mgr = SessionManager(self.ses_data, self.console)
        self.seg_mgr = SegmentManager(self.seg_data, self.console)
        self.win_mgr = WindowManager(self.win_data)
        self.utils = Utilities(self.console)
        self.plyr = AudioPlayer(self.console)

        if session_name := self.utils.get_session_name():
            self.open_session(session_name)

    # ======================================
    #               FILE IO
    # ======================================

    def open_session(self, session_name):
        self.utils.set_session_name(session_name)
        if self.ses_mgr.load_session_data(session_name):
            self.seg_mgr.load_segment_data(session_name)
            self.win_mgr.load_window_data(session_name)
            self.view.update_for_open_session(
                session_name, self.ses_data, self.seg_data, self.plyr
            )

        if (audio_filename := self.ses_data.audio_filename) is not None:
            self.open_audiofile(audio_filename)
        self.console.clear()

    def new_session(self, session_name):
        self.plyr.reset()
        self.utils.set_session_name(session_name)
        self.ses_mgr.new_session()
        self.seg_mgr.new_session()
        self.win_mgr.new_session()
        self.save_session(session_name)
        self.view.update_for_new_session(
            session_name, self.seg_data, self.ses_data, self.plyr
        )
        self.console.clear()

    def open_transcript(self, transcript_filename):
        self.ses_mgr.import_transcript(transcript_filename)
        self.seg_mgr.initialise_segment_data_from_transcript(self.ses_data.transcript)
        session_name = self.utils.get_session_name()
        normaliser = self.plyr.audio_info.peak_amplitude
        self.win_mgr.initialise_window_data(self.seg_data, normaliser)
        self.save_session(session_name)
        self.view.update_for_open_file(
            session_name,
            self.ses_data,
            self.seg_data,
            self.win_data,
            self.plyr,
        )

    def open_audiofile(self, audio_filename):
        session_name = self.utils.get_session_name()
        self.ses_data.audio_filename = audio_filename
        self.plyr.load_audio_file(audio_filename)
        self.save_session(self.utils.get_session_name())
        self.view.update_for_open_file(
            session_name,
            self.ses_data,
            self.seg_data,
            self.win_data,
            self.plyr,
        )

    def save_transcript(self, filename):
        self.utils.save_transcript_to_file(self.ses_data.transcript, filename)

    def save_rttm(self, filename):
        self.utils.save_transcript_as_rttm(self.ses_data.transcript, filename)

    def save_audio(self, filename):
        self.utils.save_audio(ply=self.plyr, filename=filename)

    # ======================================
    #              SEGMENTS
    # ======================================
    def change_segment_by_delta(self, delta):
        new_index = self.seg_data.curr_index + delta
        transcript = self.ses_data.transcript
        num_segments = len(transcript)
        session_name = self.utils.get_session_name()

        p, c, n = self.seg_mgr.update_indexes(new_index, num_segments)
        self.seg_mgr.update_segments_to_new_index(transcript, p, c, n)
        self.win_mgr.reset_window_to_match_segment(self.seg_data)
        self.win_mgr.set_prev_next_markers(curr_index=c, transcript=transcript)

        self.view.update_for_change_segment(self.seg_data, self.win_data, self.plyr)
        self.plyr.play_audio(self.win_data.start, self.win_data.end)

        self.console.log(self.seg_mgr.detect_overlap(transcript, curr_index=c))
        self.save_session(session_name)

    def go_to_segment(self, new_index):
        delta = new_index - self.seg_data.curr_index
        self.change_segment_by_delta(delta)

    def delete_segment(self):
        self.seg_mgr.delete_segment(self.ses_data, self.seg_data)
        self.change_segment_by_delta(delta=0)

    def edit_timestamps_using_markers(self):
        transcript = self.ses_data.transcript
        curr_index = self.seg_data.curr_index
        new_start = self.win_data.start_marker
        new_end = self.win_data.end_marker

        self.seg_mgr.edit_timestamps(transcript, curr_index, new_start, new_end)
        self.win_mgr.reset_window_to_match_segment(self.seg_data)

        self.save_session(self.utils.get_session_name())
        self.view.update_labels_for_save_timestamp_edits(self.seg_data)
        self.view.update_plot(self.win_data, self.plyr)
        self.console.log(self.seg_mgr.detect_overlap(transcript, curr_index))
        self.play_audio_window()
        self.utils.backup_save(
            self.ses_data,
            self.seg_data,
            self.win_data,
            self.utils.get_session_name(),
        )

    def trim_audio_and_transcript(self):
        transcript = self.ses_data.transcript
        trim_start = self.win_data.start_marker
        trim_end = self.win_data.end_marker

        trim_transcript = self.ses_mgr.trim_transcript(trim_start, trim_end, transcript)
        self.ses_data.transcript = trim_transcript
        p, c, n = self.seg_mgr.update_indexes(
            self.seg_data.curr_index, len(trim_transcript)
        )
        self.seg_mgr.update_segments_to_new_index(trim_transcript, p, c, n)
        self.plyr.trim_audio(trim_start, trim_end)

        self.view.update_for_change_segment(self.seg_data, self.win_data, self.plyr)
        self.view.update_labels_for_save_timestamp_edits(self.seg_data)

    def edit_transcript_label_or_language(self, language, text):
        self.seg_data.curr_segment.language = language
        self.seg_data.curr_segment.text = text
        self.ses_data.transcript[self.seg_data.curr_index][3] = language
        self.ses_data.transcript[self.seg_data.curr_index][4] = text
        self.save_session(self.utils.get_session_name())

    def duplicate_segment(self):
        index = self.seg_data.curr_index
        transcript = self.ses_data.transcript

        start, end, label, language, text = transcript[index]
        # slightly modify so segments dont have identical timestamps
        dup_segment = [start + 0.01, end + 0.01, label, language, text]
        tr = self.seg_mgr.insert_segment_at_index(transcript, dup_segment, index)
        self.change_segment_by_delta(delta=0)

    # ======================================
    #               AUDIO
    # ======================================
    def play_audio_window(self):
        start = self.win_data.start
        end = self.win_data.end
        self.plyr.play_audio(start, end)

    def play_skip_audio(self):
        skip_start = self.win_data.start_marker
        skip_end = self.win_data.end_marker
        start = self.win_data.start
        end = self.win_data.end
        self.plyr.play_audio(start, end, skip_start, skip_end)

    def play_segment(self):
        start = self.win_data.start_marker
        end = self.win_data.end_marker
        self.plyr.play_audio(start, end)

    def stop_audio(self):
        self.plyr.stop_audio()

    # ======================================
    #            PLOT WINDOW
    # ======================================
    def change_window_start(self, delta):
        new_start = self.win_data.start + delta
        new_start = max(0, min(new_start, self.win_data.start_marker))
        self.win_data.start = new_start
        self.view.update_plot(self.win_data, self.plyr)

    def change_window_end(self, delta):
        new_start = self.win_data.end + delta
        curr_end = self.win_data.end_marker
        new_start = max(curr_end, min(new_start, self.plyr.audio_info.duration))
        self.win_data.end = new_start
        self.view.update_plot(self.win_data, self.plyr)

    def change_marker(self, delta, is_start=True):
        duration = self.plyr.audio_info.duration
        curr_index = self.seg_data.curr_index
        transcript = self.ses_data.transcript

        if is_start:
            self.win_mgr.change_marker_by_delta(delta, duration, is_start=True)
            if self.win_data.start_marker < self.win_data.start:
                self.win_data.start = self.win_data.start_marker
        else:
            self.win_mgr.change_marker_by_delta(delta, duration, is_start=False)
            if self.win_data.end_marker > self.win_data.end:
                self.win_data.end = self.win_data.end_marker

        self.view.update_plot(self.win_data, self.plyr)
        self.console.log(self.seg_mgr.detect_overlap(transcript, curr_index))

    def zoom_plot(self, delta):
        zoom_min, zoom_max = 0.1, 2
        zoom_scaler = self.win_data.zoom_scaler + delta
        zoom_scaler = max(zoom_min, min(zoom_scaler + delta, zoom_max))
        self.win_data.zoom_scaler = zoom_scaler
        self.view.update_plot(self.win_data, self.plyr)

    # ======================================
    #                MISC
    # ======================================
    def data_dump(self):
        print(f"Index = {self.seg_data.curr_index}")
        if session_name := self.utils.get_session_name():
            session_name = os.path.basename(session_name)
            Debug.print_session_data(self.win_data, f"{session_name} window data:")
            Debug.print_session_data(self.seg_data, f"{session_name} segment data:")
            Debug.print_session_data(self.ses_data, f"{session_name} session data:")

    def save_session(self, session_name):
        self.utils.save_session(
            self.ses_data, self.seg_data, self.win_data, session_name
        )

    def run_test(self):
        self.seg_mgr.find_all_instances_of_overlap(transcript=self.ses_data.transcript)
