# RaspiBOT R3B0RN
RaspiBOT is a Telegram's Bot to control your Raspberry Pi and keep in contact with it.

## What it does
RaspiBOT has the following functionalities:
 - Show system's summary stats.
 - Add a torrent to Transmission, using its magnet link.
 - Remove a torrent from Tranmission's active torrents.
 - List Transmission's active torrents.
 - Notify Transmission's completed torrents.
 - Run user aliases.
 - More to come...

RaspiBOT also comes 'chat_id secured', which means that once you install it and say '/start' to it, it will only respond to you and no one more. That implies that only you could send commands to your RaspiBOT.

## Installation
To install RaspiBOT, you only need to execute our setup Bash script (we not recomend using PuTTY to log in to SSH, as we use 'dialog' and stuff goes weird):

```sh
$ bash <(curl -sL git.io/vSdkW)
```

## Update
Updating RaspiBOT is very easy. The only thing you need to do is use RaspiBOT's script and tell it that you want to update:

```sh
$ raspibot update
```
You can see other options with:
```sh
$ raspibot help
```

## Versions

 - v2.0.1 "Dawn of RaspiBOT" 
 - v1.0.1 "Cabashito Carmesí" https://github.com/alhenx/raspibot/tree/raspibot_old (UNMAINTAINED).
 

