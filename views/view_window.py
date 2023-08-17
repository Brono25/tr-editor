import tkinter as tk
import tkinter.messagebox as messagebox


class WindowControlFrame:
    def __init__(self, parent):
        container_frame = tk.Frame(parent.root)
        container_frame.pack(side=tk.TOP)  # Use pack
        self.frame = tk.Frame(container_frame)
        self.frame.pack()
        self.parent = parent

        self.init_window_ctrl_frame()
        self.init_start_timestamp_frame()
        self.init_end_timestamp_frame()
        self.init_zoom_and_save()

    def init_window_ctrl_frame(self):
        window_control_frame = tk.Frame(self.frame)
        window_control_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(window_control_frame, text="Window Control").pack()
        button_frame = tk.Frame(window_control_frame)
        button_frame.pack()

        func = lambda: self.parent.call_function("window_start_decrease")
        self.window_control_button1 = tk.Button(button_frame, text="<", command=func)
        self.window_control_button1.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("window_start_increase")
        self.window_control_button2 = tk.Button(button_frame, text=">", command=func)
        self.window_control_button2.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("window_end_decrease")
        self.window_control_button3 = tk.Button(button_frame, text="<", command=func)
        self.window_control_button3.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("window_end_increase")
        self.window_control_button4 = tk.Button(button_frame, text=">", command=func)
        self.window_control_button4.pack(side=tk.LEFT)

    def init_start_timestamp_frame(self):
        start_frame = tk.Frame(self.frame)
        start_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(start_frame, text="Start Timestamp").pack()
        start_button_frame = tk.Frame(start_frame)
        start_button_frame.pack()
        func = lambda: self.parent.call_function("decrease_start")
        self.start_button1 = tk.Button(start_button_frame, text="<<", command=func)
        self.start_button1.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("small_decrease_start")
        self.start_button2 = tk.Button(start_button_frame, text="<", command=func)
        self.start_button2.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("small_increase_start")
        self.start_button3 = tk.Button(start_button_frame, text=">", command=func)
        self.start_button3.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("increase_start")
        self.start_button4 = tk.Button(start_button_frame, text=">>", command=func)
        self.start_button4.pack(side=tk.LEFT)

    def init_end_timestamp_frame(self):
        end_frame = tk.Frame(self.frame)
        end_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(end_frame, text="End Timestamp").pack()
        end_button_frame = tk.Frame(end_frame)
        end_button_frame.pack()
        func = lambda: self.parent.call_function("decrease_end")
        self.end_button1 = tk.Button(end_button_frame, text="<<", command=func)
        self.end_button1.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("small_decrease_end")
        self.end_button2 = tk.Button(end_button_frame, text="<", command=func)
        self.end_button2.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("small_increase_end")
        self.end_button3 = tk.Button(end_button_frame, text=">", command=func)
        self.end_button3.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("increase_end")
        self.end_button4 = tk.Button(end_button_frame, text=">>", command=func)
        self.end_button4.pack(side=tk.LEFT)

    def init_zoom_and_save(self):
        zoom_frame = tk.Frame(self.frame)
        zoom_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(zoom_frame, text="Zoom").pack()
        zoom_button_frame = tk.Frame(zoom_frame)
        zoom_button_frame.pack()

        func = lambda: self.parent.call_function("zoom_out")
        self.zoom_out_button = tk.Button(zoom_button_frame, text="-", command=func)
        self.zoom_out_button.pack(side=tk.LEFT)

        func = lambda: self.parent.call_function("zoom_in")
        self.zoom_in_button = tk.Button(zoom_button_frame, text="+", command=func)
        self.zoom_in_button.pack(side=tk.LEFT)

        # Save edits button
        save_edits_frame = tk.Frame(self.frame)
        save_edits_frame.pack(side=tk.LEFT, padx=10)

        func = self.trim_audio
        self.new_button = tk.Button(save_edits_frame, text="\u2702", command=func)
        self.new_button.pack()

        func = lambda: self.parent.call_function("save_timestamp_edits")
        self.save_edits_button = tk.Button(
            save_edits_frame, text="\U0001F4BE", command=func
        )
        self.save_edits_button.pack()

    def activate_buttons(self):
        self.window_control_button1.config(state=tk.NORMAL)
        self.window_control_button2.config(state=tk.NORMAL)
        self.window_control_button3.config(state=tk.NORMAL)
        self.window_control_button4.config(state=tk.NORMAL)
        self.start_button1.config(state=tk.NORMAL)
        self.start_button2.config(state=tk.NORMAL)
        self.start_button3.config(state=tk.NORMAL)
        self.start_button4.config(state=tk.NORMAL)
        self.end_button1.config(state=tk.NORMAL)
        self.end_button2.config(state=tk.NORMAL)
        self.end_button3.config(state=tk.NORMAL)
        self.end_button4.config(state=tk.NORMAL)
        self.zoom_out_button.config(state=tk.NORMAL)
        self.zoom_in_button.config(state=tk.NORMAL)
        self.save_edits_button.config(state=tk.NORMAL)

    def deactivate_buttons(self):
        self.window_control_button1.config(state=tk.DISABLED)
        self.window_control_button2.config(state=tk.DISABLED)
        self.window_control_button3.config(state=tk.DISABLED)
        self.window_control_button4.config(state=tk.DISABLED)
        self.start_button1.config(state=tk.DISABLED)
        self.start_button2.config(state=tk.DISABLED)
        self.start_button3.config(state=tk.DISABLED)
        self.start_button4.config(state=tk.DISABLED)
        self.end_button1.config(state=tk.DISABLED)
        self.end_button2.config(state=tk.DISABLED)
        self.end_button3.config(state=tk.DISABLED)
        self.end_button4.config(state=tk.DISABLED)
        self.zoom_out_button.config(state=tk.DISABLED)
        self.zoom_in_button.config(state=tk.DISABLED)
        self.save_edits_button.config(state=tk.DISABLED)

    def trim_audio(self):
        response = messagebox.askyesno(
            "Trim Audio and Transcript",
            "Are you sure you want to trim the audio and transcript? This action is irreversible.",
        )
        if response:
            self.parent.call_function("trim")
