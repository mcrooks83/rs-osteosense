import tkinter as Tk
import customtkinter 
## imports
from os import listdir, getcwd, makedirs
from os.path import exists

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

        # setup sensor sdk
        self.sensor_manager = LocalSensorManager()
        params = p.Parameters()

        self.sensor_manager.initialise_sdk()
        

        self.title("Right Step")

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}")
       


        # configure grid layout (4x4)
        #self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((1 ), weight=1)

        self.console = Console(self)
        self.title_label = Title(self, text="OsteoSense Test Suite")     
        self.side_bar = SideBar(self, self.console, self.sensor_manager, params)
        self.tab_view = Tab(self, self.console, self.sensor_manager, params)
       
       
       

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
       

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


    app = MainApplication()
    app.mainloop()

