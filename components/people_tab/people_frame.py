from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
from components.people_tab import people_tree_view_frame as ptvf
from components.people_tab import person_timeline_frame as ptf

class PeopleFrame(CTkFrame):
    def __init__(self, master, console, params, side_bar, **kwargs):
        super().__init__(master,  **kwargs)

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        

        self.console = console
        self.params = params
        self.side_bar = side_bar

        self.people_tree_view_frame = ptvf.PeopleTreeFrame(self, console, params)
        self.people_tree_view_frame.grid(row=0,  column=0,  sticky="nsew", padx=5, pady=5,)
        self.people_tree_view_frame.grid_propagate(False)

        self.person_timeline_frame = ptf.PersonTimelineFrame(self, console, params)
        self.person_timeline_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5,)
        self.person_timeline_frame.grid_propagate(False)
