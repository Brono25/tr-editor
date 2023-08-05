from gui import GUI
from audio_player import AudioPlayer

gui = GUI()
player = AudioPlayer()

gui.register(player)

gui.run()
