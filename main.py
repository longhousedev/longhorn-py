import discord
import pytube
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
    print(arg)
    query = pytube.YouTube(arg)
    source = query.streams.filter(audio_codec='opus', only_audio=True).order_by('abr').desc().first()
    track = source.stream_to_buffer()
    title = source.title
    print("Track downloaded!")
    audio = discord.FFmpegOpusAudio(track, bitrate=160)
    print("Audio encoded!")
    msg = "Now playing: " + title
    for voice in bot.voice_clients:
        if voice.channel == ctx.message.author.voice.channel:
            voice.play(audio)
            voice.volume = 100
    #await ctx.send(msg)

@bot.command()
async def leave(ctx):
    for voice in bot.voice_clients:
        if voice.channel == ctx.message.author.voice.channel:
            await voice.disconnect()
            return
    await ctx.send("Bot not connected to any channels!")

bot.run(token)

