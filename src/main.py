import customtkinter as ctk
from customtkinter import *

# TODO: ask user TWITCH_ACCESS_TOKEN
# TODO: Get api data
# TODO: Daten in eine große textbox einfügen
# TODO: Mehrere Dateien?

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat")
        self.geometry("400x500")

        self.minsize(400,500)
        self.maxsize(400,500)



        self.mainloop()

App()
