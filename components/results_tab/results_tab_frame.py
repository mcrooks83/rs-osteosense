from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
from components.results_tab import test_results_frame as trf
from components.results_tab import last_known_state_frame as lksf
from components.results_tab import progress_results_frame as prf
# holds all the frames for the results tab
class ResultsTabFrame(CTkFrame):
    def __init__(self, master, console, params, **kwargs):
        super().__init__(master,  **kwargs)

        self.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.console = console
        self.params = params

        self.test_results_frame = prf.ProgressResultsFrame(self, console, params)
        self.test_results_frame.grid(row=0,  column=0, columnspan=2, sticky="nsew", padx=5, pady=5,)
        #self.test_results_frame.grid_propagate(False)

        self.test_results_frame = trf.TestResultsFrame(self, console, params)
        self.test_results_frame.grid(row=1, rowspan=2, column=0, sticky="nsew", padx=5, pady=5,)
        self.test_results_frame.grid_propagate(False)

        self.last_known_state_frame = lksf.LastKnownStateFrame(self, console, params)
        self.last_known_state_frame.grid(row=1, rowspan=2, column=1, sticky="nsew", padx=5, pady=5,)
        self.last_known_state_frame.grid_propagate(False)

       