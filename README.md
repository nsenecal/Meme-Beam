# Meme-Beam

_A shameless fork of Chatding with image sharing capabilities and Discord integration_

## Credit
- sheuronazxe: Chatding! source code.
- evanpurl: Direction and assistance with Discord.py.

## Description

**Meme-Beam** is a utility designed for streamers with low or no audience alerting the user with an audible alarm when someone writes in the twitch chat. To encourage additional audience interaction, viewers will also be able to send images to the streamer to check and subsequently push to their stream, or delete.

Meme-Beam is integrated into discord, where streamers can have a cohesive experience: monitoring submissions, reading chat, and even reading stream notifications with the aid of a third party bot.

Using Discord as a primary platform eliminates the need for desktop, remote, and mobile clients. It's usable on any platform that supports discord, and allows moderators to monitor image submissions from wherever they are.

## Planned Features
- Ability to send images to speperate channels for streamers who need more active moderation.
- Gif support

### Unincluded Assets (Must be manually installed):
- PIL (Pillow)
- Discord.py

### Set-up

_Edit file config.py_

```
# Your twitch channel preceded by a hash
CHANNEL = '#generic'

#Discord App Authentication Key
AUTHKEY = '<Auth Key>'

#Text channel that viewers submit images in
INPUT = '<viewer channel>' 

#Text channel that the streamer monitors
OUTPUT = '<streamer view>'

# Wait x seconds to play alert again on new chat message
DELAY = 10

### Enable (True) / Disable (False) alert modules
# ALERT_SOUND plays audible alarm on default sound device
# ALERT_RUMBLE activate rumble on XBOX compatible controller, more settings in rumble.py
ALERT_SOUND = True
ALERT_RUMBLE = False

# Alert sound file in WAV format
SOUND_FILE = 'sounds/alert.wav'
```

## Testing
- Run memebeam.py
- Copy/paste an image from the web or upload an image from your computer in the text channel specified as "INPUT" in config.py.
- Select the check/x on the image in the channel specified as "OUTPUT."
- Check the images folder within the project folder.
- Set the source of an image in OBS or Streamlabs OBS to "meme.gif" within the images folder.
- If you want stream notifications in chat, enable that feature using streamlabs cloudbot or your own favorite chatbot.
