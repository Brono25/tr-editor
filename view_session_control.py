import tkinter as tk
from tkinter import filedialog
import os

class SessionControlFrame:
    def __init__(self, parent, controller, button_width=10):
        self.controller = controller
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10, padx=10)
        
        self.session_label_var = tk.StringVar()
        self.session_label = tk.Label(self.frame, textvariable=self.session_label_var)
        self.session_label.grid(row=0, column=0, columnspan=2)
        new_session_button = tk.Button(
            self.frame,
            text="New Session",
            command=self.new_session,
            width=button_width,
        )
        new_session_button.grid(row=1, column=0)
        open_session_button = tk.Button(
            self.frame,
            text="Open Session",
            command=self.open_session,
            width=button_width,
        )
        open_session_button.grid(row=1, column=1)

        self.open_transcript_button = tk.Button(
            self.frame,
            text="Open Transcript",
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
            text="Open Audio",
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
        data_dump_button = tk.Button(
            self.frame,
            text="Print Data",
            command=self.controller.data_dump,
        )
        data_dump_button.grid(row=1, column=3)

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

    def activate_open_buttons(self):
        self.open_audiofile_button["state"] = tk.NORMAL
        self.open_transcript_button["state"] = tk.NORMAL