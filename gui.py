import tkinter as tk
from publisher import Publisher

class GUI(Publisher):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.button = tk.Button(self.root, text="Play Audio", command=self.button_pressed)
        self.button.pack()

    def run(self):
        self.root.mainloop()

    def button_pressed(self):
        print("Audio player called")
        self.dispatch("Play Audio")
