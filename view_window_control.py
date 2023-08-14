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

DELTA = 250 / 1000
SMALL_DELTA = 25 / 1000

class WindowControlFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent.root)
        self.parent = parent

        small_button_width = 1

        def create_buttons(
            frame,
            decrease_command,
            small_decrease_command,
            increase_command,
            small_increase_command,
        ):
            tk.Button(
                frame,
                text="<<",
                command=lambda: parent.call_function(decrease_command),
                width=small_button_width,
            ).pack(side=tk.LEFT)
            tk.Button(
                frame,
                text="<",
                command=lambda: parent.call_function(small_decrease_command),
                width=small_button_width,
            ).pack(side=tk.LEFT)
            tk.Button(
                frame,
                text=">",
                command=lambda: parent.call_function(small_increase_command),
            ).pack(side=tk.LEFT)
            tk.Button(
                frame,
                text=">>",
                command=lambda: parent.call_function(increase_command),
            ).pack(side=tk.LEFT)

        start_frame = tk.Frame(self.frame)
        start_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(start_frame, text="Start Timestamp").pack()
        create_buttons(
            start_frame,
            "decrease_start",
            "small_decrease_start",
            "increase_start",
            "small_increase_start",
        )

        end_frame = tk.Frame(self.frame)
        end_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(end_frame, text="End Timestamp").pack()
        create_buttons(
            end_frame,
            "decrease_end",
            "small_decrease_end",
            "increase_end",
            "small_increase_end",
        )

        zoom_frame = tk.Frame(self.frame)
        zoom_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(zoom_frame, text="Zoom").pack()
        self.zoom_out_button = tk.Button(
            zoom_frame, text="-", command=lambda: parent.call_function("zoom_out")
        )
        self.zoom_out_button.pack(side=tk.LEFT)
        self.zoom_in_button = tk.Button(
            zoom_frame, text="+", command=lambda: parent.call_function("zoom_in")
        )
        self.zoom_in_button.pack(side=tk.LEFT)

        # Save edits button
        self.save_edits_button = tk.Button(
            self.frame,
            text="save edits",
            command=lambda: parent.call_function("save_timestamp_edits"),
        )
        self.save_edits_button.pack(side=tk.LEFT)

        self.frame.pack(side=tk.TOP)
