from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel

from PIL import Image, ImageTk
import os


class ProgressResultsFrame(CTkFrame):
    def __init__(self, master, console, params, **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params
        self.configure(fg_color="black")

        self.grid(row=0, column=0, columnspan=2, sticky="nsew", )
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,1,2,3), weight=1)

        
       
        # icon paths (should be a class)
        up_icon_path = os.path.join(os.getcwd(), 'icons', "up_arrow" + '.png')
        down_icon_path = os.path.join(os.getcwd(), 'icons', "down_arrow" + '.png')

        self.up_icon = CTkImage(Image.open(up_icon_path), size=(20, 20))
        self.down_icon = CTkImage(Image.open(down_icon_path), size=(20, 20))

        self.loading_progress_frame = CTkFrame(self, fg_color="transparent")
        self.loading_progress_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.sym_progress_frame = CTkFrame(self, fg_color="transparent")
        self.sym_progress_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

        self.off_progress_frame = CTkFrame(self, fg_color="transparent")
        self.off_progress_frame.grid(row=1, column=2, sticky="nsew", padx=20, pady=10)

        self.absorbtion_frame = CTkFrame(self, fg_color="transparent")
        self.absorbtion_frame.grid(row=1, column=3, sticky="nsew", padx=20, pady=10)
      
        
        self.loading_progress_label = CTkLabel(self.loading_progress_frame, text=f'Weight Bearing:', 
                                               font=CTkFont(size=28, weight="bold"), text_color="#EF5DA8",)
        self.loading_progress_label.grid(row=1, column=0, sticky="nsew", padx=5)
        self.loading_progress_value_label = CTkLabel(self.loading_progress_frame, text=f'20%', image=self.up_icon, compound="left",
                                                     font=CTkFont(size=28, weight="bold"), text_color="#FFFFFF", justify="left")
        self.loading_progress_value_label.grid(row=1, column=1, sticky="nswe", padx=5)

        self.sym_progress_label = CTkLabel(self.sym_progress_frame, text=f'Symmetry:', font=CTkFont(size=28, weight="bold"), text_color="#EF5DA8")
        self.sym_progress_label.grid(row=1, column=0, sticky="nswe", padx=5)

        self.sym_progress_value_label = CTkLabel(self.sym_progress_frame, text=f'5%', image=self.down_icon, compound="left",
                                                 font=CTkFont(size=28, weight="bold"), text_color="#FFFFFF")
        self.sym_progress_value_label.grid(row=1, column=2, sticky="nswe", padx=5)
        
        self.off_progress_label = CTkLabel(self.off_progress_frame, text=f'Off Loading:', 
                                           font=CTkFont(size=28, weight="bold"), text_color="#EF5DA8")
        self.off_progress_label.grid(row=1, column=0, sticky="nsew", padx=5)
  
        self.off_progress_value_label = CTkLabel(self.off_progress_frame, text=f'5% L Heel', image=self.up_icon, compound="left",
                                                 font=CTkFont(size=32, weight="bold"), text_color="#FFFFFF")
        self.off_progress_value_label.grid(row=1, column=2, sticky="nswe", padx=5)

        self.ab_progress_label = CTkLabel(self.absorbtion_frame, text=f'Absorbtion:', 
                                           font=CTkFont(size=28, weight="bold"), text_color="#EF5DA8")
        self.ab_progress_label.grid(row=1, column=0, sticky="nsew", padx=5)
  
        self.ab_progress_value_label = CTkLabel(self.absorbtion_frame, text=f'30%', image=self.up_icon, compound="left",
                                                 font=CTkFont(size=32, weight="bold"), text_color="#FFFFFF")
        self.ab_progress_value_label.grid(row=1, column=2, sticky="nswe", padx=5)

        

        