import discord
from discord import client
from discord.utils import get
from PIL import Image
import requests
from io import BytesIO
import threading
import asyncio
import os
import configparser
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import socket, time
from alerts import sound, rumble
from common import window

config = configparser.ConfigParser()
sock = socket.socket()
sock.connect(('irc.chat.twitch.tv', 6667))
sock.send(f"NICK justinfan0\n".encode('utf-8'))
client = discord.Client()


def update():
    config.read('config.ini')

    global CHANNEL, AUTHKEY, INPUT, OUTPUT, DELAY, SOUND_FILE, ALERT_SOUND, WIDTH, ALERT_RUMBLE, ALERT_IMAGE, IMAGE_SOUND, CHAT_ENABLED

    AUTHKEY = config['settings']['AUTHKEY']  # Discord App Auth
    INPUT = config['settings']['INPUT']  # Viewer Discord Channel
    OUTPUT = config['settings']['OUTPUT']  # Streamer Discord Channel

    try:
        int(config['settings']['DELAY'])
    except ValueError:
        DELAY = 10
    else:
        DELAY = int(config['settings']['DELAY'])  # Delay in seconds

    try:
        int(config['settings']['WIDTH'])
    except ValueError:
        WIDTH = 200
    else:
        WIDTH = int(config['settings']['WIDTH'])  # scaled width of image

    SOUND_FILE = config['settings']['SOUND_FILE']  # Path the chat alert
    CHANNEL = config['settings']['CHANNEL']  # Twitch Channel
    IMAGE_SOUND = config['settings']['IMAGE_SOUND']  # Path to image alert
    CHAT_ENABLED = config['settings']['CHAT_ENABLED']  # Enable/Disable Chat
    ALERT_SOUND = config['settings']['ALERT_SOUND']  # Enable/Disable Chat Notifications
    ALERT_RUMBLE = config['settings']['ALERT_RUMBLE']  # rumble
    ALERT_IMAGE = config['settings']['ALERT_IMAGE']  # Enable/Disable Image Notifications

    sock.send(f"JOIN {'#' + CHANNEL}\n".encode('utf-8'))
    global pook
    pook = True


update()


lastAlert = 0
channel = None
channel2 = None
ping = []


class Gui:
    def __init__(self, master=None):
        self.master = master
        master.title("Meme-Beam Settings [Bot Offline]")
        master.resizable(False, False)
        master.iconbitmap(r"images/lazer.ico")

        config.read('config.ini')

        CHANNEL = config['settings']['CHANNEL']
        AUTHKEY = config['settings']['AUTHKEY']
        INPUT = config['settings']['INPUT']
        OUTPUT = config['settings']['OUTPUT']
        DELAY = config['settings']['DELAY']
        ALERT_SOUND = config['settings']['ALERT_SOUND']
        ALERT_RUMBLE = config['settings']['ALERT_RUMBLE']
        ALERT_IMAGE = config['settings']['ALERT_IMAGE']
        SOUND_FILE = config['settings']['SOUND_FILE']
        IMAGE_SOUND = config['settings']['IMAGE_SOUND']
        WIDTH = config['settings']['WIDTH']
        CHAT_ENABLED = config['settings']['CHAT_ENABLED']

        def chatfile():
            self.master.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=[("Wav files","*.wav")])
            sound2.delete(0, 'end')
            sound2.insert(1, self.master.filename)
            sound2.xview('end')

        def imgfile():
            self.master.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=[("Wav files","*.wav")])
            alt2.delete(0, 'end')
            alt2.insert(1, self.master.filename)
            alt2.xview('end')

        def save():
            config['settings']['CHANNEL'] = twitch2.get()
            config['settings']['AUTHKEY'] = discord2.get()
            config['settings']['INPUT'] = input2.get()
            config['settings']['OUTPUT'] = output2.get()
            config['settings']['DELAY'] = ping2.get()
            config['settings']['ALERT_SOUND'] = sound4.var.get()
            config['settings']['ALERT_RUMBLE'] = alert.var.get()
            config['settings']['ALERT_IMAGE'] = alt4.var.get()
            config['settings']['SOUND_FILE'] = sound2.get()
            config['settings']['IMAGE_SOUND'] = alt2.get()
            config['settings']['WIDTH'] = width2.get()
            config['settings']['CHAT_ENABLED'] = chat.var.get()
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            update()

        input1 = tk.Label(master, text="Viewer Channel:")
        input1.grid(row=1, column=1)
        input2 = tk.Entry(master)
        input2.grid(row=1, column=2)
        input2.insert(0, INPUT)
        output = tk.Label(master, text="Streamer Channel:")
        output.grid(row=1, column=3)
        output2 = tk.Entry(master)
        output2.grid(row=1, column=4)
        output2.insert(0, OUTPUT)

        twitch = tk.Label(master, text="Twitch Channel:")
        twitch.grid(row=2, column=1)
        twitch2 = tk.Entry(master)
        twitch2.grid(row=2, column=2)
        twitch2.insert(0, CHANNEL)
        discord = tk.Label(master, text="Discord Auth:")
        discord.grid(row=2, column=3)
        discord2 = tk.Entry(master)
        discord2.grid(row=2, column=4)
        discord2.insert(0, AUTHKEY)

        ping = tk.Label(master, text="Notification Delay (s):")
        ping.grid(row=3, column=1)
        ping2 = tk.Entry(master)
        ping2.grid(row=3, column=2)
        ping2.insert(0, DELAY)
        width = tk.Label(master, text="Image Width (pix):")
        width.grid(row=3, column=3)
        width2 = tk.Entry(master)
        width2.grid(row=3, column=4)
        width2.insert(0, WIDTH)

        sound = tk.Label(master, text="Chat Alert:")
        sound.grid(row=4, column=1)
        sound2 = tk.Entry(master)
        sound2.grid(row=4, column=2)
        sound2.insert(1, SOUND_FILE)
        sound2.xview('end')
        sound3 = tk.Button(master, text="Open File", command=chatfile)
        sound3.grid(row=4, column=3)
        sound4 = tk.Checkbutton(master, text="Enabled", onvalue="True", offvalue="False")
        sound4.var = tk.StringVar(value=ALERT_SOUND)
        sound4.config(var=sound4.var)
        sound4.grid(row=4, column=4)

        alt = tk.Label(master, text="Image Alert:")
        alt.grid(row=5, column=1)
        alt2 = tk.Entry(master)
        alt2.grid(row=5, column=2)
        alt2.insert(0, IMAGE_SOUND)
        alt3 = tk.Button(master, text="Open File", command=imgfile)
        alt3.grid(row=5, column=3)
        alt4 = tk.Checkbutton(master, text="Enabled", onvalue="True", offvalue="False")
        alt4.var = tk.StringVar(value=ALERT_IMAGE)
        alt4.config(var=alt4.var)
        alt4.grid(row=5, column=4)

        alert = tk.Checkbutton(master, text="Rumble", onvalue="True", offvalue="False")
        alert.var = tk.StringVar(value=ALERT_RUMBLE)
        alert.config(var=alert.var)
        alert.grid(row=10, column=1)
        chat = tk.Checkbutton(master, text="Chat Enabled", onvalue="True", offvalue="False")
        chat.var = tk.StringVar(value=CHAT_ENABLED)
        chat.config(var=chat.var)
        chat.grid(row=10, column=2)
        #startup = tk.Checkbutton(master, text="Run on Startup", onvalue="True", offvalue="False")
        #startup.grid(row=10, column=3)
        #startup.var = tk.StringVar(value=INIT)
        #startup.config(var=startup.var)
        apply = tk.Button(master, text="Apply All Changes", command=save)
        apply.grid(row=10, column=4)


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

    try:
        for guild in client.guilds:
            for channels in guild.channels:
                global channel
                global channel2
                channel = get(guild.channels, name=INPUT, type=discord.ChannelType.text).id
                channel2 = get(guild.channels, name=OUTPUT, type=discord.ChannelType.text).id
        channel = client.get_channel(channel)
        channel2 = client.get_channel(channel2)
    except AttributeError:
        await client.logout()
        print("Bot Offline")
        root.title("Meme-Beam Settings [Settings Error]")
    else:
        print("Back Online! 💪")
        root.title("Meme-Beam Settings [Bot Online]")

