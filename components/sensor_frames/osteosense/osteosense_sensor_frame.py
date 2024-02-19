from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
#from matplotlib.pyplot import Figure
#from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
#from matplotlib import style
#from mpl_toolkits.axisartist.axislines import AxesZero
#style.use('fivethirtyeight')
#style.use("dark_background")
#import threading
#import math

class OsteoSenseSensorFrame(CTkFrame):
    def __init__(self, master, console, params,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.grid(row=0, column=0, sticky="nw")
        #self.grid_columnconfigure(0, weight=1)

        self.logo_label = CTkLabel(self, text="OsteoSense Sensor Frame", font=CTkFont(size=15, weight="bold") )
        self.logo_label.grid(row=0, column=0, padx=5, )

        