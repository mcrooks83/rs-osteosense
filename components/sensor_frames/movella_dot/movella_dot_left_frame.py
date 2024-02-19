from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
#from matplotlib.pyplot import Figure
#from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
#from matplotlib import style
#from mpl_toolkits.axisartist.axislines import AxesZero
#style.use('fivethirtyeight')
#style.use("dark_background")
#import threading
#import math

class MovellaDotLeftFrame(CTkFrame):
    def __init__(self, master, console, params,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.console = console
        self.params = params

        self.grid(row=0, column=0, sticky="nsew", )
        #self.grid_columnconfigure((0), weight=1)
        #self.grid_rowconfigure((0), weight=1)
        
        #self.grid_columnconfigure(0, weight=1)

        self.logo_label = CTkLabel(self, text="Movella Dot Left Frame", font=CTkFont(size=15, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=5, pady=(20, 20), sticky="nwse" )

        

        