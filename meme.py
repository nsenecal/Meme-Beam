import socket, time
from config import DELAY, CHANNEL, ALERT_SOUND, ALERT_RUMBLE
from alerts import sound, rumble
from common import window

from ppadb.client import Client as AdbClient
import requests

sock = socket.socket()
sock.connect(('irc.chat.twitch.tv',6667))
sock.send(f"NICK justinfan0\n".encode('utf-8'))
sock.send(f"JOIN {CHANNEL}\n".encode('utf-8'))

lastAlert = 0

def getImage(link): #Deals with retrieving the image file and writing it
    response = requests.get(str(link))
    file = open("images/meme.png", "wb")
    file.write(response.content)
    file.close()

def parseChat(resp):
    resp = resp.rstrip().split('\r\n')
    for line in resp:
        if "PRIVMSG" in line:
            user = line.split(':')[1].split('!')[0]
            msg = line.split(':', maxsplit=2)[2]
            line = user + ": " + msg
            if msg.split(" ")[0] == "!meme": #detects command for image
                image = msg.split(" ")[1]
                getImage(image)
        print(line)

while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    elif len(resp) > 0:
        parseChat(resp)
        if not window.foreground() and time.time() - lastAlert > DELAY:
            if ALERT_SOUND: sound.alert()
            if ALERT_RUMBLE: rumble.alert()
            lastAlert = time.time()
