import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from debug import Debug
import os
from view_session_control import SessionControlFrame
from view_segment_control import SegmentControlFrame
from view_plot import PlotFrame
from view_text import TextFrame

class View:
    def __init__(self, controller):
        self.root = tk.Tk()
        self.session_control_frame = SessionControlFrame(self.root, controller)
        self.segment_control_frame = SegmentControlFrame(self.root, controller)
        self.text_frame = TextFrame(self.root)  
        self.plot_frame = PlotFrame(self.root)


    def run(self):
        self.root.mainloop()
