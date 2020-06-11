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
    # source = discord.FFmpegPCMAudio('hodgepodge.mp3'), after=lambda e: print('done', e)
    # playing test song

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://youtu.be/OlhqQfzaQTk"])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    vc.play(discord.FFmpegPCMAudio("song.mp3"))
    # vc.play(source)


# reads config.ini file and loads in the token for discord and a google sheets document with the music details
# you'll have to edit config.ini for these to work properly
# currently, sheet is unused
def configure():
    global token
    global guildName
    global sheet
    conf = cfp.ConfigParser()
    conf.read("config.ini")
    token = conf['DEFAULT']['token']
    guildName = conf['DEFAULT']['guild']
    sheet = conf['DEFAULT']['sheet']


def main():
    configure()
    # handling Ctrl-C to stop the bot -- does not work
    try:
        client.run(token)
    except (KeyboardInterrupt, SystemExit):
        print("KeyboardInterrupt reached")
        vc.disconnect()
        exit()


main()
