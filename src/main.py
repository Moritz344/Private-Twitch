import customtkinter as ctk
import sys
import random
from customtkinter import *
from twitchio.ext import commands
import os
from dotenv import load_dotenv
from chat import *
import asyncio
from tkinter import *
import tkinter as tk
from PIL import Image,ImageTk
from CTkToolTip import *
import json
from settings import *
from CTkSpinbox import *
from datetime import datetime

# BESCHREIBUNG: Chat Nachrichten und gui laufen gleichzeitg mit threads 
# BESCHREIBUNG: Mit queue die chat nachrichten an main senden





class NavBar(object):
    def __init__(self,window,textbox,streamer,cat_img,cat_label):
        
        self.btnState = False
        self.nav_icon = ctk.CTkImage(Image.open("assets/menu.png"),size=(30,30))
        self.close_icon = ctk.CTkImage(Image.open("assets/close.png"),size=(40,40))
        self.bot_icon = ctk.CTkImage(Image.open("assets/bot.png"),size=(120,80))

        self.textbox = textbox
        self.streamer_liste = (list(streamer))
        self.cat_img = cat_img
        self.cat_label = cat_label

        self.background_color = "#282828"
        self.panels_color = "#3c3836"
        self.hover_color = "#665c54"
        self.text_color = "#edd892"
        
        self.window = window
        self.frame_color = "#333333"
        
        self.topFrame = ctk.CTkFrame(window,fg_color=self.panels_color,height=50,width=1920,corner_radius=0)
        self.topFrame.pack(padx=0,pady=0,side="top",)

        self.navbarBtn = ctk.CTkButton(self.topFrame,text="",
        image=self.nav_icon,hover_color=self.panels_color,fg_color=self.panels_color,
        command=self.switch)

        self.navbarBtn.place(x=-45,y=5)
        
        self.navRoot = ctk.CTkFrame(window,fg_color=self.frame_color,height=1000,width=300)
        self.navRoot.place(x=-300,y=0)
        

        
        self.channel_btn = ctk.CTkButton(self.navRoot,fg_color=self.frame_color,
        text="Streamer",hover_color=self.hover_color,text_color=self.text_color,font=("opensans",40),command=self.change_streamer)
        self.channel_btn.place(x=50,y=200)

        self.about_btn = ctk.CTkButton(self.navRoot,fg_color=self.frame_color,
        text="About",hover_color=self.hover_color,text_color=self.text_color,font=("opensans",40)
        ,command=self.about_window)
        self.about_btn.place(x=42,y=300)

        self.settings_btn = ctk.CTkButton(self.navRoot,fg_color=self.frame_color,
        text="Settings",hover_color=self.hover_color,width=0,text_color=self.text_color,font=("opensans",40),
        command=self.settings_window)
        self.settings_btn.place(x=50,y=250)

        self.exit_btn = ctk.CTkButton(self.navRoot,fg_color=self.frame_color,
        text="Exit",hover_color=self.hover_color,text_color=self.text_color,font=("opensans",40),command=lambda: sys.exit(0) ,
        width=0)
        self.exit_btn.place(x=49,y=350)



        self.navBar_close = ctk.CTkButton(self.navRoot,text="",image=self.close_icon,
        fg_color=self.frame_color,hover_color=self.frame_color,command=self.switch)
        self.navBar_close.place(x=200,y=14)


        ctk.CTkLabel(self.navRoot,fg_color=self.frame_color,text="Private Twitch",text_color="white",
        font=("opensans",30)).place(x=35,y=20)

        self.chat_thread = None
        self.streamer_on = False

    
    def about_window(self):
        window = ctk.CTkToplevel()
        window.title("About")
        window.geometry("700x300")
        window.minsize(700,300)
        window.maxsize(700,300)
        label_text = """
This is the gui form of my cli twitch chat app.
If you need help contact me on my 
github.com/Moritz344/Private-Twitch.
Keep in mind this is my private tool 
for my twitch chat so don't expect to much.
        """
        #ctk.CTkLabel(window,text=label_text,text_color="white",font=("opensans",20)).place(x=70,y=100)
        ctk.CTkLabel(window,text="About",text_color=self.text_color,font=("opensans",60)).place(x=12,y=10)

        text_label = ctk.CTkTextbox(window,text_color="white",font=("",20),width=600,height=200)
        text_label.place(x=10,y=80)
        text_label.insert("end",label_text)
        text_label.configure(state="disabled")
    
    def settings_window(self):
        window = ctk.CTkToplevel()
        window.title("Settings")
        window.geometry("500x600")
        window.minsize(500,600)
        window.maxsize(500,600)


        # font größe ändern


        def write_token():
            load_dotenv("secret.env")
            TOKEN=os.getenv("TOKEN")
            self.token_input.insert("end",f"{TOKEN}")
        
        def no_focus_entry(event=None):
            window.focus_set()

            # save access token in .env file
            with open("secret.env","w") as env_file:
                env_file.write(f"TOKEN={self.token_input.get()}")

        def write_preferences_to_json(main,key,new_value):
            try:
                # get the content of the file
                with open("data.json","r") as file:
                    content = json.load(file)

                if main in content:
                    # z.b: content["preferences"]["font"] = "Arial"
                    content[main][key] = new_value



                with open("data.json","w") as file:
                    # aktualisiere json file
                    json.dump(content,file,indent=4)

            except Exception as e:
                print(e)

        def change_border_spacing(value):
            write_preferences_to_json("settings","borderSpacing",value)
        def change_font_size(v):
            write_preferences_to_json("settings","font_size",v)
        def colorscheme_title(choice):
            write_preferences_to_json("settings","colorscheme",choice)

        # border spacing,font
        
        bot_img = ctk.CTkLabel(window,text="",image=self.bot_icon)
        bot_img.place(x=30,y=20)

        label_1 = ctk.CTkLabel(window,text="ACCESS TOKEN",font=("opensans",30),
        text_color=self.text_color)
        label_1.place(x=135,y=50)

        ctk.CTkLabel(window,text="BORDER SPACING",text_color=self.text_color,
        font=("opensans",30)).place(x=120,y=306)

        spacing_box = CTkSpinbox(window,start_value=0,max_value=50,step_value=2,min_value=0,
        command=change_border_spacing)
        spacing_box.place(x=190,y=355)

        spacing_box.set(borderSpacing)

        tooltip_1 = CTkToolTip(label_1,delay=0.3,message="Get your token at: https://twitchtokengenerator.com/")
        tooltip_2 = CTkToolTip(bot_img,delay=0.3,message="Get your token at: https://twitchtokengenerator.com/")

        self.token_input = ctk.CTkEntry(window,placeholder_text="oauth:129dfsd95394",show="*",
        fg_color=self.background_color,
        width=200,height=40,font=("opensans",30))
        self.token_input.pack(padx=50,pady=100)

        
        ctk.CTkLabel(window,text="COLORSCHEMES",
        font=("opensans",30),text_color=self.text_color).place(x=125,y=200)
        
        text_color_list = ["coffeine","lavender","quiet"]

        self.optionmenu_1 = ctk.CTkOptionMenu(window,width=240,
        values=text_color_list,fg_color=self.background_color,button_color="#458588",
        button_hover_color=self.hover_color,command=colorscheme_title)
        
        ctk.CTkLabel(window,text="FONT SIZE",font=("",30),text_color=self.text_color).place(x=170,y=450)
        self.spinbox_2 = CTkSpinbox(window,max_value=50,start_value=30,min_value=0,
        command=change_font_size)
        self.spinbox_2.set(font_size)
        self.spinbox_2.place(x=190,y=500)
        

        self.optionmenu_1.set(colorscheme)
        self.optionmenu_1.place(x=135,y=250)
        
        write_token()

        window.bind("<Return>",no_focus_entry)
        window.bind("<Escape>",no_focus_entry)


        window.mainloop()
    def stop_chat(self):
        if self.chat_thread and self.chat_thread.is_alive():
            stop_event.set()
            self.chat_thread.join()

    def switch_streamer(self):
        
        #self.submit_btn.configure(state="disabled")
        new_channel = self.channel_var.get()
        self.streamer = new_channel

        self.textbox.delete("0.0","end")
        self.cat_label.place_forget()

        try:
            if not self.streamer_on:
                self.streamer_on = True
                self.start_chat(self.streamer)
        except Exception as e:
            print("ai can't solve this one for sure",e) 



        self.frame.place_forget()
        print(self.channel_var.get())

    def stop_and_restart_chat(self,new_channel):
        
        try:
            stop_chat()
            self.start_chat(new_channel)
        except Exception as e:
            print(e)
        

    def start_chat(self,channel,):
        print(f"Starte neuen Chat für {channel}")
        self.chat_thread = threading.Thread(target=run_chat,args=(channel,self.window),daemon=True)
        self.chat_thread.start()
    
    def change_streamer(self):
        self.frame = ctk.CTkFrame(self.window,width=500,height=500,)
        self.frame.place(x=200,y=100)


        self.channel_var = tk.StringVar()
        self.channel_name = ctk.CTkEntry(self.frame,font=("opensans",30),width=300,height=50,
        textvariable=self.channel_var)
        self.channel_name.place(x=100,y=200)

        self.submit_btn = ctk.CTkButton(self.frame,font=("opensans",30),text="Submit"
        ,command=self.switch_streamer,text_color=self.text_color,hover_color=self.hover_color,fg_color=self.background_color)
        self.submit_btn.place(x=100,y=300)

        self.cancel_btn = ctk.CTkButton(self.frame,font=("opensans",30),text="Cancel"
        ,command=lambda: self.frame.place_forget(),text_color=self.text_color,hover_color=self.hover_color,
        fg_color=self.background_color)
        self.cancel_btn.place(x=260,y=300)

        ctk.CTkLabel(self.frame,font=("opensans",40),text="Add a Streamer ...").place(x=110,y=100)

        ctk.CTkButton(self.frame,text="",image=self.close_icon,
        fg_color=self.frame.cget("fg_color")
       ,hover_color=self.frame.cget("fg_color"),
        command=lambda: self.frame.place_forget()).place(x=400,y=0)


        self.channel_name.configure(state="normal")


    def switch(self):
        if self.btnState :
            for x in range(300):
                self.navRoot.place(x=-x * 2,y=0)
                self.topFrame.update()

            self.topFrame.configure(fg_color=self.panels_color)
            self.window.configure(fg_color=self.background_color)
            
            self.btnState = False
        else:
            # ÖFFNEN
            self.topFrame.configure(fg_color=self.panels_color)
            self.window.configure(fg_color=self.background_color)

            for x in range(-300,0):
                self.navRoot.place(x=x * 4,y=0)
                self.topFrame.update()
            
            self.btnState = True


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.channel_name = channel
        self.title(f"Reading someones's chat")
        self.geometry("800x750")

        self.minsize(800,750)
        self.maxsize(800,750)
        
        self.streamer = []



        self.fg_color = "#edd892"
        self.random_color = ["red","blue"]

        self.textbox = ctk.CTkTextbox(self,width=800,height=710,
        font=("opensans",20),text_color="white",border_spacing=borderSpacing,fg_color="#2a2b2a",activate_scrollbars=True)
        self.textbox.place(x=0,y=50)
        self.textbox.insert("end","No Streamer added yet :/ \n")
        self.textbox.insert("end","----------------------------\n")
        self.textbox.insert("end","If you see no messages being generated\n")
        self.textbox.insert("end","check If you saved your acces token in the settings window\n")
        

        # nametag farbe ändern mit tag funktion

        self.textbox.tag_config("content_tag", foreground="white", )
        self.textbox.tag_config("date_tag", foreground="white", )

        if "No Streamer added yet " in self.textbox.get("1.0","end"):
                    self.textbox.configure(text_color="#edd892")
        
        self.update_chat()

        self.cat_img = ctk.CTkImage(Image.open("assets/play.png"),size=(100,100))
        self.cat_label = ctk.CTkLabel(self,text="",fg_color="#2a2b2a",image=self.cat_img)
        self.cat_label.place(x=300,y=300)

        NavBar(self,self.textbox,self.streamer,self.cat_img,self.cat_label)


        self.mainloop()


    def move_textbox(self):
        self.textbox.yview_moveto(1.0)

    def update_chat(self):
        try:
            
            while not chat_queue.empty():
                msg = chat_queue.get()
                
                self.datetime = datetime.now().strftime("%H:%M")
                self.textbox.configure(state="normal")
                name,content = msg.split(":",1)
                
                
                def update_textbox():
                    self.textbox.configure(
                    border_spacing=borderSpacing,font=("opensans",font_size))
                update_textbox()
                self.name_tag = f"name_{name}_{random.randint(1, 10000)}"
                def colorscheme_func(colorscheme):
                    # Verschiedene colorschemes 

                    if colorscheme == "Standard" or colorscheme == "coffeine":
                        self.color = random.choice(coffeine)
                        self.textbox.tag_config(self.name_tag, foreground=self.color, )
                    elif colorscheme == "lavender":
                        self.color = random.choice(lavender)
                        self.textbox.tag_config(self.name_tag,foreground=self.color)
                    elif colorscheme == "quiet":
                        self.color = random.choice(quiet)
                        self.textbox.tag_config(self.name_tag,foreground=self.color)
                        
                colorscheme_func(colorscheme)
                self.textbox.insert("end",f"[{self.datetime}] ","date_tag")
                self.textbox.insert("end",f"{name}: ",self.name_tag)
                self.textbox.insert("end",f"{content} \n","content_tag")

                self.textbox.configure(state="disabled")
            
            self.after(10, lambda: self.move_textbox())
            self.after(100,self.update_chat)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    App()
