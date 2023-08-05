from subscriber import Subscriber

class AudioPlayer(Subscriber):
    def notify(self, message):
        print("Audio player received message:", message)
