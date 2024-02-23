from customtkinter import CTkToplevel, CTkTextbox,  CTkLabel


class InstructionsWindow(CTkToplevel):
    def __init__(self, master, protocol,   **kwargs):
        super().__init__(master,  **kwargs)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = 500
        height = 200

        # Calculate the x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        # Set the geometry of the Toplevel window
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.title("Protocol Instructions")

        print(protocol)

        self.protocol = protocol
        self.protocol_name = self.protocol["name"]
        self.instructions = self.protocol["instructions"]
        
        #self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


        self.label = CTkLabel(self, text=f"{self.protocol_name}")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.textbox = CTkTextbox(self, width=400, corner_radius=10)
        self.textbox.grid(row=1, column=0, sticky="nsew")
        self.textbox.insert("0.0", f"{self.instructions}\n")


       
