import discord
import pytube
import youtube_dl as yt
import os
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
async def play(ctx, arg):
    os.remove('song.m4a')
    params = {
        'outtmpl' : 'song.m4a',
        'format': 'bestaudio/best',
        'postpreocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'prefferedquality': 128,
        }],
    }
    yt.YoutubeDL(params).download([arg])
    print("Track downloaded!")
    audio = discord.FFmpegOpusAudio('song.m4a', bitrate=160)
    print("Audio encoded!")
    #msg = "Now playing: " + title
    for voice in bot.voice_clients:
        if voice.channel == ctx.message.author.voice.channel:
            voice.play(audio)
            voice.volume = 50
    await ctx.send('Song playing!')

@bot.command()
async def vol(ctx, arg):
    for voice in bot.voice_clients:
        if voice.channel == ctx.message.author.voice.channel:
            voice.volume = int(arg)

@bot.command()
async def stop(ctx):
    for voice in bot.voice_clients:
        if voice.channel == ctx.message.author.voice.channel:
            voice.stop()

@bot.command()
async def leave(ctx):
    for voice in bot.voice_clients:
        if voice.channel == ctx.message.author.voice.channel:
            await voice.disconnect()
            return
    await ctx.send("Bot not connected to any channels!")


bot.run(token)

