from customtkinter import CTkLabel as Label
from customtkinter import CTkFont

class Title(Label):
    def __init__(self, master, text, *args, **kwargs):
        super().__init__(master, height=30,font=CTkFont(size=18, weight="bold"),  text=text, justify="center", *args, **kwargs)
        self.grid(row=0, column=0, columnspan=2, sticky='nsew')
