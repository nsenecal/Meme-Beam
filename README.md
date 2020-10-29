# Meme-Beam

_A shameless fork of Chatding with image sharing capabilities_

## Preamble

**Meme-Beam** is a utility designed for streamers with low or no audience alerting the user with an audible alarm when someone writes in the twitch chat. To encourage additional audience interaction, viewers will also be able to send images to the streamer to check and subsequently push to their stream, or delete.

## Testing
- Follow Set-up below.
- Type !meme in twitch chat, followed by a space and the **image location** of an image. When you paste the image location into an internet browser it should take you straight to the image, not a website.
- Check the images folder within the project folder.

## Planned Features
- A full gui
- A passive twitch chat sifter
- Android client for single monitor streamers
- Image viewer for multi monitor streamers
- Remote clients for moderators(?)

### Unincluded Assets:
- PIL (Pillow)
- 

### Set-up

_Edit file config.py_

```
# Your twitch channel preceded by a hash
CHANNEL = '#sheuronazxe'

# Wait x seconds to play alert again on new chat message
DELAY = 120

### Enable (True) / Disable (False) alert modules
# ALERT_SOUND plays audible alarm on default sound device
# ALERT_RUMBLE activate rumble on XBOX compatible controller, more settings in rumble.py
ALERT_SOUND = True
ALERT_RUMBLE = False

# Alert sound file in WAV format
SOUND_FILE = 'sounds/alert.wav'
```

### Behavior

**Meme-Beam** plays the alert when it detects a new message in the chat and waits the number of seconds specified in the DELAY variable for a new alert.

If the window is in foreground no sound will be played (this feature only works on Windows platform).
