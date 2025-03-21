from twitchio.ext import commands
import os 
from dotenv import load_dotenv
import threading
import asyncio
import queue
from main import *
from main import NavBar
from termcolor import cprint,colored
from customtkinter import *
import customtkinter as ctk

load_dotenv("secret.env")
Twitch_token = os.getenv("TOKEN")
channel = "ohnePixel"

chat_queue = queue.Queue()
stop_event = threading.Event()

class Chat(commands.Bot):
    def __init__(self,channel):
        super().__init__(token=Twitch_token,msg="",prefix=None,initial_channels=[channel])

        self.channel = channel
       
    async def event_ready(self):
        print(self.nick,channel)
    async def event_message(self,message):
        try:
            chat_message = f"{message.author.name}: {message.content}"
            chat_queue.put(chat_message)
        except Exception as e:
            print(e)



def run_chat(channel):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = Chat(channel)
    loop.run_until_complete(bot.run())

def stop_chat():
    print("Stopping chat ...")
    stop_event.set()

if __name__ == "__main__":
    run_chat(channel)
