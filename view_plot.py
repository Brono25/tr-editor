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

    def update_plot(self, x=None, y=None):
        self.plot_ax.clear()
        if x is not None and y is not None:
            self.plot_ax.plot(x, y)
        else:
            self.plot_ax.plot([])
        self.plot_canvas.draw()
