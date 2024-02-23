from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel


from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib import style
from mpl_toolkits.axisartist.axislines import AxesZero
#style.use('fivethirtyeight')
style.use("dark_background")
class TestResultsFrame(CTkFrame):
    def __init__(self, master, console, params, **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params
        self.configure(border_color="#5D5FEF", border_width=2) #5D5FEF #EF5DA8

        self.grid(row=0, column=0, sticky="nsew",  )
        self.grid_rowconfigure((1,2), weight=1)
        self.grid_columnconfigure((0,1), weight=1)


        self.test_results_name_label = CTkLabel(self, text=f'Protocol: 10m Walk, Test: Weight Bearing', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#FFFFFF",)
        self.test_results_name_label.grid(row=0, column=0,columnspan=2, sticky="new", padx=10, pady=5)

        self.loading_distribution_frame = CTkFrame(self)
        self.loading_distribution_frame.grid(row=2, column=0,columnspan=2, sticky="nsew", padx=10,pady=10)
        self.loading_distribution_frame.grid_columnconfigure((0), weight=1)
        #self.comparison_frame.grid_columnconfigure((0), weight=1)
        self.loading_distribution_frame.grid_propagate(False)

        self.stream_fig = Figure(figsize=(5,3))
        self.ax = self.stream_fig.subplots()
        self.ax.set_title(f"Loading Distribution", fontsize=10)
        self.ax.set_xlabel("5s Blocks", fontsize=10)
        self.stream_fig.subplots_adjust(bottom=0.2, left=0.05, right=0.95, )        

        self.stream_fig_canvas = FigureCanvasTkAgg(self.stream_fig, master=self.loading_distribution_frame)
        self.stream_fig_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        self.loading_results_frame = CTkFrame(self)
        self.loading_results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10 )
        #self.loading_results_frame.grid_propagate(False)
        #self.loading_results_frame.grid_columnconfigure((0), weight=1)

        self.freq_results_frame = CTkFrame(self)
        self.freq_results_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        #self.freq_results_frame.grid_propagate(False)
        self.freq_results_frame.grid_columnconfigure((0,1), weight=1)
        self.freq_results_frame.grid_rowconfigure((0,1,2,3), weight=1)

        self.loading_results_title = CTkLabel(self.loading_results_frame, text=f'Results', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#FFFFFF",)
        self.loading_results_title.grid(row=0, column=0, sticky="nsw", padx=5, )

        self.weight_bearing_title = CTkLabel(self.loading_results_frame, text=f'Weight Bearing:',
                                               font=CTkFont(size=12, weight="bold"), text_color="#5D5FEF",)
        self.weight_bearing_title.grid(row=1, column=0, sticky="nsw", padx=5, pady=10)

        self.weight_bearing = CTkLabel(self.loading_results_frame, text=f"AVG: L: 3.6, R: 2.3, W: 1.7 (BW/s)", 
                                               font=CTkFont(size=12, ), text_color="#FFFFFF",)
        self.weight_bearing.grid(row=1, column=1, sticky="nsw", padx=5,  pady=10)

        self.sym_title = CTkLabel(self.loading_results_frame, text=f'Symmetry:',
                                               font=CTkFont(size=12, weight="bold"), text_color="#5D5FEF",)
        self.sym_title.grid(row=2, column=0, sticky="nsw", padx=5, pady=10)

        self.sym = CTkLabel(self.loading_results_frame, text=f"Very Imbalanced 87%",
                                               font=CTkFont(size=12, ), text_color="#FFFFFF",)
        self.sym.grid(row=2, column=1, sticky="nsw", padx=5,  pady=10)

        self.favour_title = CTkLabel(self.loading_results_frame, text=f'Domiant:',
                                               font=CTkFont(size=12, weight="bold"), text_color="#5D5FEF",)
        self.favour_title.grid(row=3, column=0, sticky="nsw", padx=5, pady=10)

        self.favour = CTkLabel(self.loading_results_frame, text=f"LEFT" ,
                                               font=CTkFont(size=12, ), text_color="#FFFFFF",)
        self.favour.grid(row=3, column=1, sticky="nsw", padx=5,  pady=10)

        self.missing_title = CTkLabel(self.loading_results_frame, text=f'Missing Gait:',
                                               font=CTkFont(size=12, weight="bold"), text_color="#5D5FEF",)
        self.missing_title.grid(row=4, column=0, sticky="nsw", padx=5, pady=10)

        self.missing = CTkLabel(self.loading_results_frame, text=f"L Heel Strike" ,
                                               font=CTkFont(size=12, ), text_color="#FFFFFF",)
        self.missing.grid(row=4, column=1, sticky="nsw", padx=5,  pady=10)



  

        self.low_freq_left_title = CTkLabel(self.freq_results_frame, text=f'Left Low Frequency', 
                                               font=CTkFont(size=14, weight="bold"), text_color="#FFFFFF",)
        self.low_freq_left_title.grid(row=0, column=0, sticky="new", padx=5, )
        self.low_freq_left = CTkLabel(self.freq_results_frame, text=f'49%', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#5D5FEF",)
        self.low_freq_left.grid(row=1, column=0, sticky="new", padx=5, )

        self.low_freq_right_title = CTkLabel(self.freq_results_frame, text=f'Right Low Frequency', 
                                               font=CTkFont(size=14, weight="bold"), text_color="#FFFFFF",)
        self.low_freq_right_title.grid(row=2, column=0, sticky="new", padx=5, )

        self.low_freq_right = CTkLabel(self.freq_results_frame, text=f'51%', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#5D5FEF",)
        self.low_freq_right.grid(row=3, column=0, sticky="new", padx=5, )


        self.high_freq_left_title = CTkLabel(self.freq_results_frame, text=f'Left High Frequency', 
                                               font=CTkFont(size=14, weight="bold"), text_color="#FFFFFF",)
        self.high_freq_left_title.grid(row=0, column=1, sticky="new", padx=5, )

        self.high_freq_right = CTkLabel(self.freq_results_frame, text=f'23%', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#5D5FEF",)
        self.high_freq_right.grid(row=1, column=1, sticky="new", padx=5, )

        self.high_freq_right_title = CTkLabel(self.freq_results_frame, text=f'Right High Frequency', 
                                               font=CTkFont(size=14, weight="bold"), text_color="#FFFFFF",)
        self.high_freq_right_title.grid(row=2, column=1, sticky="new", padx=5, )

        self.high_freq_left = CTkLabel(self.freq_results_frame, text=f'77%', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#5D5FEF",)
        self.high_freq_left.grid(row=3, column=1, sticky="new", padx=5)


        

        
    

        

        