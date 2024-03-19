from customtkinter import CTkFrame 
from customtkinter import CTkLabel, CTkComboBox, StringVar
from customtkinter import CTkFont

class SideBar(CTkFrame):
    def __init__(self, master,  sensor_manager, params,  **kwargs):
        super().__init__(master,  **kwargs)

        self.sm = sensor_manager
        self.supported_sensors = sensor_manager.get_supported_sensors()
    
        # spans 10 rows
        self.grid(row=0, column=0, rowspan=5, sticky="nsew")
        #self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
    

