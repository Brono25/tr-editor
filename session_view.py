import tkinter as tk
from tkinter import filedialog, messagebox
import os

class SessionView:
    def __init__(self, manager):
        self.manager = manager  
        self.root = tk.Tk()
        self.root.title("TR-Editor")
        
        self.init_ops_frame()
        self.init_other_elements()


    def init_ops_frame(self):
        button_width = 10
        self.ops_frame = tk.Frame(self.root)
        self.ops_frame.pack(pady=10, padx=10)

        self.session_label_var = tk.StringVar() 
        self.session_label = tk.Label(self.ops_frame, textvariable=self.session_label_var)
        self.session_label.grid(row=0, column=0, columnspan=2)  # Centre top: session label

        new_session_button = tk.Button(self.ops_frame, text="New Session", command=self.new_session, width=button_width)
        new_session_button.grid(row=1, column=0)  # Middle left: [New Session]
        open_session_button = tk.Button(self.ops_frame, text="Open Session", command=self.open_session, width=button_width)
        open_session_button.grid(row=1, column=1)  # Middle left: [Open Session]
            
        self.open_transcript_button = tk.Button(self.ops_frame, text="Open Transcript", command=self.open_transcript, state=tk.DISABLED,width=button_width)
        self.open_transcript_button.grid(row=2, column=0)  # Lower middle left: [Open Transcript]
        self.transcript_label_var = tk.StringVar() 
        self.transcript_label = tk.Label(self.ops_frame, textvariable=self.transcript_label_var)
        self.transcript_label.grid(row=2, column=1)  # Lower middle left: "transcript label"

        self.open_audiofile_button = tk.Button(self.ops_frame, text="Open WAV", command=self.open_audio_file, state=tk.DISABLED, width=button_width)
        self.open_audiofile_button.grid(row=3, column=0)  # Bottom left: [Open Audiofile]
        self.audiofile_label_var = tk.StringVar() 
        self.audiofile_label = tk.Label(self.ops_frame, textvariable=self.audiofile_label_var)
        self.audiofile_label.grid(row=3, column=1)  # Bottom left: "audiofile label"



    def activate_open_buttons(self):
        self.open_audiofile_button['state'] = tk.NORMAL
        self.open_transcript_button['state'] = tk.NORMAL



    def init_other_elements(self):
        # Button to play audio
        play_audio_button = tk.Button(self.root, text="Play", command=None)
        play_audio_button.pack(pady=5)

        # Button for Data Dump
        data_dump_button = tk.Button(self.root, text="Data Dump", command=self.manager.data_dump)
        data_dump_button.pack(pady=5)

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
            transcript = 'None'
        self.transcript_label_var.set(os.path.basename(transcript))
            

    def update_audiofile_label(self, audiofile):
        if not audiofile:
            audiofile = 'None'
        self.audiofile_label_var.set(os.path.basename(audiofile))



    def new_session(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            defaultextension=".yml",
            filetypes=[("YAML files", "*.yml")],
        )
        if file_path:
            self.manager.new_session(file_path) 

    def open_session(self):
            session_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yml")])
            self.manager.open_session(session_path)
            


    def open_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.wav_file_entry.delete(0, tk.END)
            self.wav_file_entry.insert(0, file_path)
            self.session_open_audio_file(file_path)

    def open_transcript(self):
        transcript_filename = filedialog.askopenfilename(filetypes=[("Tr files", "*.tr")])
        self.manager.open_transcript(transcript_filename)


    def run(self):
        self.root.mainloop()
