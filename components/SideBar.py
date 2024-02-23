from customtkinter import CTkFrame 
from customtkinter import CTkLabel, CTkComboBox, StringVar
from customtkinter import CTkFont

class SideBar(CTkFrame):
    def __init__(self, master,  sensor_manager, params,  **kwargs):
        super().__init__(master,  **kwargs)


        #self.console = console
        self.sm = sensor_manager
       
        self.supported_sensors = sensor_manager.get_supported_sensors()
    

        # spans 10 rows
        self.grid(row=0, column=0, rowspan=5, sticky="nsew")
        #self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        #self.configure(width=200)

        self.logo_label = CTkLabel(self, text="Account", font=CTkFont(size=15, weight="bold"), width=200 )
        self.logo_label.grid(row=0, column=0, padx=5, pady=10, )

        self.patient_name = CTkLabel(self, text="", font=CTkFont(size=15, weight="bold"), )
        self.patient_name.grid(row=1, column=0,sticky="nw", padx=20, pady=10, )

    
        # side bar widgets go below in row 1, 2 or 3
        #self.appearance_mode_label = CTkLabel(self, text="Sensor Controls:", anchor="w")
        #self.appearance_mode_label.grid(row=3, column=1, padx=20, pady=(10, 0))
    def set_patient_name(self, name):
        self.patient_name.configure(text=f"{name}")

