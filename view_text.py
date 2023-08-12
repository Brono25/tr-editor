import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from debug import Debug
import os


class TextFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10, padx=10)
        wrap_len = 700
        col = 0
        font_size = 20
        label_width = 60
        line_spacing = 10
        padding_label = tk.Label(self.frame, text="", width=20)
        padding_label.grid(row=0, column=0, rowspan=3)

        self.prev_text = tk.Label(
            self.frame,
            text=f"Prev Line 0: ",
            anchor="w",
            wraplength=wrap_len,
            justify="left",
            fg="grey",
            width=label_width,
            font=("Helvetica", font_size - 5),
        )
        self.prev_text.grid(row=0, column=col, sticky="w", pady=line_spacing)

        self.curr_text = tk.Label(
            self.frame,
            text=f"Curr Line 1: ",
            anchor="w",
            wraplength=wrap_len,
            justify="left",
            width=label_width,
            font=("Helvetica", font_size),
        )
        self.curr_text.grid(row=1, column=col, sticky="w", pady=line_spacing)

        self.next_text = tk.Label(
            self.frame,
            text=f"Next Line 3: ",
            anchor="w",
            wraplength=wrap_len,
            justify="left",
            fg="grey",
            width=label_width,
            font=("Helvetica", font_size - 5),
        )
        self.next_text.grid(row=2, column=col, sticky="w", pady=line_spacing)

    def update_text(self, segment_data):
        def get_line_text(segment, index):
            start, end, language, label, text = (
                (
                    segment.start,
                    segment.end,
                    segment.language,
                    segment.label,
                    segment.text,
                )
                if segment.text
                else (None, None, None, None, None)
            )

            if text:
                return f"Line {index}:  ({start:.2f},   {end:.2f}) : {label} : {language} : {text}"
            return "-"

        prev_text = get_line_text(segment_data.prev_segment, segment_data.prev_index)
        curr_text = get_line_text(segment_data.curr_segment, segment_data.curr_index)
        next_text = get_line_text(segment_data.next_segment, segment_data.next_index)

        self.prev_text.config(text=prev_text, fg="black")
        self.curr_text.config(
            text=curr_text, fg="darkred" if "!" in curr_text else "black"
        )
        self.next_text.config(text=next_text, fg="black")
