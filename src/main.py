import customtkinter as ctk
import random
from customtkinter import *
from twitchio.ext import commands
import os
from dotenv import load_dotenv
from chat import *
import asyncio

# TODO: ask user TWITCH_ACCESS_TOKEN

# BESCHREIBUNG: Chat Nachrichten und gui laufen gleichzeitg mit threads 
# BESCHREIBUNG: Mit queue die chat nachrichten an main senden

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat")
        self.geometry("800x710")

        self.minsize(800,710)
        self.maxsize(1920,1080)

        self.farben = random.choice(["blue","yellow"])
        chat_thread = threading.Thread(target=run_chat,daemon=True)
        chat_thread.start()

        self.fg_colors = ["#7cafc4","#edd892","#4c9f70"]

        self.textbox = ctk.CTkTextbox(self,width=1920,height=1080,
        font=("opensans",20),text_color="white",)
        self.textbox.place(x=0,y=0)
        self.textbox.insert("end","Chat Nachrichten werden generiert ... \n")

        # nametag farbe ändern mit tag funktion
        self.textbox.tag_config("name_tag", foreground=random.choice(self.fg_colors), )
        self.textbox.tag_config("content_tag", foreground="white", )

        if "Chat Nachrichten werden generiert ..." in self.textbox.get("1.0","end"):
                    self.textbox.configure(text_color="#edd892")

        self.update_chat()


        self.mainloop()

    def update_chat(self):
        try:
            while not chat_queue.empty():
                msg = chat_queue.get()
                
                self.textbox.configure(state="normal")
                name,content = msg.split(":",1)
                self.textbox.insert("end",f"{name}:","name_tag")
                self.textbox.insert("end",f"{content} \n","content_tag")

                self.textbox.yview("end")

                self.textbox.configure(state="disabled")
            self.after(100,self.update_chat)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    App()
