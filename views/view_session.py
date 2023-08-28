import tkinter as tk
from tkinter import filedialog
import os

SAVE_SYMBOL = "\U0001F4BE"
OPEN_SYMBOL = "\U0001F4C1"
NEW_SYMBOL = "\U0001F4C4"
DEBUG_SYMBOL = "\u26C1"


class SessionControlFrame:
    def __init__(self, parent, button_width=8):
        self.parent = parent
        self.frame = tk.Frame(parent.root)
        self.frame.pack(pady=10, padx=10)
        self.current_session_dir = os.getcwd()

        self.session_label_var = tk.StringVar()
        self.session_label = tk.Label(self.frame, textvariable=self.session_label_var)
        self.session_label.grid(row=0, column=0, columnspan=2)
        new_session_button = tk.Button(
            self.frame,
            text=f"{NEW_SYMBOL} Session",
            command=self.new_session,
            width=button_width,
        )
        new_session_button.grid(row=1, column=0)
        open_session_button = tk.Button(
            self.frame,
            text=f"{OPEN_SYMBOL} Session",
            command=self.open_session,
            width=button_width,
        )
        open_session_button.grid(row=1, column=1)

        self.open_transcript_button = tk.Button(
            self.frame,
            text=f"{OPEN_SYMBOL} Transcript",
            command=self.open_transcript,
            state=tk.DISABLED,
            width=button_width,
        )
        self.open_transcript_button.grid(row=2, column=0)
        self.transcript_label_var = tk.StringVar()
        self.transcript_label = tk.Label(
            self.frame, textvariable=self.transcript_label_var
        )
        self.transcript_label.grid(row=2, column=1)
        self.open_audiofile_button = tk.Button(
            self.frame,
            text=f"{OPEN_SYMBOL} Audio",
            command=self.open_audio_file,
            state=tk.DISABLED,
            width=button_width,
        )
        self.open_audiofile_button.grid(row=3, column=0)
        
        self.audiofile_label_var = tk.StringVar()
        self.audiofile_label = tk.Label(
            self.frame, textvariable=self.audiofile_label_var
        )
        self.audiofile_label.grid(row=3, column=1)


        self.save_tr_button = tk.Button(
            self.frame,
            text=f"{SAVE_SYMBOL} .tr",
            command=self.save_transcript,
        )
        self.save_tr_button.grid(row=1, column=3)

        self.audiofile_label.grid(row=3, column=1)

        self.save_rttm_button = tk.Button(
            self.frame,
            text=f"{SAVE_SYMBOL} .rttm",
            command=self.save_rttm,
        )
        self.save_rttm_button.grid(row=1, column=4)

        self.save_audio_button = tk.Button(
            self.frame,
            text=f"{SAVE_SYMBOL} .wav",
            command=self.save_audio,
        )
        self.save_audio_button.grid(row=1, column=5)


        data_dump_button = tk.Button(
            self.frame,
            text=DEBUG_SYMBOL,
            command=lambda: self.parent.call_function("data_dump"),
        )
        data_dump_button.grid(row=1, column=6)

    def new_session(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=self.current_session_dir,
            defaultextension=".yml",
            filetypes=[("YAML files", "*.yml")],
        )
        if file_path:
            self.current_session_dir = os.path.dirname(file_path)
            self.parent.call_function("new_session", file_path)

    def open_session(self):
        session_path = filedialog.askopenfilename(
            initialdir=self.current_session_dir,
            filetypes=[("YAML files", "*.yml")],
        )
        if session_path:
            self.current_session_dir = os.path.dirname(session_path)
            self.parent.call_function("open_session", session_path)



    def open_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.audiofile_label_var.set(os.path.basename(file_path))
            self.parent.call_function("open_audio_file", file_path)

    def open_transcript(self):
        transcript_filename = filedialog.askopenfilename(
            filetypes=[("Tr files", "*.tr")]
        )
        if transcript_filename:
            self.parent.call_function("open_transcript", transcript_filename)
            
    def save_audio(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=self.current_session_dir,
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
        )
        if file_path:
            self.parent.call_function("save_audio", file_path)
            self.parent.console.log(f"Saved {file_path}")

    def save_transcript(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=self.current_session_dir,
            defaultextension=".tr",
            filetypes=[("Transcript files", "*.tr")],
        )
        if file_path:
            self.parent.call_function("save_tr", file_path)
            self.parent.console.log(f"Saved {file_path}")


    def save_rttm(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=self.current_session_dir,
            defaultextension=".rttm",
            filetypes=[("RTTM files", "*.rttm")],
        )
        if file_path:
            self.parent.call_function("save_rttm", file_path)


    def update_session_label(self, session):
        if not session:
            session_label = "Active Session: None"
        else:
            session_name = os.path.basename(session)
            session_name_without_extension, _ = os.path.splitext(session_name)
            session_label = f"Active Session: {session_name_without_extension}"
        self.session_label_var.set(session_label)

    def update_transcript_label(self, transcript_filename):
        if not transcript_filename:
            transcript_filename = "None"
        self.transcript_label_var.set(os.path.basename(transcript_filename))

    def update_audiofile_label(self, audiofile):
        if not audiofile:
            audiofile = "None"
        self.audiofile_label_var.set(os.path.basename(audiofile))

    def activate_open_buttons(self):
        self.open_audiofile_button["state"] = tk.NORMAL
        self.open_transcript_button["state"] = tk.NORMAL


