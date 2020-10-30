import discord
from discord import client
from discord.utils import get
from PIL import Image
import requests
from io import BytesIO

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        name = input("Enter a channel name: ")
        for guild in client.guilds:
            for channels in guild.channels:
                channel = get(guild.channels, name=name, type=discord.ChannelType.text)
        await channel.send('test')

    async def on_message(self, message):
        if message.author == client.user:
            return
        else:

            try:
                raw = message.attachments[0].url
                response = requests.get(raw)
                img = Image.open(BytesIO(response.content))
            except IndexError:
                try:
                    response = requests.get(message.content)
                    file = open(r"images/meme.gif", "wb")
                    file.write(response.content)
                    file.close()
                except:
                    await channel.send("Not an image, smoothbrain")
            else:
                await channel.send("nice" + " " + str(img.format))
                if str(img.format) != "GIF":
                    img = Image.open(BytesIO(response.content))
                    scaled = int(400 * (img.size[1] / img.size[0]))
                    img = [img.resize((400, scaled), Image.ANTIALIAS)]
                    img[0].save(r"images/meme.gif", format="GIF", append_images=img[1:], save_all=True, duration=100,loop=0)
                else:
                    file = open(r"images/staging.gif", "wb")
                    file.write(response.content)
                    file.close()

                    file = Image.open(r"images/staging.gif")
                    scaled = int(400 * (file.size[1] / file.size[0]))
                    file = file.resize((400, scaled), Image.ANTIALIAS)
                    file.save(r"meme/meme.gif")


client = MyClient()
client.run('<auth token>')