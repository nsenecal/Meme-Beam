import tkinter as tk
from tkinter import filedialog
import configparser

config = configparser.ConfigParser()


class Gui:
    def __init__(self, master=None):
        self.master = master
        master.title("Meme-Beam Settings")
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
        INIT = config['settings']['INIT']
        CHAT_ENABLED = config['settings']['CHAT_ENABLED']

        def chatfile():
            self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
            sound2.delete(0, 'end')
            sound2.insert(1, self.master.filename)
            sound2.xview('end')

        def imgfile():
            self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
            alt2.delete(0, 'end')
            alt2.insert(1, self.master.filename)
            alt2.xview('end')

        def save():
            from common.shared import ech
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
            config['settings']['INIT'] = startup.var.get()
            config['settings']['CHAT_ENABLED'] = chat.var.get()
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

        input = tk.Label(master, text="Viewer Channel:")
        input.grid(row=1, column=1)
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
        startup = tk.Checkbutton(master, text="Run on Startup", onvalue="True", offvalue="False")
        startup.grid(row=10, column=3)
        startup.var = tk.StringVar(value=INIT)
        startup.config(var=startup.var)
        apply = tk.Button(master, text="Apply All Changes", command=save)
        apply.grid(row=10, column=4)


def run():
    root = tk.Tk()
    Gui(root)
    root.mainloop()
