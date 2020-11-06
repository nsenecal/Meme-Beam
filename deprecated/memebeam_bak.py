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

import socket, time
from alerts import sound, rumble
from common import window
#from config import DELAY, CHANNEL, ALERT_SOUND, ALERT_RUMBLE, AUTHKEY, INPUT, OUTPUT, SOUND_FILE

def update():
    config = configparser.ConfigParser()
    config.read('config.ini')

    global CHANNEL, AUTHKEY, INPUT, OUTPUT, DELAY, SOUND_FILE, ALERT_SOUND, WIDTH, ALERT_RUMBLE, ALERT_IMAGE, IMAGE_SOUND, INIT, CHAT_ENABLED

    CHANNEL = config['settings']['CHANNEL'] #Twitch Channel
    AUTHKEY = config['settings']['AUTHKEY'] #Discord App Auth
    INPUT = config['settings']['INPUT'] #Viewer Discord Channel
    OUTPUT = config['settings']['OUTPUT'] #Streamer Discord Channel
    DELAY = int(config['settings']['DELAY']) #Delay in seconds
    SOUND_FILE = config['settings']['SOUND_FILE'] #Path the chat alert
    ALERT_SOUND = config['settings']['ALERT_SOUND'] #Enable/Disable Chat Notifications
    WIDTH = int(config['settings']['WIDTH']) #scaled width of image

    ALERT_RUMBLE = config['settings']['ALERT_RUMBLE'] #rumble
    ALERT_IMAGE = config['settings']['ALERT_IMAGE'] #Path to image alert
    IMAGE_SOUND = config['settings']['IMAGE_SOUND'] #Path to image alert
    INIT = config['settings']['INIT'] #Run on startup
    CHAT_ENABLED = config['settings']['CHAT_ENABLED'] #Enable/Disable Chat

update()

sock = socket.socket()
sock.connect(('irc.chat.twitch.tv', 6667))
sock.send(f"NICK justinfan0\n".encode('utf-8'))
sock.send(f"JOIN {'#'+CHANNEL}\n".encode('utf-8'))

lastAlert = 0
channel = None
channel2 = None
client = discord.Client()

ping = []


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

    for guild in client.guilds:
        for channels in guild.channels:
            global channel
            global channel2
            channel = get(guild.channels, name=INPUT, type=discord.ChannelType.text).id
            channel2 = get(guild.channels, name=OUTPUT, type=discord.ChannelType.text).id
    channel = client.get_channel(channel)
    channel2 = client.get_channel(channel2)

    print("Back Online! 💪")


async def chat():
    while True:
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
                #gooey here


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


client.loop.create_task(chat())
thread = threading.Thread(target=loop)
thread.start()
client.run(AUTHKEY)
