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
        self.ops_frame = tk.Frame(self.root)
        self.ops_frame.pack(pady=10, padx=10)

        self.file_entry = tk.Entry(self.ops_frame, width=50)
        self.file_entry.pack(pady=10)

        # Entry for WAV file
        self.wav_file_entry = tk.Entry(self.ops_frame, width=50)  
        self.wav_file_entry.pack(pady=10)

        new_session_button = tk.Button(self.ops_frame, text="New Session", command=self.new_session)
        new_session_button.pack(pady=5)

        # Button to open WAV file
        open_wav_button = tk.Button(self.ops_frame, text="Open WAV", command=self.open_audio_file)
        open_wav_button.pack(pady=5)
        
        open_session_button = tk.Button(self.ops_frame, text="Open Session", command=self.open_session)
        open_session_button.pack(pady=5, side=tk.LEFT) 
        
        # Add session label next to the open session button
        self.session_label_var = tk.StringVar()  # Create a StringVar to hold the label text
        self.session_label = tk.Label(self.ops_frame, textvariable=self.session_label_var)
        self.session_label.pack(pady=5, side=tk.LEFT)  # Pack label to position it to the right of the button
        

        # Button to open transcript
        open_transcript_button = tk.Button(self.ops_frame, text="Open Transcript", command=None)
        open_transcript_button.pack(pady=5)

    def init_other_elements(self):
        # Button to play audio
        play_audio_button = tk.Button(self.root, text="Play", command=None)
        play_audio_button.pack(pady=5)

        # Button for Data Dump
        data_dump_button = tk.Button(self.root, text="Data Dump", command=self.manager.data_dump)
        data_dump_button.pack(pady=5)

    def update_session_label(self, new_text):
        self.session_label_var.set(new_text)

    def new_session(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            defaultextension=".yml",
            filetypes=[("YAML files", "*.yml")],
        )
        if file_path:
            self.manager.new_session(file_path) 

    def open_session(self):
            file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yml")])
            
            if file_path:
                try:
                    self.manager.open_session(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open session: {str(e)}")
                    self.session_label_var.set("Failed to open session!")  

    def open_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.wav_file_entry.delete(0, tk.END)
            self.wav_file_entry.insert(0, file_path)
            self.session_open_audio_file(file_path)

    def open_transcript(self):
        file_path = filedialog.askopenfilename(filetypes=[("Tr files", "*.tr")])
        if file_path:
            try:
                self.session_open_transcript(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open transcript: {str(e)}")


    def run(self):
        self.root.mainloop()
