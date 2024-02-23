from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
import customtkinter
from tkinter import ttk

class PeopleTreeFrame(CTkFrame):
    def __init__(self, master, console, params, **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params
        self.configure(border_color="#5D5FEF", border_width=2) #5D5FEF #EF5DA8

        self.grid(row=0, column=0, sticky="nsew",  )
        self.grid_rowconfigure((1,2), weight=1)
        self.grid_columnconfigure((0,1), weight=1)


        self.people_tree_title = CTkLabel(self, text=f'People', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#FFFFFF",)
        self.people_tree_title.grid(row=0, column=0,columnspan=2, sticky="new", padx=10, pady=5)

        