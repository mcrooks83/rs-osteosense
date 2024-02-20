from customtkinter import CTkToplevel, CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel,CTkInputDialog

class AssignSensorWindow(CTkToplevel):
    def __init__(self, master, address, assignment_ref, params,   **kwargs):
        super().__init__(master,  **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = 300
        height = 200

        # Calculate the x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        # Set the geometry of the Toplevel window
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.title("Assign Sensor")
        #self.iconify()
        self.address = address
        self.params = params

        #self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


        self.label = CTkLabel(self, text=f"{self.address}")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.placement_select = CTkComboBox(self, values=self.params.get_placements(),
                                     command=self.on_placement_select,) #variable=selected_sensor_var)
        #self.sensor_select.grid(row=1, column=0,sticky='nw',padx=10,)
        self.placement_select.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        self.assignment_ref = assignment_ref
    
    def on_placement_select(self, placement):
        print(f"{placement}")
        self.assignment_ref(self.address, placement)
        self.assigned_label = CTkLabel(self, text=f"Assigned to {placement}", text_color="#EF5DA8")
        self.assigned_label.grid(row=2, column=0,padx=5, pady=5, sticky="nsew")
