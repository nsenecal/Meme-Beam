import socket, time
from config import DELAY, CHANNEL, ALERT_SOUND, ALERT_RUMBLE
from alerts import sound, rumble
from common import window

import requests
import PIL
from PIL import ImageTk
import tkinter as tk
import threading


sock = socket.socket()
sock.connect(('irc.chat.twitch.tv', 6667))
sock.send(f"NICK justinfan0\n".encode('utf-8'))
sock.send(f"JOIN {CHANNEL}\n".encode('utf-8'))

lastAlert = 0

current = None
que = []

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        thread = threading.Thread(target=self.loop)
        thread.daemon = True
        thread.start()

    def parsechat(self, input):

        resp = input.rstrip().split('\r\n')
        for line in resp:
            if "PRIVMSG" in line:
                user = line.split(':')[1].split('!')[0]
                msg = line.split(':', maxsplit=2)[2]
                line = user + ": " + msg
                if msg.split(" ")[0] == "!meme":  # detects command for image
                    image = msg.split(" ")[1]
                    que.append(str(image))
            print(line)

    def check(self):
        global current
        global que

        if current is None and len(que) > 0:
            self.update_preview(que[0])
            current = que[0]

    def loop(self):

        while True:

            self.check()

            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            elif len(resp) > 0:
                self.parsechat(resp)
                global lastAlert
                if not window.foreground() and time.time() - lastAlert > DELAY:
                    if ALERT_SOUND: sound.alert()
                    if ALERT_RUMBLE: rumble.alert()
                    lastAlert = time.time()

    def push(self):

        global current
        global que
        
        file = PIL.Image.open(r"images/staging.png")
        scaled = int(500 * (file.size[1] / file.size[0]))
        file = file.resize((500, scaled), PIL.Image.ANTIALIAS)
        file.save(r"images/meme.png")
        self.update_preview(None)
        que.remove(que[0])
        current = None
        self.check()

    def reject(self):

        global current
        global quew
        
        self.update_preview(None)
        que.remove(que[0])
        current = None
        self.check()

    def wipe(self):

        global current
        global que
        self.update_preview(None)
        current = None
        self.check()


    def update_preview(self, link):
        if link == None:
            self.imgLabel = self.panel
            self.imgLabel.configure(image=None)
            self.imgLabel.image = None
            self.imgLabel.pack()
        else:
            try: response = requests.get(link).content
            except:
                print("U dum")
            else:
                file = open(r"images/staging.png", "wb")
                file.write(response)
                file.close()

                file = PIL.Image.open(r"images/staging.png")
                scaled = int(200 * (file.size[1] / file.size[0]))
                file = file.resize((200, scaled), PIL.Image.ANTIALIAS)
                file.save(r"images/preview.png")
                img = ImageTk.PhotoImage(file)
                self.imgLabel = self.panel
                self.imgLabel.configure(image=img)
                self.imgLabel.image = img
                self.imgLabel.pack()
    
    def create_widgets(self):
        self.panel = tk.Label()
        self.yes = tk.Button(self, text="Yes", fg="green",command=self.push)
        self.yes.pack(side="bottom")
        self.no = tk.Button(self, text="No", fg="Red", command=self.reject)
        self.no.pack(side="bottom")
        self.clear = tk.Button(self, text="Clear", command=self.wipe)
        self.clear.pack(side="bottom")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
