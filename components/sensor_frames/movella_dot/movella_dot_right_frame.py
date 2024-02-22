from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib import style
from mpl_toolkits.axisartist.axislines import AxesZero
#style.use('fivethirtyeight')
style.use("dark_background")
#import threading
#import math

from components.sensor_frames.movella_dot import count_down_frame as cdf
from components.sensor_frames.movella_dot import plot_frame as pf

class MovellaDotRightFrame(CTkFrame):
    def __init__(self, master, console, params, count_down_complete_ref,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)

        self.protocol_label = CTkLabel(self, text="No Protocol Selected", fg_color="#5D5FEF", font=CTkFont(size=12, weight="bold"))
        self.protocol_label.grid(row=0, column=0, sticky="nesw")

        # add this frame into a holding frame
        self.plot_frame = pf.PlotFrame(self, self.console, self.params)

        self.count_down_frame = cdf.CountDownFrame(self, self.console, self.params, count_down_complete_ref)
        
    def raise_frame(self, frame):
        frame.lift()
    
    def lower_frame(self, frame):
        frame.lower()

        