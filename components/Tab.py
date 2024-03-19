from customtkinter import CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel,CTkFrame

from components.sensor_frames.movella_dot import movella_dot_sensor_frame as mdsf
from components.sensor_frames.osteosense import  osteosense_sensor_frame as ossf
from components.results_tab import results_tab_frame as rtf
from components.people_tab import people_frame as ptvf


import inspect

# currently not in use
class Tab(CTkTabview):
    def __init__(self, master, console, sensor_manager, params, sidebar,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(anchor="w", segmented_button_fg_color="#EF5DA8") 

        self.console = console
        self.params = params
        self.side_bar = sidebar
        self.sm = sensor_manager
        self.supported_sensors = sensor_manager.get_supported_sensors()

        #variables
        self.connect_to_pos = 0
        self.grid(row=1, column=1,  padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        #self.add("People")
        self.add("Tests")
        self.add("Results")

        self.set_tab_view("Tests")  # set currently visible tab

        ##### TAB 0
        #self.tab0 = self.tab("People")
        #self.tab0.grid_columnconfigure((0,1), weight=1)  # Column weight
        #self.tab0.people_frame = ptvf.PeopleFrame(self.tab0, console, params, self.side_bar)
        #self.tab0.people_frame.grid(row=1, column=0, columnspan=2, rowspan=3)
        #self.tab0.grid_rowconfigure(1,weight=1)  # Row weight
        
        ##### TAB 1
        self.tab2 = self.tab("Results")
        self.tab2.grid_columnconfigure((0,1), weight=1)  # Column weight
        self.tab2.results_tab_frame = rtf.ResultsTabFrame(self.tab2, console, params, self.side_bar)
        self.tab2.results_tab_frame.grid(row=2, column=0, columnspan=2, rowspan=3)  # spans two columns that are "created" by the parent view
        self.tab2.grid_rowconfigure((2),weight=1)  # Column weight

        ##### TAB 2
        self.tab1 = self.tab("Tests")
        self.tab1.grid_columnconfigure((0,1), weight=1)  # Column weight
        #self.tab1.grid_rowconfigure(1, weight=1)
        self.tab1.grid_rowconfigure(2,weight=1)  # Row weight
        
        # sensor select
        self.tab1.title_frame = CTkFrame(self.tab1, fg_color="transparent")
        self.tab1.title_frame.grid(row=0, column=0, sticky='nesw', )

        self.select_sensor_label = CTkLabel(self.tab1.title_frame, text="Select Sensor", font=CTkFont(size=14, weight="bold"),  text_color="#EF5DA8")
        self.select_sensor_label.grid(row=0, column=0,rowspan=1, padx=10, sticky='nw')
        
        #self.params.set_selected_sensor  = StringVar(value=self.supported_sensors[1])
        self.sm.manager.set_selected_sensor(self.supported_sensors[1])
        self.sensor_select = CTkComboBox(self.tab1.title_frame, values=self.supported_sensors,
                                     command=self.load_sensor_frame,) #variable=selected_sensor_var)
        self.sensor_select.grid(row=0, column=1,sticky='nw',padx=10,)
        #self.sensor_select.bind("<<ComboboxSelected>>", self.load_sensor_frame)

        self.tab1.sensor_frame = None

    def set_tab_view(self, tab_name):
        self.set(f"{tab_name}")

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

    

    

    

    

