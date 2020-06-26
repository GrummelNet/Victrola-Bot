import os
import sys
import discord
import youtube_dl
import configparser as cfp
import threading
# from discord.ext import commands
# import tkinter as tk
from gui import *


client = discord.Client()
# global data -- to be loaded in by configure()
token = None
guildName = None
sheet = None
# voice globals
channel = None
vc = None

songs = dict()
songList = []
currentSong = ''

@client.event
async def on_ready():
    global channel
    global vc
    print("Bot is ready")
    # finding chosen guild
    for guild in client.guilds:
        if guild.name == guildName:
            break

    # joining the voice channel
    channel = guild.voice_channels[0] # just picks the first voice channel in the list
    print("started joining")
    vc = await channel.connect()
    startSong("hodgepodge")


# downloads a song in the config.ini list
# called by configure()
def downloadSong(songName):
    global songs
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': songName + '.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([songs[songName]])


# starts a song
def startSong(songName):
    global currentSong
    if vc.is_playing():
        vc.stop()
    print(f"Playing song: {songName}")
    currentSong = songName
    # looping songs can't be done this way.
    vc.play(discord.FFmpegPCMAudio(songName + ".mp3"), after=loopSong)

# is called when the currentSong ends and replays that song
def loopSong(error):
    global currentSong
    print(f"Looping song: {currentSong}")
    vc.play(discord.FFmpegPCMAudio(currentSong + ".mp3"), after=loopSong)


# takes in a list of button texts and returns a list of buttons with those texts
# arranges them in a grid
def buttonsFromList(textList, m):
    width = smallestSquare(len(textList))

    r = 0
    c = 0
    for bText in textList:
        button = tk.Button(
            master = m,
            text = bText,
            command = partial(startSong, bText),
            height = 5,
            width =  15
        )
        button.grid(row=r, column=c)
        # button.pack()
        c += 1
        if c > width:
            c = 0
            r += 1
    # TODO: add connect + disconnect


# reads config.ini file and loads in the token for discord and a google sheets document with the music details
# you'll have to edit config.ini for these to work properly
# currently, sheet is unused
def configure():
    global token
    global guildName
    global sheet
    global songs
    conf = cfp.ConfigParser()
    conf.read("config.ini")
    token = conf['DEFAULT']['token']
    guildName = conf['DEFAULT']['guild']
    sheet = conf['DEFAULT']['sheet']

    # creating the song list
    for songStats in conf.sections():
        print(f"Handling section: {songStats}")
        print(conf[songStats]["link"])
        # adding song to song dictionary
        songs[conf[songStats]["songName"]] = conf[songStats]["link"]
        songList.append(conf[songStats]["songName"])
        # if we don't have the song yet, download it
        if not os.path.exists(conf[songStats]["songName"] + ".mp3"):
            print(f'downloading song: {conf[songStats]["songName"]}')
            downloadSong(conf[songStats]["songName"])


# to be called by a thread, starts the Gui loop
# root must be a tkinter window
def startGui():
    window = makeWindow()
    buttonsFromList(songList, window)
    window.mainloop()


def main():
    configure()

    gui = threading.Thread(
        target=startGui,
        name="guiThread",
        # args=(window,),
        # kwargs={}
    )
    print("got after gui thread")
    gui.start()
    print("got after window mainloop")
    client.run(token)


main()
