from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
from components.sensor_frames.movella_dot import protocol_frame as pcolf
from components.sensor_frames.movella_dot import sensor_frame as sf
class MovellaDotLeftFrame(CTkFrame):
    def __init__(self, master, console, params, start_measuring_for_sensors, stop_measuring_for_sensors, set_protocol,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.grid(row=0, column=0, sticky="nsew", )
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1,0), weight=1)
        self.sensor_frame = sf.SensorFrame(self, self.console, self.params)
        self.sensor_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")
        self.sensor_frame.grid_propagate(False)
        self.protcol_frame = pcolf.ProtocolFrame(self, self.console, self.params, start_measuring_for_sensors, stop_measuring_for_sensors, set_protocol)
        self.protcol_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nesw")
        self.protcol_frame.grid_propagate(False)
    

        

        