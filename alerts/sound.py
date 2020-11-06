from sys import platform


def alert(SOUND_FILE):

    if "linux" in platform:
        import os
        os.system(f"aplay -q {SOUND_FILE}")

    elif "darwin" in platform:
        import os
        os.system(f"afplay {SOUND_FILE}")

    elif "win" in platform:
        import winsound
        winsound.PlaySound(SOUND_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC)

    else:
        raise Exception('ERROR: Unsupported platform to play audio. Edit config.py and disable audio.')
