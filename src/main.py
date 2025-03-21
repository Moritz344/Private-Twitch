import customtkinter as ctk
import sys
import random
import multiprocessing
from customtkinter import *
from twitchio.ext import commands
import os
from dotenv import load_dotenv
from chat import *
import asyncio
from tkinter import *
import tkinter as tk
from PIL import Image,ImageTk

# TODO: ask user TWITCH_ACCESS_TOKEN

# BESCHREIBUNG: Chat Nachrichten und gui laufen gleichzeitg mit threads 
# BESCHREIBUNG: Mit queue die chat nachrichten an main senden

# TODO: FINDE EINEN WEG DEN CHAT ZU STOPPEN




class NavBar(object):
    def __init__(self,window,textbox,streamer):
        
        self.btnState = False
        self.nav_icon = ctk.CTkImage(Image.open("assets/menu.png"),size=(30,30))
        self.close_icon = ctk.CTkImage(Image.open("assets/close.png"),size=(30,30))

        self.textbox = textbox
        self.streamer_liste = (list(streamer))
        
        self.window = window
        self.frame_color = "#333333"
        
        self.topFrame = ctk.CTkFrame(window,fg_color=self.frame_color,height=50)
        self.topFrame.pack(padx=0,pady=0,side="top",fill=tk.X)

        self.navbarBtn = ctk.CTkButton(self.topFrame,text="",
        image=self.nav_icon,hover_color=self.frame_color,fg_color=self.frame_color,border_width=0,
        command=self.switch)
        self.navbarBtn.place(x=0,y=5)
        
        self.navRoot = ctk.CTkFrame(window,fg_color=self.frame_color,height=1000,width=300)
        self.navRoot.place(x=-300,y=0)


        
        self.channel_btn = ctk.CTkButton(self.navRoot,fg_color=self.frame_color,
        text="Streamer",hover_color="green",font=("opensans",30),command=self.change_streamer)
        self.channel_btn.place(x=50,y=50)

        self.exit_btn = ctk.CTkButton(self.navRoot,fg_color=self.frame_color,
        text="Exit",hover_color="green",font=("opensans",30),command=lambda: sys.exit(0) )
        self.exit_btn.place(x=50,y=100)

        self.settings_btn = ctk.CTkButton(self.navRoot,fg_color=self.frame_color,
        text="Settings",hover_color="green",font=("opensans",30),command=lambda: sys.exit(0) )
        self.settings_btn.place(x=50,y=150)

        self.navBar_close = ctk.CTkButton(self.navRoot,text="",image=self.close_icon,
        fg_color=self.frame_color,hover_color=self.frame_color,command=self.switch)
        self.navBar_close.place(x=200,y=10)



        self.chat_thread = None


    
    def stop_chat(self):
        if self.chat_thread and self.chat_thread.is_alive():
            stop_event.set()
            self.chat_thread.join()

    def switch_streamer(self):
        
        self.submit_btn.configure(state="disabled")
        new_channel = self.channel_var.get()
        self.streamer = new_channel

        self.textbox.delete("0.0","end")

        proc = multiprocessing.Process(target=run_chat,args=(self.streamer))

        #self.stop_chat()
        #self.start_chat(self.streamer)



        self.frame.place_forget()
        print(self.channel_var.get())

    def stop_and_restart_chat(self,new_channel):
        
        try:
            stop_chat()
            self.start_chat(new_channel)
        except Exception as e:
            print(e)
        

    def start_chat(self,channel):
        print(f"Starte neuen Chat für {channel}")
        self.chat_thread = threading.Thread(target=run_chat,args=(channel,),daemon=True)
        self.chat_thread.start()
    
    def change_streamer(self):
        self.frame = ctk.CTkFrame(self.window,width=500,height=500,)
        self.frame.place(x=200,y=100)
        self.channel_var = tk.StringVar()
        self.channel_name = ctk.CTkEntry(self.frame,font=("opensans",30),width=200,height=30,
        textvariable=self.channel_var)
        self.channel_name.place(x=180,y=250)

        self.submit_btn = ctk.CTkButton(self.frame,font=("opensans",30),text="Submit"
        ,command=self.switch_streamer)
        self.submit_btn.place(x=180,y=300)

        ctk.CTkButton(self.frame,text="",image=self.close_icon,
        fg_color=self.frame.cget("fg_color")
       ,hover_color=self.frame.cget("fg_color"),
        command=lambda: self.frame.place_forget()).place(x=400,y=0)


        self.channel_name.configure(state="normal")


    def switch(self):
        if self.btnState :
            for x in range(301):
                self.navRoot.place(x=-x,y=0)
                self.topFrame.update()

            self.topFrame.configure(fg_color="grey17")
            self.window.configure(fg_color="grey17")
            
            self.btnState = False
        else:
            self.topFrame.configure(fg_color="grey17")
            self.window.configure(fg_color="grey17")

            for x in range(-300,0):
                self.navRoot.place(x=x,y=0)
                self.topFrame.update()
            
            self.btnState = True


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat")
        self.geometry("800x710")

        self.minsize(800,710)
        self.maxsize(1920,1080)
        
        self.channel_name = channel
        self.streamer = []

        self.farben = random.choice(["blue","yellow"])

        


        self.fg_colors = ["#7cafc4","#edd892","#4c9f70"]

        self.textbox = ctk.CTkTextbox(self,width=1920,height=1080,
        font=("opensans",20),text_color="white",)
        self.textbox.place(x=0,y=50)
        self.textbox.insert("end","Chat Nachrichten werden generiert ... \n")

        # nametag farbe ändern mit tag funktion
        self.textbox.tag_config("name_tag", foreground=random.choice(self.fg_colors), )
        self.textbox.tag_config("content_tag", foreground="white", )

        if "Chat Nachrichten werden generiert ..." in self.textbox.get("1.0","end"):
                    self.textbox.configure(text_color="#edd892")
        
        self.update_chat()
        self.n = NavBar(self,self.textbox,self.streamer)

        self.mainloop()



    def update_chat(self):
        try:
            
            while not chat_queue.empty():
                msg = chat_queue.get()
                
                self.textbox.configure(state="normal")
                name,content = msg.split(":",1)
                self.textbox.insert("end",f"{name}: ","name_tag")
                self.textbox.insert("end",f"{content} \n","content_tag")

                self.textbox.yview("end")

                self.textbox.configure(state="disabled")
            self.after(100,self.update_chat)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    #run_window()
    App()
