import tkinter as tk
import os 

class Console:
    def __init__(self, parent):
        self.parent = parent
        self.session_dir = None
        self.frame = tk.Frame(parent.root)
        self.frame.pack(expand=tk.YES, fill=tk.BOTH)

        self.header_frame = tk.Frame(self.frame)
        self.header_frame.pack(fill=tk.X)

        self.button = tk.Button(self.header_frame, text="Run Test", command=self.on_button_click)
        self.button.pack(side=tk.LEFT)

        self.header_label = tk.Label(self.header_frame, text="Console Log:", anchor=tk.W)
        self.header_label.pack(side=tk.LEFT, fill=tk.X)

        self.log_text = tk.Text(self.frame, wrap=tk.WORD, height=5)
        self.log_text.pack(expand=tk.YES, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame, command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text["yscrollcommand"] = self.scrollbar.set


    def log(self, message):
        self.clear()
        if message:
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            print(message)

    def clear(self):
        self.log_text.delete(1.0, tk.END)

    def on_button_click(self):
        self.parent.call_function("run_test")

    def audio_trim_log(self, start, end):
        if not self.session_dir:
            print("No session directory set")
            return
        session_dir = os.path.dirname(self.session_dir)
        log_file_path = os.path.join(session_dir, "audio_trim_log")
        log_entry = f"{start},{end}"
        with open(log_file_path, 'a') as f:
            f.write(log_entry + '\n')


    def set_session_dir(self, session_dir):
        self.session_dir = session_dir