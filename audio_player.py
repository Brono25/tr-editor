from pydub import AudioSegment
import pyaudio
import threading
import os


class AudioPlayer:
    def __init__(self):
        self.audio_obj = None
        self.stop_flag = False
        self.play_thread = None

    def load_audio_file(self, path):
        try:
            audio_obj = AudioSegment.from_file(path)
            print(f"{os.path.basename(path)} successfully loaded")
            return audio_obj
        except Exception as e:
            print(f"An error occurred while loading the audio file: {e}")
            return None

    def play_audio(self, start, end):
        start = start * 1000  # ms
        end = end * 1000
        if not self.audio_obj:
            print("Error: No audio loaded.")
            return

        sliced_audio = self.audio_obj[start:end]

        if (
            hasattr(self, "play_thread")
            and self.play_thread
            and self.play_thread.is_alive()
        ):
            self.stop_audio()

        self.stop_flag = False
        self.play_thread = threading.Thread(
            target=self._play_audio_in_thread, args=(sliced_audio,)
        )
        self.play_thread.start()

    def _play_audio_in_thread(self, sliced_audio):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(sliced_audio.sample_width),
            channels=sliced_audio.channels,
            rate=sliced_audio.frame_rate,
            output=True,
        )

        chunk_size = 1024
        for i in range(0, len(sliced_audio.raw_data), chunk_size):
            if self.stop_flag:
                break
            stream.write(sliced_audio.raw_data[i : i + chunk_size])
        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop_audio(self):
        self.stop_flag = True
        if self.play_thread:
            self.play_thread.join()
            self.play_thread = None
