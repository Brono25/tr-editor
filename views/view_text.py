import tkinter as tk
import re


class TextFrame:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent.root)
        self.frame.pack(pady=10, padx=10)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.transcript_text = tk.Text(
            self.frame,
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set,
            height=5,
            spacing1=10,
        )
        self.transcript_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.scrollbar.config(command=self.transcript_text.yview)

        # Save button to trigger the save function
        self.save_button = tk.Button(
            self.frame, text="Save", command=self.process_edits
        )
        self.save_button.pack()

    def update_text(self, segment_data):
        def get_line_text(segment, index):
            start, end, language, label, text = (
                (
                    segment.start,
                    segment.end,
                    segment.language,
                    segment.label,
                    segment.text,
                )
                if segment.text
                else (None, None, None, None, None)
            )

            if text:
                return f"Line {index}:  ({start:.3f},   {end:.3f}) : {label} : {language} : {text}"
            return "-"

        prev_text = get_line_text(segment_data.prev_segment, segment_data.prev_index)
        curr_text = get_line_text(segment_data.curr_segment, segment_data.curr_index)
        next_text = get_line_text(segment_data.next_segment, segment_data.next_index)

        self.transcript_text.delete(1.0, tk.END)

        self.transcript_text.insert(tk.END, prev_text + "\n", "non_current_line")
        self.transcript_text.insert(tk.END, curr_text + "\n", "current_line")
        self.transcript_text.insert(tk.END, next_text + "\n", "non_current_line")
        self.transcript_text.tag_config(
            "current_line",
            foreground="darkred" if "!" in curr_text else "black",
            font=("Helvetica", 22),
        )
        self.transcript_text.tag_config(
            "non_current_line", foreground="lightgrey", font=("Helvetica", 16)
        )

        self.transcript_text.config(font=("Helvetica", 18))

    def process_edits(self):
        edited_text = self.transcript_text.get(1.0, tk.END)
        lines = edited_text.split("\n")
        lines = [x for x in lines if x != ""]

        pattern = re.compile(
            r"Line\s+\d+:\s+\((-?\d+\.\d{3}),\s*(-?\d+\.\d{3})\)\s+:\s+[A-Z]{3}\s+:\s+(SPA|ENG|NA)\s+:\s+.*|^\s*-\s*$"
        )

        if len(lines) != 3:
            return

        for line in lines:
            if not pattern.match(line):
                self.parent.console.log("Invalid transcript edits")
                return

        _, _, _, language, text = lines[1].split(":")
        language = language.strip()
        text = text.strip()
        self.parent.call_function("transcript_edits", language, text)

