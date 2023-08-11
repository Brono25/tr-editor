import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from debug import Debug
import os


class View:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("TR-Editor")

        self.init_session_control_frame()
        self.init_segment_control_frame()
        self.init_text_frame()
        self.init_plot_frame()

    def init_session_control_frame(self):
        button_width = 10
        self.session_control_frame = tk.Frame(self.root)
        self.session_control_frame.pack(pady=10, padx=10)

        self.session_label_var = tk.StringVar()
        self.session_label = tk.Label(
            self.session_control_frame, textvariable=self.session_label_var
        )
        self.session_label.grid(row=0, column=0, columnspan=2)
        new_session_button = tk.Button(
            self.session_control_frame,
            text="New Session",
            command=self.new_session,
            width=button_width,
        )
        new_session_button.grid(row=1, column=0)
        open_session_button = tk.Button(
            self.session_control_frame,
            text="Open Session",
            command=self.open_session,
            width=button_width,
        )
        open_session_button.grid(row=1, column=1)

        self.open_transcript_button = tk.Button(
            self.session_control_frame,
            text="Open Transcript",
            command=self.open_transcript,
            state=tk.DISABLED,
            width=button_width,
        )
        self.open_transcript_button.grid(row=2, column=0)
        self.transcript_label_var = tk.StringVar()
        self.transcript_label = tk.Label(
            self.session_control_frame, textvariable=self.transcript_label_var
        )
        self.transcript_label.grid(row=2, column=1)
        self.open_audiofile_button = tk.Button(
            self.session_control_frame,
            text="Open WAV",
            command=self.open_audio_file,
            state=tk.DISABLED,
            width=button_width,
        )
        self.open_audiofile_button.grid(row=3, column=0)
        self.audiofile_label_var = tk.StringVar()
        self.audiofile_label = tk.Label(
            self.session_control_frame, textvariable=self.audiofile_label_var
        )
        self.audiofile_label.grid(row=3, column=1)
        data_dump_button = tk.Button(
            self.session_control_frame,
            text="Data Dump",
            command=self.controller.data_dump,
        )
        data_dump_button.grid(row=1, column=3)

    def init_segment_control_frame(self):
        self.segment_control_frame = tk.Frame(self.root)
        self.segment_control_frame.pack(pady=10, padx=10)

        # Row 0
        label_change_segment = tk.Label(
            self.segment_control_frame, text="Change Segment Index"
        )
        label_change_segment.grid(row=0, column=2, columnspan=3)

        # Row 1
        self.play_button = tk.Button(
            self.segment_control_frame, text="Play", command=None, state=tk.DISABLED
        )
        self.play_button.grid(row=1, column=0)

        self.stop_button = tk.Button(
            self.segment_control_frame, text="Stop", command=None, state=tk.DISABLED
        )
        self.stop_button.grid(row=1, column=1)

        self.left_arrow_button = tk.Button(
            self.segment_control_frame, text="\u2190", command=self.controller.decrement_index, state=tk.DISABLED
        )  # Left arrow
        self.left_arrow_button.grid(row=1, column=2)

        self.right_arrow_button = tk.Button(
            self.segment_control_frame,
            text="\u2192", # ->
            command=self.controller.increment_index,
            state=tk.DISABLED,
        )  
        self.right_arrow_button.grid(row=1, column=3)

        self.text_box_input = tk.Entry(
            self.segment_control_frame, width=5, state=tk.DISABLED
        )
        self.text_box_input.grid(row=1, column=4)

        self.line_count_label = tk.Label(self.segment_control_frame, text=" of (None)")
        self.line_count_label.grid(row=1, column=5)

        self.delete_segment_button = tk.Button(
            self.segment_control_frame, text="Delete", command=None, state=tk.DISABLED
        )
        self.delete_segment_button.grid(row=1, column=6)

    def init_text_frame(self):
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(pady=10, padx=10)
        wrap_len = 500
        col = 0
        font_size = 20

        padding_label = tk.Label(self.text_frame, text="", width=20)
        padding_label.grid(row=0, column=0, rowspan=3)

        self.prev_text = tk.Label(
            self.text_frame,
            text=f"Prev Line 0: ",
            anchor="w",
            wraplength=wrap_len,
            justify="left",
            fg="grey",
            font=("Helvetica", font_size - 4),
        )
        self.prev_text.grid(row=0, column=col, sticky="w")

        self.curr_text = tk.Label(
            self.text_frame,
            text=f"Curr Line 1: ",
            anchor="w",
            wraplength=wrap_len,
            justify="left",
            font=("Helvetica", font_size),
        )
        self.curr_text.grid(row=1, column=col, sticky="w")

        self.next_text = tk.Label(
            self.text_frame,
            text=f"Next Line 3: ",
            anchor="w",
            wraplength=wrap_len,
            justify="left",
            fg="grey",
            font=("Helvetica", font_size - 4),
        )
        self.next_text.grid(row=2, column=col, sticky="w")

    def init_plot_frame(self):
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot_fig, self.plot_ax = plt.subplots(figsize=(5, 3))
        self.plot_ax.tick_params(axis="both", which="major", labelsize=5)
        self.plot_canvas = FigureCanvasTkAgg(self.plot_fig, master=self.plot_frame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        plt.xlabel("Seconds", fontsize=6)

    def activate_open_buttons(self):
        self.open_audiofile_button["state"] = tk.NORMAL
        self.open_transcript_button["state"] = tk.NORMAL

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

    def update_line_count_label(self, new_text):
        self.new_label.config(text=new_text)

    def update_plot(self, x=None, y=None):
        self.plot_ax.clear()
        if x is not None and y is not None:
            self.plot_ax.plot(x, y)
        else:
            self.plot_ax.plot([])
        self.plot_canvas.draw()

    def update_session_label(self, session):
        if not session:
            session_label = "Active Session: None"
        else:
            session_name = os.path.basename(session)
            session_name_without_extension, _ = os.path.splitext(session_name)
            session_label = f"Active Session: {session_name_without_extension}"
        self.session_label_var.set(session_label)

    def update_transcript_label(self, transcript):
        if not transcript:
            transcript = "None"
        self.transcript_label_var.set(os.path.basename(transcript))

    def update_audiofile_label(self, audiofile):
        if not audiofile:
            audiofile = "None"
        self.audiofile_label_var.set(os.path.basename(audiofile))

    def update_text(self, segment_data):
        def get_line_text(segment, index):
            if segment.text:
                start, end, language, label, text = (
                    segment.start,
                    segment.end,
                    segment.language,
                    segment.label,
                    segment.text,
                )
                return f"Line {index}:  ({start:.2f},   {end:.2f}) : {label} : {language} : {text}"
            return "-"

        self.prev_text.config(
            text=f"{get_line_text(segment_data.prev_segment, segment_data.prev_index)}"
        )
        self.curr_text.config(
            text=f"{get_line_text(segment_data.curr_segment, segment_data.curr_index)}"
        )
        self.next_text.config(
            text=f"{get_line_text(segment_data.next_segment, segment_data.next_index)}"
        )

    def update_segment_control_buttons(self, session_data):
        if session_data.transcript:
            self.activate_segment_control_buttons()
        else:
            self.deactivate_segment_control_buttons()

    def new_session(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            defaultextension=".yml",
            filetypes=[("YAML files", "*.yml")],
        )
        if file_path:
            self.controller.new_session(file_path)

    def open_session(self):
        session_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yml")])
        if session_path:
            self.controller.open_session(session_path)

    def open_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.wav_file_entry.delete(0, tk.END)
            self.wav_file_entry.insert(0, file_path)
            self.session_open_audio_file(file_path)

    def open_transcript(self):
        transcript_filename = filedialog.askopenfilename(
            filetypes=[("Tr files", "*.tr")]
        )
        if transcript_filename:
            self.controller.open_transcript(transcript_filename)

    def run(self):
        self.root.mainloop()
