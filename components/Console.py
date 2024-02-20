from customtkinter import CTkLabel 
from customtkinter import CTkFont
from customtkinter import CTkFrame as Frame
from customtkinter import CTkTextbox 

from tkinter import  INSERT,END

class Console(CTkTextbox):
    def __init__(self, master,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        #self.console = CTkTextbox(self, state='normal', width=500)
        self.grid(row=4, column=1, columnspan=3, padx=(20, 20), pady=(5, 5), sticky="ews")
        self.insert("0.0", "-| OsteoSense Logs |- \n\n" )
   
    def insert_text(self, text):
        self.configure(state ='normal')
        self.insert(INSERT,text)
        self.insert(INSERT, "\n")
        self.configure(state='disabled')
        #self.set_yview(END)
    
    def clear_console(self):
        self.configure(state ='normal')
        self.delete("2.0","end")
        #self.console.delete("0.0", "end")  # delete all text
        self.insert(INSERT, "\n\n")
        #self.display_title_text()
        self.configure(state="disabled")