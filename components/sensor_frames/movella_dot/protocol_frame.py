from customtkinter import CTkFrame, CTkTextbox, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel

from test_data import protocols
from components.sensor_frames.movella_dot import instructions_window as iw

class ProtocolFrame(CTkFrame):
    def __init__(self, master, console, params, start_measuring_for_sensors, stop_measuring_for_sensors, set_protocol,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.start_measuring_for_sensors_ref = start_measuring_for_sensors
        self.stop_measuring_for_sensors_ref = stop_measuring_for_sensors
        self.set_protocol_ref = set_protocol

        self.protocols = protocols.protocols
        self.protocol_names = [p["name"] for p in self.protocols]

        self.selected_protocol = None
        
        self.grid(row=0, column=0, sticky="nsew", )

        self.title_frame = CTkFrame(self, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, sticky='nesw', )

        self.protocol_label = CTkLabel(self.title_frame, text=f"Protocols:", font=CTkFont(size=14, weight="bold"), text_color="#EF5DA8")
        self.protocol_label.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        self.protocol_select = CTkComboBox(self.title_frame, values=self.protocol_names,
                                     command=self.on_protocol_select,) #variable=selected_sensor_var)
        #self.sensor_select.grid(row=1, column=0,sticky='nw',padx=10,)
        self.protocol_select.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        self.status_label = None
    

    def on_protocol_select(self, protocol):
        self.console.clear_console()
        self.console.insert_text(f"selected protcol: {protocol}") 

        

        #get the full protocol
        self.selected_protocol = [p for p in self.protocols if p["name"] == protocol ][0]
        reps = self.selected_protocol["repetitions"]
        time_per_rep = self.selected_protocol["time_per_rep"]
        distance_per_rep = self.selected_protocol["distance"]
        description = self.selected_protocol["description"]

       
        # create a table of details (move to component and pass headers / values to it)
        self.protocol_details = CTkFrame(self, fg_color="transparent")
        self.protocol_details.grid(row=2, column=0, columnspan=2, sticky='nesw', )   
        
        self.description_header = CTkLabel(self.protocol_details, text="Description:", text_color="#5D5FEF").grid(row=0, column=0, padx=5, pady=5,  sticky="nes")
        self.description_label = CTkLabel(self.protocol_details, text=f"{description}", text_color="#FFFFFF").grid(row=0, column=1, padx=5, pady=5,  sticky="nws")

        #self.instructions_header = CTkLabel(self.protocol_details, text="Instructions:", text_color="#5D5FEF").grid(row=1, column=0, padx=5,  sticky="nesw")
        self.view_instructions_btn = CTkButton(self.protocol_details, text="View Instructions",fg_color="#EF5DA8", corner_radius=50, command=self.view_instructions).grid(row=0, column=2, padx=5, pady=5, sticky="nws")

        self.reps_header = CTkLabel(self.protocol_details, text="Repetitions:", text_color="#5D5FEF").grid(row=2, column=0, padx=5,  sticky="nesw")
        self.time_header = CTkLabel(self.protocol_details, text="Rep Duration:", text_color="#5D5FEF").grid(row=2, column=1, padx=5,  sticky="nesw")
        self.distance_header = CTkLabel(self.protocol_details, text="Rep Distance:", text_color="#5D5FEF").grid(row=2, column=2, padx=5,  sticky="nesw")

        self.reps_label = CTkLabel(self.protocol_details, text=f"{reps}", text_color="#FFFFFF").grid(row=3, column=0, padx=5,  sticky="nesw")
        self.time_label = CTkLabel(self.protocol_details, text=f"{time_per_rep}s", text_color="#FFFFFF").grid(row=3, column=1, padx=5,  sticky="nesw")
        self.distance_label = CTkLabel(self.protocol_details, text=f"{distance_per_rep}m", text_color="#FFFFFF").grid(row=3, column=2, padx=5,  sticky="nesw")
       
        self.start_stop_frame = CTkFrame(self, fg_color="transparent")
        self.start_stop_frame.grid(row=4, column=0, columnspan=2, sticky='nesw', padx=5, pady=20)

        self.start_measuring_btn =  CTkButton(self.start_stop_frame, text="start test", fg_color="#5D5FEF", command=self.start_measuring_for_sensors_ref )
        self.start_measuring_btn.grid(row=0, column=0, sticky='nwse',  padx=5, pady=5 )
        
        if(time_per_rep == 0):
            self.stop_measuring_btn =  CTkButton(self.start_stop_frame, text="stop test", fg_color="#5D5FEF", command=self.stop_measuring_for_sensors_ref )
            self.stop_measuring_btn.grid(row=0, column=1, sticky='nwse',  padx=5, pady=5 )

        self.reset_protocl_btn =  CTkButton(self.start_stop_frame, text="reset test", fg_color="#159BAD", command= self.reset_protcol )
        self.reset_protocl_btn.grid(row=0, column=2, sticky='nwse',  padx=5, pady=5 )

      
        self.status_label = CTkLabel(self.start_stop_frame, text=f"reps complete: 0, reps to go: {reps}", text_color="#FFFFFF")
        self.status_label.grid(row=1, column=0, padx=5,  pady=5, sticky="nesw")
       
        self.set_protocol_ref(self.selected_protocol)

    def reset_protcol(self):
        self.set_protocol_ref(self.selected_protocol)

    def view_instructions(self):
        self.iw = iw.InstructionsWindow(self, self.selected_protocol)

    def update_status(self, status):
        self.status_label.configure(text=status)

    def complete_protocol(self):
        self.save_results_button =  CTkButton(self.start_stop_frame, text="save test", fg_color="#5D5FEF", command=self.stop_measuring_for_sensors_ref )
        self.save_results_button.grid(row=0, column=3, sticky='nwse',  padx=5, pady=5 )


    

        

        