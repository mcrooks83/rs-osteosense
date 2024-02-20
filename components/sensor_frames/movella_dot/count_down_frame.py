from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel


class CountDownFrame(CTkFrame):
    def __init__(self, master, console, params, count_down_complete_ref, **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params

        self.count_down_complete_ref = count_down_complete_ref

        self.count_down_end = 0
        self.count_down_start = params.get_count_down_start()

        self.grid(row=1, column=0, sticky="nsew", )
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=1)

        self.count_down_label = CTkLabel(self, text=f"{self.count_down_start}", font=CTkFont(size=100, weight="bold"), text_color="#EF5DA8")
        self.count_down_label.grid(row=1, column=0, sticky="nsew")
    

    def start_countdown(self):
        self.time_remaining = self.count_down_start  # Reset the countdown time
        self.update_countdown()

    def update_countdown(self):
        if self.time_remaining > 0:
            self.count_down_label.configure(text=f"{self.time_remaining}")
            self.time_remaining -= 1
            self.countdown = self.after(1000, self.update_countdown)
        else:
            self.time_remaining -= 1
            self.count_down_label.configure(text=f"{self.time_remaining}")
            self.count_down_complete_ref(True)

        

        