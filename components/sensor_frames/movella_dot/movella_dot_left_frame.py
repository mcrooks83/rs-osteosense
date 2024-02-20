from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel


class MovellaDotLeftFrame(CTkFrame):
    def __init__(self, master, console, params,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.grid(row=0, column=0, sticky="nsew", )
        #self.grid_columnconfigure((0), weight=1)
        #self.grid_rowconfigure((0), weight=1)
    

        

        