# DiscordBot
DiscordBot with Python


# About
### The bot works on the Discord!  
Try my discord bot [Seol](https://discord.com/api/oauth2/authorize?client_id=688395885259784212&permissions=0&scope=bot)!  

music.py - playing youtube music is available. you need Youtube API.  


# Installation

### install python

1.install python which version is more than 3.6  

2.install pakages below using pip  


### Configuration 

Set configs/configs.py - using sample_configs.py  

Set docs/music_options.py - `YOUTUBE_API_KEY`


### download ffmpeg

#### for Windows
3.download ffmpeg from [ffmpeg](https://ffmpeg.org/download.html)  

4.unzip ffmpeg  

5.open command shell as an administrator and enter setx Path "%Path%; ` your ffmpeg dir path `\bin"  
(or set ffmpeg bin dir path to Environment Variables-User variables Path)  

#### for Linux
3.sudo apt-get update  

4.sudo apt-get install ffmpeg  


# Development Environment
This bot is developed on python version 3.8.  

Python which version is 3.6 or more is required.  
(Discord api support for Python versions 3.5.3 or more.)  
(The `f-string`(string formatting) is available for Python versions 3.6 or more.)   


# Need Pakages
  
discord  

os(standard pakage)  

sys(standard pakage)  

asyncio(standard pakage)  


### music.py
PyNaCl  

youtube_dl  

urllib(standard pakage)  

datetime(standard pakage)  


# Commands

### music.py
join : join the voice channel  

leave : leave the voice channel  

play `search` : search `search` source at youtube and play source  
&nbsp;&nbsp;&nbsp;&nbsp;-youtube, twitch, and other source is available

pause : pause the play source

resume : resume the play source

skip : skip the play source  

volume `volume` : adjust volume to `volume` (0~100)  

speed `speed` : adjust next play source speed to `speed` (0~)    

queue : show current queue  


# Join Community
DiscordBot is developed currently. If you need help or want to give some advices, freely join my discord server.  

<a href="http://join.shfd27.p-e.kr"><img src="https://github.com/shfd27/shfd27/blob/main/image/discord.png?raw=true" height="35px" width="35px"></a>


# Version
`1.1.0`