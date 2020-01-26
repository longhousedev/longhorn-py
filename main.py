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
    await ctx.message.author.voice.channel.connect()
    #bot.connect(test)

@bot.command()
async def leave(ctx):
    for voice in bot.voice_clients:
        if voice.channel == ctx.message.author.voice.channel:
            await voice.disconnect()
            return
    await ctx.send("Bot not connected to any channels!")

bot.run(token)

