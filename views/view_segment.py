import tkinter as tk


PLAY_SYMBOL = "\u25B6"
STOP_SYMBOL = "\u25A0"
LEFT_ARROW = "\u2190"
RIGHT_ARROW = "\u2192"


class SegmentControlFrame:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent.root)
        self.frame.pack(pady=10, padx=10)

        command = lambda: self.parent.call_function("play_audio")
        self.play_button = self.create_button(PLAY_SYMBOL, 1, 0, command)
        command = lambda: self.parent.call_function("skip_play")
        self.skip_play = self.create_button(
            f"{PLAY_SYMBOL}||{PLAY_SYMBOL}", 1, 2, command
        )
        command = lambda: self.parent.call_function("play_segment")
        self.play_segment = self.create_button(f"|{PLAY_SYMBOL}|", 1, 1, command)
        command = lambda: self.parent.call_function("stop_audio")
        self.stop_button = self.create_button(STOP_SYMBOL, 1, 3, command)

        command = lambda: self.parent.call_function("decrement_index")
        self.left_arrow_button = self.create_button(LEFT_ARROW, 1, 4, command)
        command = lambda: self.parent.call_function("increment_index")
        self.right_arrow_button = self.create_button(RIGHT_ARROW, 1, 5, command)

        self.create_label("Change Segment Index", row=0, column=4, columnspan=3)
        self.text_box_input = tk.Entry(self.frame, width=5, state=tk.DISABLED)
        self.text_box_input.grid(row=1, column=6)
        self.text_box_input.bind("<Return>", self.text_box_input_process)

        self.line_count_label = tk.Label(self.frame, text=" of (None)")
        self.line_count_label.grid(row=1, column=7)

    def create_button(self, text, row, column, command=None, state=tk.DISABLED):
        button = tk.Button(self.frame, text=text, command=command, state=state)
        button.grid(row=row, column=column)
        return button

    def create_label(self, text, row, column, columnspan=1):
        label = tk.Label(self.frame, text=text)
        label.grid(row=row, column=column, columnspan=columnspan)

    def update_segment_control_buttons(self, num_segments):
        if num_segments:
            self.activate_segment_control_buttons()
        else:
            self.deactivate_segment_control_buttons()

    def activate_segment_control_buttons(self):
        self.left_arrow_button["state"] = tk.NORMAL
        self.right_arrow_button["state"] = tk.NORMAL
        self.text_box_input["state"] = tk.NORMAL
        self.play_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.NORMAL
        self.skip_play["state"] = tk.NORMAL
        self.play_segment["state"] = tk.NORMAL

    def deactivate_segment_control_buttons(self):
        self.left_arrow_button["state"] = tk.DISABLED
        self.right_arrow_button["state"] = tk.DISABLED
        self.text_box_input["state"] = tk.DISABLED
        self.play_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.DISABLED
        self.skip_play["state"] = tk.DISABLED
        self.play_segment["state"] = tk.DISABLED

    def set_total_num_segments_label(self, count):
        if count - 1 >= 0:
            self.line_count_label.config(text=f" of {count - 1}")
        else:
            self.line_count_label.config(text=f" of (None)")

    def set_input_text_box_label(self, new_text=""):
        original_state = self.text_box_input.cget("state")
        self.text_box_input.config(state=tk.NORMAL)
        self.text_box_input.delete(0, tk.END)
        self.text_box_input.insert(0, str(new_text))
        self.text_box_input.config(state=original_state)

    def text_box_input_process(self, event):
        input_text = self.text_box_input.get()
        try:
            new_index = int(input_text)
            self.parent.call_function("change_seg_input", new_index)
        except ValueError:
            pass
