from customtkinter import CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel

from components.sensor_frames.movella_dot import movella_dot_sensor_frame as mdsf
from components.sensor_frames.osteosense import  osteosense_sensor_frame as ossf

import inspect

# currently not in use
class Tab(CTkTabview):
    def __init__(self, master, console, sensor_manager, params,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(anchor="w")

        self.console = console
        self.params = params
        self.sm = sensor_manager
        self.supported_sensors = sensor_manager.get_supported_sensors()

        #variables
        self.connect_to_pos = 0
        
        self.grid(row=1, column=1, rowspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
       
        self.add("Sensors")
        self.add("Data Capture")
        
        self.tab1 = self.tab("Sensors")
        self.tab1.grid_columnconfigure((0,1), weight=1)  # Column weight
        #self.tab1.grid_rowconfigure(1, weight=1)
        self.tab1.grid_rowconfigure(2,weight=1)  # Column weight
        
        # sensor select
        self.select_sensor_label = CTkLabel(self.tab1, text="Select Sensor", font=CTkFont(size=12, weight="bold"))
        self.select_sensor_label.grid(row=0, column=0,rowspan=1, padx=10, sticky='nw')
        
        #self.params.set_selected_sensor  = StringVar(value=self.supported_sensors[1])
        self.sm.manager.set_selected_sensor(self.supported_sensors[1])
        self.sensor_select = CTkComboBox(self.tab1, values=self.supported_sensors,
                                     command=self.load_sensor_frame,) #variable=selected_sensor_var)
        self.sensor_select.grid(row=1, column=0,sticky='nw',padx=10,)
        #self.sensor_select.bind("<<ComboboxSelected>>", self.load_sensor_frame)

        self.tab1.sensor_frame = None



    def load_sensor_frame(self, sensor):
        print(f"{sensor} selected")  

        #destroy previous frame if exisits
        if(self.tab1.sensor_frame):
             self.tab1.sensor_frame.destroy()               
        
        if(sensor == "Movella Dot"):
            print("loading Movella Dot Frame")
            self.tab1.sensor_frame = mdsf.MovellaDotSensorFrame(self.tab1, self.sm, self.console, self.params)
            self.tab1.sensor_frame.grid(row=2, column=0, columnspan=2)
        elif(sensor == "OsteoSense"):
            self.tab1.sensor_frame = ossf.OsteoSenseSensorFrame(self.tab1, self.sm,self.console, self.params)
            self.tab1.sensor_frame.grid(row=2, column=0, columnspan=2)

    

    

    

    

