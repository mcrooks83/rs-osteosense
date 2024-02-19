from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib import style
from mpl_toolkits.axisartist.axislines import AxesZero
#style.use('fivethirtyeight')
style.use("dark_background")
#import threading
#import math

class MovellaDotRightFrame(CTkFrame):
    def __init__(self, master, console, params,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
    

        self.stream_fig = Figure()
        self.ax = self.stream_fig.subplots()
        self.ax.set_title(f"Acceleration")
        self.ax.set_xlabel("packet count")
        self.stream_fig.subplots_adjust(bottom=0.15)        

        self.stream_fig_canvas = FigureCanvasTkAgg(self.stream_fig, master=self)
        self.stream_fig_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew', padx=5, pady=10)
        


        