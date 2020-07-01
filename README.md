# Victrola-Bot
A short Discord Bot to play and loop music for my online D&amp;D sessions.
I wanted a music bot where I could always loop the song and have my own gui.

# How it works
The bot reads config.ini and individually downloads and saves each (new) song to audio/[songName].mp3
then connects to the first voice channel of the server specified and a gui is created for playing any of the songs in config.ini  

# Setup
1. make a discord bot and application through the discord developer portal, and invite it to the server you'd like.
	- you can follow the instructions here
2. edit config.ini so that "token" is set to your new bot's token and "guild" is set to the name of the server you invited.
3. add songs by adding new sections to config.ini and filling in the fields of "songName" and "link".
	- so if you wanted to add the song "Rocket Man" by Elton John you would add this to config.ini

```
[song1]
songName = Rocket Man
link = https://youtu.be/DtVBCG6ThDk
```

4. run victrola.py
