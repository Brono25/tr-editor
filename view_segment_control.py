import tkinter as tk
from tkinter import messagebox


class SegmentControlFrame:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10, padx=10)

        label_change_segment = tk.Label(self.frame, text="Change Segment Index")
        label_change_segment.grid(row=0, column=2, columnspan=3)

        self.play_button = tk.Button(
            self.frame, text="Play", command=self.play_segment, state=tk.DISABLED
        )
        self.play_button.grid(row=1, column=0)

        self.stop_button = tk.Button(
            self.frame, text="Stop", command=self.stop_segment, state=tk.DISABLED
        )
        self.stop_button.grid(row=1, column=1)

        self.left_arrow_button = tk.Button(
            self.frame,
            text="\u2190",
            command=self.controller.decrement_index,
            state=tk.DISABLED,
        )
        self.left_arrow_button.grid(row=1, column=2)

        self.right_arrow_button = tk.Button(
            self.frame,
            text="\u2192",
            command=self.controller.increment_index,
            state=tk.DISABLED,
        )
        self.right_arrow_button.grid(row=1, column=3)

        self.text_box_input = tk.Entry(self.frame, width=5, state=tk.DISABLED)
        self.text_box_input.grid(row=1, column=4)
        self.text_box_input.bind("<Return>", self.text_box_input_process)

        self.line_count_label = tk.Label(self.frame, text=" of (None)")
        self.line_count_label.grid(row=1, column=5)

        self.delete_segment_button = tk.Button(
            self.frame, text="Delete", command=self.confirm_delete, state=tk.DISABLED
        )
        self.delete_segment_button.grid(row=1, column=6)

    def play_segment(self):
        print("Play")

    def stop_segment(self):
        print("Stop")

    def confirm_delete(self):
        result = messagebox.askyesno(
            "Confirmation", "Are you sure you want to delete the current segment?"
        )
        if result:
            self.controller.delete_segment()

    def update_segment_control_buttons(self, num_segments):
        if num_segments:
            self.activate_segment_control_buttons()
        else:
            self.deactivate_segment_control_buttons()

    def activate_segment_control_buttons(self):
        self.left_arrow_button["state"] = tk.NORMAL
        self.right_arrow_button["state"] = tk.NORMAL
        self.text_box_input["state"] = tk.NORMAL
        self.delete_segment_button["state"] = tk.NORMAL

    def deactivate_segment_control_buttons(self):
        self.left_arrow_button["state"] = tk.DISABLED
        self.right_arrow_button["state"] = tk.DISABLED
        self.text_box_input["state"] = tk.DISABLED
        self.delete_segment_button["state"] = tk.DISABLED

    def activate_play_stop_buttons(self):
        self.play_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.NORMAL

    def deactivate_play_stop_buttons(self):
        self.play_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.DISABLED

    def update_line_count_label(self, count):
        if count - 1 >= 0:
            self.line_count_label.config(text=f" of {count - 1}")
        else:
            self.line_count_label.config(text=f" of (None)")


    def update_text_input(self, new_text=""):
        original_state = self.text_box_input.cget("state")
        self.text_box_input.config(state=tk.NORMAL)
        self.text_box_input.delete(0, tk.END)
        self.text_box_input.insert(0, str(new_text))
        self.text_box_input.config(state=original_state)

    def text_box_input_process(self, event):
        input_text = self.text_box_input.get()
        try:
            self.controller.change_segment_input_box(int(input_text))
        except ValueError:
            pass
