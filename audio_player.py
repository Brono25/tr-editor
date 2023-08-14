from pydub import AudioSegment
import pyaudio
import threading
import os
import numpy as np


PRE_SILENCE = AudioSegment.silent(duration=50)
POST_SILENCE = AudioSegment.silent(duration=1000)


class AudioInfo:
    def __init__(self):
        self.peak_amplitude = None
        self.duration = None
        self.sample_rate = None


class AudioPlayer:
    def __init__(self):
        self.audio_obj = None
        self.audio_info = AudioInfo()
        self._stop_flag = False
        self._play_thread = None

    def load_audio_file(self, path):
        try:
            self.audio_obj = AudioSegment.from_file(path)
            samples = np.array(self.audio_obj.get_array_of_samples())
            self.audio_info.peak_amplitude = np.max(np.abs(samples))
            self.audio_info.duration = self.audio_obj.duration_seconds
            self.audio_info.sample_rate = self.audio_obj.frame_rate
            print(f"{os.path.basename(path)} successfully loaded")
        except Exception as e:
            print(f"An error occurred while loading the audio file: {e}")
            return None

    def play_audio(self, start, end):
        self.stop_audio()
        start_ms = start * 1000
        end_ms = end * 1000

        if not self.audio_obj:
            print("Error: No audio loaded.")
            return

        sliced_audio = self.audio_obj[start_ms:end_ms]

        sliced_audio = PRE_SILENCE + sliced_audio + POST_SILENCE

        if (
            hasattr(self, "play_thread")
            and self._play_thread
            and self._play_thread.is_alive()
        ):
            self.stop_audio()

        self._stop_flag = False
        self._play_thread = threading.Thread(
            target=self._play_audio_in_thread, args=(sliced_audio,)
        )
        self._play_thread.start()

    def _play_audio_in_thread(self, sliced_audio):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(sliced_audio.sample_width),
            channels=sliced_audio.channels,
            rate=sliced_audio.frame_rate,
            output=True,
        )

        chunk_size = 1024

        raw_data = sliced_audio.raw_data
        for i in range(0, len(raw_data), chunk_size):
            if self._stop_flag:
                break
            chunk_end = min(i + chunk_size, len(raw_data))

            stream.write(raw_data[i:chunk_end])

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop_audio(self):
        self._stop_flag = True
        if self._play_thread:
            self._play_thread.join()
            self._play_thread = None

    def get_audio_time_vectors(self, start, end):
        start_ms = start * 1000
        end_ms = end * 1000
        audio_slice = self.audio_obj[start_ms:end_ms]
        samples = np.array(audio_slice.get_array_of_samples())
        time_vector = np.arange(len(samples)) / audio_slice.frame_rate
        return samples / self.audio_info.peak_amplitude, time_vector
