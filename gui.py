import tkinter as Tk
import customtkinter 
## imports
from os import listdir, getcwd, makedirs
from os.path import exists
import sys
import os

from components.Title import Title
from components.SideBar import SideBar
from components.Tab import Tab
from components.Console import Console
from classes.LocalSensorManager import LocalSensorManager
import classes.params as p


#### Main UI using Tkinter ###

class MainApplication(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.sensor_manager = LocalSensorManager()
        params = p.Parameters()

        self.sensor_manager.initialise_sdk()

        self.title("Right Step")

        self.width = self.winfo_screenwidth() 
        self.height = self.winfo_screenheight()
        self.geometry(self.CenterWindowToDisplay(self.width, self.height))
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((1 ), weight=1)
        
        self.title_label = Title(self, text="OsteoSense Test Suite")     
        self.side_bar = SideBar(self,  self.sensor_manager, params)
        self.console = Console(self.side_bar)
        #self.side_bar.grid_propagate(False)
        self.tab_view = Tab(self, self.console, self.sensor_manager, params, self.side_bar)

    def CenterWindowToDisplay(self, width: int, height: int, scale_factor: float = 1.0):
        """Centers the window to the main display/monitor"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width/2) - (width/2)) * scale_factor)
        y = int(((screen_height/2) - (height)) * scale_factor)
        print("y", y)
        return f"{width}x{height}+{0}+{0}"   
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
       
def on_keyboard_interrupt( event):
        print("killing app", event)
        app.destroy()
        os._exit(0)
        
if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    app = MainApplication()

    app.bind("<Control-c>", on_keyboard_interrupt)

    app.mainloop()

