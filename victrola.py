import os
import sys
import discord
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

    # joining the first voice channel
    channel = guild.voice_channels[0]
    print("started joining")
    vc = await channel.connect()
    # vc.play(discord.FFmpegPCMAudio('hodgepodge.mp3'), after=lambda e: print('done', e))


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
    try:
        client.run(token)
    except KeyboardInterrupt:
        print("disconnect started")
        vc.disconnect()
        exit()


main()
