import os
import sys
import discord
import youtube_dl
import configparser as cfp
# from discord.ext import commands


client = discord.Client()
# global data -- to be loaded in by configure()
token = None
guildName = None
sheet = None
# voice globals
channel = None
vc = None

songs = dict()


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
    playSong("hodgepodge")


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


# plays a chosen song
def playSong(songName):
    if vc.is_playing():
        stop()
    print(f"Playing song: {songName}")
    vc.play(discord.FFmpegPCMAudio(songName + ".mp3"), after=playSong(songName))


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
        # if we don't have the song yet, download it
        if not os.path.exists(conf[songStats]["songName"] + ".mp3"):
            print(f'downloading song: {conf[songStats]["songName"]}')
            downloadSong(conf[songStats]["songName"])


def main():
    configure()
    client.run(token)


main()
