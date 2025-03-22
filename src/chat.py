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
import multiprocessing

load_dotenv("secret.env")
Twitch_token = os.getenv("TOKEN")

channel = "ohnePixel"

chat_queue = queue.Queue()
stop_event = multiprocessing.Event()
chat_process = None

class Chat(commands.Bot):
    def __init__(self,channel):
        try:
            super().__init__(token=Twitch_token,msg="",prefix=None,initial_channels=[channel])

            self.channel = channel
        except Exception:
            print("Vermutlich weil kein ACCESS TOKEN eingegeben wurde.")
       
    async def event_ready(self):
        print(self.nick,channel)
    async def event_message(self,message):
        try:
            chat_message = f"{message.author.name}: {message.content}"
            chat_queue.put(chat_message)
        except Exception as e:
            print(e)



def run_chat(channel):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot = Chat(channel)
        loop.run_until_complete(bot.run())
    except Exception:
        print("Vermutlich weil kein ACCESS TOKEN eingegeben wurde.")

def stop_chat():
    print("Stopping chat ...")
    stop_event.set()


if __name__ == "__main__":
    try:
        run_chat(channel)
    except Exception:
        print("kxdmdxgmxgm")
