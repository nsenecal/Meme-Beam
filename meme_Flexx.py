import socket, time
from config import DELAY, CHANNEL, ALERT_SOUND, ALERT_RUMBLE
from alerts import sound, rumble
from common import window

import requests
import PIL
from PIL import Image
import threading
from flexx import flx


sock = socket.socket()
sock.connect(('irc.chat.twitch.tv', 6667))
sock.send(f"NICK justinfan0\n".encode('utf-8'))
sock.send(f"JOIN {CHANNEL}\n".encode('utf-8'))

lastAlert = 0

Image = [None,False]
que = []


def getimage(link):  # Deals with retrieving the image file and writing it
    response = requests.get(link).content
    try:
        file = open(r"images/staging.png", "wb")
    except:
        print("File error")
        file = Image.open(r"images/error.png")
        scaled = int(500 * (file.size[1] / file.size[0]))
        file = file.resize((500, scaled), PIL.Image.ANTIALIAS)
        file.save(r"images/meme.png")
    else:
        file = open(r"images/staging.png", "wb")
        file.write(response)
        file.close()

        file = Image.open(r"images/staging.png")
        scaled = int(500 * (file.size[1] / file.size[0]))
        file = file.resize((500, scaled), PIL.Image.ANTIALIAS)
        file.save(r"images/meme.png")
    que.remove(link)


def parsechat(self):
    resp = self.rstrip().split('\r\n')
    for line in resp:
        if "PRIVMSG" in line:
            user = line.split(':')[1].split('!')[0]
            msg = line.split(':', maxsplit=2)[2]
            line = user + ": " + msg
            if msg.split(" ")[0] == "!meme":  # detects command for image
                image = msg.split(" ")[1]
                que.append(str(image))
        print(line)
        print(que)


class Thread(object):

    def __init__(self):

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Execute

    def run(self):
        # Forever loop that monitors chat. Hopefully stable?
        while True:
            global Image
            if Image[1] == True:
                print("ech")

            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            elif len(resp) > 0:
                parsechat(resp)
                global lastAlert
                if not window.foreground() and time.time() - lastAlert > DELAY:
                    if ALERT_SOUND: sound.alert()
                    if ALERT_RUMBLE: rumble.alert()
                    lastAlert = time.time()


running = Thread()

class Jank(flx.Widget):

    def init(self):
        with flx.VBox(flex=0):
            with flx.VBox(flex = 0):
                src = str(que[0])
                self.img = flx.ImageWidget(flex=0, stretch=False,source=src)
                self.img.set_minsize(500, 500)
                self.img.set_maxsize(500, 500)
            with flx.HBox(flex=1):
                self.b1 = flx.Button(text="Yes")
                self.void = flx.Label()
                self.b2 = flx.Button(text="No")
                self.b1.set_maxsize(40, 40)
                self.b2.set_maxsize(40, 40)
                self.void.set_maxsize(420, 40)

    @flx.reaction("b1.pointer_click")
    def b1_clicked(self, *events):
        global Image
        Image[1] = True

    @flx.reaction("b2.pointer_click")
    def b2_clicked(self, *events):
        print("no")
        global Image
        print(Image[1])

if __name__ == '__main__':
    m = flx.launch(Jank, "app", title="Meme-Beam", size=(510, 540))
    flx.run()
