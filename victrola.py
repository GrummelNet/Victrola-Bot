import os
import sys
import discord
import configparser as cfp
# from discord.ext import commands


client = discord.Client()
# global data -- to be loaded in by configure()
token = None
sheet = None


@client.event
async def on_ready():
    print("Bot is ready")


# reads config.ini file and loads in the token for discord and a google sheets document with the music details
# you'll have to edit config.ini for these to work properly
# currently, sheet is unused
def configure():
    global token
    global sheet
    conf = cfp.ConfigParser()
    conf.read("config.ini")
    token = conf['DEFAULT']['token']
    sheet = conf['DEFAULT']['sheet']


def main():
    configure()
    client.run(token)

main()
