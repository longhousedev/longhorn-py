import discord
from discord.ext import commands
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')

bot = commands.Bot(command_prefix="!")

token = config.get('auth', 'token')

@bot.event
async def on_ready():
    print("We have logged in as {0.user}")

@bot.command()
async def join(ctx):
    global voice
    voice = await ctx.message.author.voice.channel.connect()
    #bot.connect(test)

@bot.command()
async def leave(ctx):
    await voice.disconnect()

bot.run(token)

