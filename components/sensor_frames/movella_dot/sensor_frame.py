from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
from components.test_tab import protocol_frame as pcolf

class SensorFrame(CTkFrame):
    def __init__(self, master, console, params,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.grid(row=0, column=0, sticky="nsew", )

       

    

        

        