pook = False

async def chat():
    while True:
        if pook is True:
            await client.logout()
        if len(ping) > 0:
            global channel2
            try:
                await channel2.send(ping[0])
                ping.pop(0)
            except:
                pass
            else:
                pass
        await asyncio.sleep(0.01)


@client.event
async def on_raw_reaction_add(reaction):
    if reaction.user_id != 771424434387943424:
        msg = await channel2.fetch_message(reaction.message_id)
        if reaction.emoji.name == "✅":
            raw = msg.attachments[0].url
            response = requests.get(raw)
            img = Image.open(BytesIO(response.content))
            scaled = int(WIDTH * (img.size[1] / img.size[0]))
            img = [img.resize((WIDTH, scaled), Image.ANTIALIAS)]
            img[0].save(r"images/meme.gif", format="GIF", append_images=img[1:], save_all=True, duration=100, oop=100)
        elif reaction.emoji.name == "❌":
            await msg.delete()
        elif reaction.emoji.name == "🚫":
            os.remove(r"images/meme.gif")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        if message.channel == channel:
            try:
                await message.attachments[0].save(r"images/staging.gif")
                await message.delete()
                oof = await channel2.send(content=str(message.author), file=discord.File(r"images/staging.gif"))
                await oof.add_reaction("✅")
                await oof.add_reaction("❌")
            except IndexError:
                await message.delete()
                # oof = await channel2.send(file=discord.File(r"images/staging.gif"))
                # await oof.add_reaction("✅")
                # await oof.add_reaction("❌")
            else:
                pass
        elif message.channel == channel2:
            if message.content == "!Clear":
                os.remove(r"images/meme.gif")
            elif message.content == "!settings":
                pass


def parseChat(resp):
    resp = resp.rstrip().split('\r\n')
    for line in resp:
        if "PRIVMSG" in line:
            user = line.split(':')[1].split('!')[0]
            msg = line.split(':', maxsplit=2)[2]
            line = "**" + user + "**" + ": " + msg
            ping.append(line)


def loop():
    while True:

        global lastAlert
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            parseChat(resp)
            if not window.foreground() and time.time() - lastAlert > DELAY:
                if ALERT_SOUND == "True": sound.alert(SOUND_FILE)
                if ALERT_RUMBLE == "True": rumble.alert()
                lastAlert = time.time()


def abandon():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        os._exit(0)


def run():
    try:
        client.run(AUTHKEY)
    except discord.errors.LoginFailure:
        print("Invalid Auth Key")
    else:
        pass


client.loop.create_task(chat())
thread = threading.Thread(target=loop)
thread2 = threading.Thread(target=run)
thread.start()
thread2.start()

root = tk.Tk()
Gui(root)
root.protocol("WM_DELETE_WINDOW", abandon)
root.mainloop()

