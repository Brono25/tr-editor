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


    def plot_segment_bounds(self, start_time, end_time):
        if start_time and end_time:
            self.plot_ax.axvline(x=start_time, color='red')
            self.plot_ax.axvline(x=end_time, color='red')
            self.plot_canvas.draw()

    def plot_overlapped_line(self, x_value, color='lightgrey'):
        if x_value is not None:
            self.plot_ax.axvline(x=x_value, color=color)
            self.plot_canvas.draw()
        
