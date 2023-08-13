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
import matplotlib

INCREMENT = 0.1
SMALL_INCREMENT = 25 / 1000


class WindowControlFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        small_button_width = 1

        def create_buttons(frame, decrease_command, small_decrease_command, increase_command, small_increase_command):
            tk.Button(frame, text="<<", command=small_decrease_command, width=small_button_width).pack(side=tk.LEFT)
            tk.Button(frame, text="<", command=decrease_command, width=small_button_width).pack(side=tk.LEFT)
            tk.Button(frame, text=">", command=increase_command).pack(side=tk.LEFT)
            tk.Button(frame, text=">>", command=small_increase_command).pack(side=tk.LEFT)

        start_frame = tk.Frame(self)
        start_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(start_frame, text="Start Timestamp").pack()
        create_buttons(start_frame, self.decrease_start, self.small_decrease_start, self.increase_start, self.small_increase_start)

        end_frame = tk.Frame(self)
        end_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(end_frame, text="End Timestamp").pack()
        create_buttons(end_frame, self.decrease_end, self.small_decrease_end, self.increase_end, self.small_increase_end)

        zoom_frame = tk.Frame(self)
        zoom_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(zoom_frame, text="Zoom").pack()
        self.zoom_out_button = tk.Button(zoom_frame, text="-", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT)
        self.zoom_in_button = tk.Button(zoom_frame, text="+", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT)

        # Save edits button
        self.save_edits_button = tk.Button(self, text="save edits", command=self.controller.save_timestamp_edits)
        self.save_edits_button.pack(side=tk.LEFT)

        self.pack(side=tk.TOP)




    def decrease_start(self):
        self.controller.change_start_timestamp(INCREMENT * (-1))

    def small_decrease_start(self):
        self.controller.change_start_timestamp(SMALL_INCREMENT * (-1))

    def increase_start(self):
        self.controller.change_start_timestamp(INCREMENT)

    def small_increase_start(self):
        self.controller.change_start_timestamp(SMALL_INCREMENT)

    def decrease_end(self):
        self.controller.change_end_timestamp(INCREMENT * (-1))

    def small_decrease_end(self):
        self.controller.change_end_timestamp(SMALL_INCREMENT * (-1))

    def increase_end(self):
        self.controller.change_end_timestamp(INCREMENT)

    def small_increase_end(self):
        self.controller.change_end_timestamp(SMALL_INCREMENT)

    def zoom_in(self):
        print("Zoom in clicked!")

    def zoom_out(self):
        print("Zoom out clicked!")
