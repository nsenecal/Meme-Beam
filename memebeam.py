import discord
from discord import client
from discord.utils import get
from PIL import Image
import requests
from io import BytesIO
import threading

import socket, time
from config import DELAY, CHANNEL, ALERT_SOUND, ALERT_RUMBLE, AUTHKEY, INPUT, OUTPUT
from alerts import sound, rumble
from common import window

sock = socket.socket()
sock.connect(('irc.chat.twitch.tv', 6667))
sock.send(f"NICK justinfan0\n".encode('utf-8'))
sock.send(f"JOIN {CHANNEL}\n".encode('utf-8'))

lastAlert = 0

channel = None
channel2 = None
client = discord.Client()

ping = []

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

    # name = input("Enter a channel name: ")
    name = INPUT
    name2 = OUTPUT
    for guild in client.guilds:
        for channels in guild.channels:
            global channel
            global channel2
            channel = get(guild.channels, name=name, type=discord.ChannelType.text)
            channel2 = get(guild.channels, name=name2, type=discord.ChannelType.text)
    await channel.send("Back Online! 💪")

    while True:
        if len(ping) > 0:
            await channel2.send(ping[0])
            ping.pop(0)


@client.event
async def on_raw_reaction_add(reaction):
    if reaction.user_id != 771424434387943424:
        msg = await channel2.fetch_message(reaction.message_id)
        if reaction.emoji.name == "✅":
            raw = msg.attachments[0].url
            response = requests.get(raw)
            img = Image.open(BytesIO(response.content))
            scaled = int(400 * (img.size[1] / img.size[0]))
            img = [img.resize((400, scaled), Image.ANTIALIAS)]
            img[0].save(r"images/meme.gif", format="GIF", append_images=img[1:], save_all=True, duration=100, oop=100)
        elif reaction.emoji.name == "❌":
            await msg.delete()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        if message.channel == channel:
            try:
                await message.attachments[0].save(r"images/staging.gif")
                await message.delete()
                oof = await channel2.send(file=discord.File(r"images/staging.gif"))
                await oof.add_reaction("✅")
                await oof.add_reaction("❌")
            except IndexError:
                pass
                # Dunno
                await message.delete()
                # oof = await channel2.send(file=discord.File(r"images/staging.gif"))
                # await oof.add_reaction("✅")
                # await oof.add_reaction("❌")
            else:
                pass

def parseChat(resp):
    resp = resp.rstrip().split('\r\n')
    for line in resp:
        if "PRIVMSG" in line:
            user = line.split(':')[1].split('!')[0]
            msg = line.split(':', maxsplit=2)[2]
            line = user + ": " + msg
            ping.append(line)
        print(line)


def loop(self):
    while True:
        global lastAlert
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            parseChat(resp)
            if not window.foreground() and time.time() - lastAlert > DELAY:
                if ALERT_SOUND: sound.alert()
                if ALERT_RUMBLE: rumble.alert()
                lastAlert = time.time()


thread = threading.Thread(target=loop, args=(1,))
thread.start()
client.run(AUTHKEY)
