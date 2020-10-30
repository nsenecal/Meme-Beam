import socket, time
from config import DELAY, CHANNEL, ALERT_SOUND, ALERT_RUMBLE
from alerts import sound, rumble
from common import window

#Added modules
import requests # deals with image downloads
import PIL #image manipulation
from PIL import Image, ImageTk
import tkinter as tk # GUI
import threading # multithreading
import os # odd jobs

# connect to irc
sock = socket.socket()
sock.connect(('irc.chat.twitch.tv', 6667))
sock.send(f"NICK justinfan0\n".encode('utf-8'))
sock.send(f"JOIN {CHANNEL}\n".encode('utf-8'))

lastAlert = 0

current = False # Is an image being previewed?
que = [] # collection of image links in order as they are requested


# Application Class
class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Creates buttons and image viewer
        self.panel = tk.Label()
        self.yes = tk.Button(self, text="Yes", fg="green", command=self.push)
        self.yes.pack(side="bottom")
        self.no = tk.Button(self, text="No", fg="Red", command=self.reject)
        self.no.pack(side="bottom")
        self.clear = tk.Button(self, text="Clear", command=self.wipe)
        self.clear.pack(side="bottom")

        thread = threading.Thread(target=self.loop) # Alert Lopp
        thread.daemon = True
        thread.start()

        thread2 = threading.Thread(target=self.constant_check) # Loop for checking for images
        thread2.daemon = True
        thread2.start()

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

    def constant_check(self): # Checks for images and when a new image should be previewed
        global current
        global que
        print(current, que)
        if current is False and len(que) > 0:
            self.update_preview(que[0])
            current = True
        self.after(100,self.constant_check)

    def loop(self): # Alert loop
        while True:
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

    def push(self): # Image should be written
        global current
        global que

        file = PIL.Image.open(r"images/staging.png")
        scaled = int(500 * (file.size[1] / file.size[0]))
        file = file.resize((500, scaled), PIL.Image.ANTIALIAS)
        file.save(r"images/meme.png")
        self.update_preview(None)
        que.pop(0)
        current = False

    def reject(self): # Image should not exist
        global current
        global que

        self.update_preview(None)
        if len(que) > 0:
            que.pop(0)
        current = False

    def wipe(self): # Remove current image from stream
        global current
        global que
        self.update_preview(None)
        os.remove(r"images/meme.png")
        current = False

    def update_preview(self, link): # Called every time checker thinks a new image should be previewed
        global current
        if link == None:
            self.imgLabel = self.panel
            self.imgLabel.configure(image=None)
            self.imgLabel.image = None
            self.imgLabel.pack()
        else:
            try:
                response = requests.get(link).content
            except IndexError: #Bugged
                self.reject()

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


if __name__ == "__main__": #Self explanatory
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
