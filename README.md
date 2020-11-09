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
- Ability to send images to separate channels for streamers who need more active moderation.
- Gif support

### Unincluded Assets (Must be manually installed):
- PIL (Pillow)
- Discord.py
- Requests

### Set-up

_Edit file config.ini_

```
[settings]
input = <discord channel>
output = <discord channel>
channel = <twitch channel>
authkey = <discord app auth>
delay = <time in seconds>
width = <lock image to width>
sound_file = <path to .wav>
alert_sound = True
image_sound = <path to .wav>
alert_image = True
alert_rumble = True
chat_enabled = True
init = True
```

## Testing
- Run memebeam.py
- Copy/paste an image from the web or upload an image from your computer in the text channel specified as "INPUT" in config.py.
- Select the check/x on the image in the channel specified as "output."
- Check the images folder within the project folder.
- Set the source of an image in OBS or Streamlabs OBS to "meme.gif" within the images folder.
- If you want stream notifications in chat, enable that feature using streamlabs cloudbot or your own favorite chatbot.
- Type !Clear into the streamer channel to delete the current image
- Type !Settings into the streamer channel to activate the gui.
