import discord
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
token = config.get('auth', 'token')

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}")

client.run(token)