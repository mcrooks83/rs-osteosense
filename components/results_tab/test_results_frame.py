from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
from components.sensor_frames.movella_dot import protocol_frame as pcolf
from components.sensor_frames.movella_dot import sensor_frame as sf

class TestResultsFrame(CTkFrame):
    def __init__(self, master, console, params, **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.grid(row=0, column=0, sticky="nsew", )
        self.grid_columnconfigure((0), weight=1)
        #self.grid_rowconfigure((1,0), weight=1)

        self.count_down_label = CTkLabel(self, text=f'Test Results', font=CTkFont(size=22, weight="bold"), text_color="#EF5DA8")
        self.count_down_label.grid(row=0, column=0, sticky="nsew")
        
    

        

        