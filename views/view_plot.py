import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class PlotFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.plot_fig, self.plot_ax = plt.subplots(figsize=(5, 3))
        self.plot_ax.tick_params(axis="both", which="major", labelsize=5)
        self.plot_canvas = FigureCanvasTkAgg(self.plot_fig, master=self.frame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        plt.xlabel("Seconds", fontsize=6)


    def plot_audio(self, x=None, y=None):
        self.plot_ax.clear()
        if x is not None and y is not None and len(x) > 0: 
            self.plot_ax.plot(x, y)
            self.plot_ax.set_xlim(x[0], x[-1])  
        else:
            self.plot_ax.plot([])

        self.plot_ax.set_ylim(-1, 1)
        self.plot_canvas.draw()


    def plot_vertical_line(self, x, color='black', linestyle='solid', linewidth=1.0, label=None):
        if x:
            self.plot_ax.axvline(x=x, color=color, linestyle=linestyle, linewidth=linewidth)
            if label:
                self.plot_ax.text(x, -0.95, label, fontsize=6, color=color)  
            self.plot_canvas.draw()
