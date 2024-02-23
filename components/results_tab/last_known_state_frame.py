from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
import os
from PIL import Image, ImageTk

from matplotlib.pyplot import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib import style
from mpl_toolkits.axisartist.axislines import AxesZero
#style.use('fivethirtyeight')
style.use("dark_background")

# last known state example
class LastKnownStateFrame(CTkFrame):
    def __init__(self, master, console, params, **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params
        self.configure(border_color="#EF5DA8", border_width=2) #5D5FEF #EF5DA8

        self.grid(row=0, column=0, sticky="nsew",  )
        self.grid_rowconfigure((2), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.test_results_name_label = CTkLabel(self, text=f'Last Known State', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#FFFFFF",)
        self.test_results_name_label.grid(row=0, column=0,columnspan=2, sticky="new", padx=10, pady=5)

        self.comparison_frame = CTkFrame(self)
        self.comparison_frame.grid(row=2, column=0,columnspan=2, sticky="nsew", padx=10, pady=10)
        self.comparison_frame.grid_columnconfigure((0), weight=1)
        self.comparison_frame.grid_propagate(False)

        self.stream_fig = Figure(figsize=(5,3))
        self.ax = self.stream_fig.subplots()
        self.ax.set_title(f"Progress Comparison", fontsize=10)
        self.ax.set_xlabel("Time", fontsize=10)
        self.stream_fig.subplots_adjust(bottom=0.2, left=0.05, right=0.95, )             

        self.stream_fig_canvas = FigureCanvasTkAgg(self.stream_fig, master=self.comparison_frame)
        self.stream_fig_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        self.test_results_frame = CTkFrame(self)
        self.test_results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10 )
        #self.test_results_frame.grid_propagate(False)

        self.image_frame = CTkFrame(self)
        self.image_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.image_frame.grid_columnconfigure((0), weight=1)
        #self.image_frame.grid_propagate(False)
        

        self.loading_results_title = CTkLabel(self.test_results_frame, text=f'Last Results', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#FFFFFF",)
        self.loading_results_title.grid(row=0, column=0, sticky="nsw", padx=5, )

        self.weight_bearing_title = CTkLabel(self.test_results_frame, text=f'Weight Bearing:',
                                               font=CTkFont(size=12, weight="bold"), text_color="#EF5DA8",)
        self.weight_bearing_title.grid(row=1, column=0, sticky="nsw", padx=5, pady=10)

        self.weight_bearing = CTkLabel(self.test_results_frame, text=f"AVG: L: 3.6, R: 2.3, W: 1.7 (BW/s)", 
                                               font=CTkFont(size=12, ), text_color="#FFFFFF",)
        self.weight_bearing.grid(row=1, column=1, sticky="nsw", padx=5, pady=10 )

        self.sym_title = CTkLabel(self.test_results_frame, text=f'Symmetry:',
                                               font=CTkFont(size=12, weight="bold"), text_color="#EF5DA8",)
        self.sym_title.grid(row=2, column=0, sticky="nsw", padx=5,pady=10 )

        self.sym = CTkLabel(self.test_results_frame, text=f"Very Imbalanced 87%",
                                               font=CTkFont(size=12, ), text_color="#FFFFFF",)
        self.sym.grid(row=2, column=1, sticky="nsw", padx=5,  )

        self.favour_title = CTkLabel(self.test_results_frame, text=f'Domiant:',
                                               font=CTkFont(size=12, weight="bold"), text_color="#EF5DA8",)
        self.favour_title.grid(row=3, column=0, sticky="nsw", padx=5, pady=10)

        self.favour = CTkLabel(self.test_results_frame, text=f"LEFT" ,
                                               font=CTkFont(size=12, ), text_color="#FFFFFF",)
        self.favour.grid(row=3, column=1, sticky="nsw", padx=5,  pady=10)

        self.missing_title = CTkLabel(self.test_results_frame, text=f'Missing Gait:',
                                               font=CTkFont(size=12, weight="bold"), text_color="#EF5DA8",)
        self.missing_title.grid(row=4, column=0, sticky="nsw", padx=5,pady=10 )

        self.missing = CTkLabel(self.test_results_frame, text=f"L Heel Strike" ,
                                               font=CTkFont(size=12, ), text_color="#FFFFFF",)
        self.missing.grid(row=4, column=1, sticky="nsw", padx=5,  pady=10)


         # scan frame
        self.scan_title = CTkLabel(self.image_frame, text=f'Latest Scan', 
                                               font=CTkFont(size=22, weight="bold"), text_color="#FFFFFF",)
        self.scan_title.grid(row=0, column=0, sticky="nsw", padx=10,)

        scan_image_path = os.path.join(os.getcwd(), 'images', "knee-mri" + '.jpeg')
        self.scan_image = CTkImage(Image.open(scan_image_path), size=(215,215))

        self.scan_image_label = CTkLabel(self.image_frame, text="", image=self.scan_image, justify="center")
        self.scan_image_label.grid(row=1, column=0, sticky="nswe", pady=10)


        self.scan_details_limb_label = CTkLabel(self.image_frame, text="Left knee 28/02/2024", justify="center",
                                           font=CTkFont(size=12), text_color="#EF5DA8",)
        self.scan_details_limb_label.grid(row=2, column=0, sticky="nsw", padx=5,)

        self.scan_details_stat_label = CTkLabel(self.image_frame, text="BMD T: -1.5", justify="center",
                                           font=CTkFont(size=12), text_color="#EF5DA8",)
        self.scan_details_stat_label.grid(row=3, column=0, sticky="nsw", padx=5,)
  


        

        

