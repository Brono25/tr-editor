import tkinter as tk

class ConsoleFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent.root)
        self.frame.pack(expand=tk.YES, fill=tk.BOTH)
        
        self.header_label = tk.Label(self.frame, text="Console Log:", anchor=tk.W) 
        self.header_label.pack(fill=tk.X) 
        
        self.log_text = tk.Text(self.frame, wrap=tk.WORD, height=5)
        self.log_text.pack(expand=tk.YES, fill=tk.BOTH)
        
        self.scrollbar = tk.Scrollbar(self.frame, command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text['yscrollcommand'] = self.scrollbar.set

    def log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)  

    def clear(self):
        self.log_text.delete(1.0, tk.END)
