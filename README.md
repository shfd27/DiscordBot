# DiscordBot
DiscordBot with Python

# About
### The bot works on the Discord!  
Try my discord bot [seol bot](https://discord.com/api/oauth2/authorize?client_id=688395885259784212&permissions=0&scope=bot)!  
music.py - playing youtube music is available. you need Youtube API.  

# Installation
### install python

1.install python which version is more than 3.6  
2.install pakages below using pip  

### Configuration  
Set configs/configs.py using sample_configs.py  
and docs/music_options.py(YOUTUBE_API_KEY)

### download ffmpeg

#### for windows
3.download ffmpeg from ffmpeg.  
4.unzip ffmpeg  
5.open command shell as an administrator and enter setx Path "%Path%; &lt; your ffmpeg dir path &gt; \bin"  
(or set ffmpeg dir path to Environment Variables-User variables Path)  

#### for linux
3.sudo apt-get update  
4.sudo apt-get install ffmpeg  

# Development Environment
This bot  is developed on python version 3.8.  

Python which version is 3.6 or more is required.  
(Discord api support for Python versions 3.5.3 or more.)  
(The f-string(string formatting) is available for Python versions 3.6 or more.)   

# Need Pakages

discord  

asyncio(standard pakage)  


### music.py
PyNaCl  

youtube_dl  

urllib(standard pakage)  

# Commands

### music.py
join : join the voice channel  

leave : leave the voice channel  

play {search} : search {search} source at youtube and play source  

pause : pause the play source

resume : resume the play source

skip : skip the play source  

q : show current queue  

# Join Community
DiscordBot is developed currently. If you need help or want to give some advices, freely join my discord server.  

<a href="http://join.shfd27.p-e.kr"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Discord-512.webp/512px-Discord-512.webp.png" height="35px" width="35px"></a>

# Version
`1.1.0`