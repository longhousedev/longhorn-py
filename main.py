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

@bot.event
async def on_disconnect():
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()
        try:
            os.remove('song.m4a')
        except FileNotFoundError:
            pass
    except AttributeError:
        pass
    await ctx.send("Bot terminated.")


@bot.command()
async def join(ctx):
    await ctx.message.author.voice.channel.connect()
    await ctx.send("Joined "+ str(ctx.message.author.voice.channel))

@bot.command()
async def play(ctx, arg):
    if discord.utils.get(bot.voice_clients, guild=ctx.guild) is None:
        print("bob")
        await join(ctx)
    try:
        os.remove('song.m4a')
    except FileNotFoundError:
        pass
    params = {
        'outtmpl' : 'song.m4a',
        'format': 'bestaudio/best',
        'postpreocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'prefferedquality': 128,
        }],
    }
    title = yt.YoutubeDL(params).extract_info(arg, download=False).get("title", None)
    yt.YoutubeDL(params).download([arg])
    audio = discord.FFmpegOpusAudio("song.m4a", bitrate=160)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.play(audio)
    await ctx.send("Now playing: " + title)

@bot.command()
async def pause(ctx):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.pause()
        await ctx.send("Music paused.")
    except AttributeError:
        await ctx.send("Bot not connected to any channels!")

@bot.command()
async def resume(ctx):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.resume()
        await ctx.send("Music resumed!")
    except AttributeError:
        await ctx.send("Bot not connected to any channels!")


@bot.command()
async def stop(ctx):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()
        try:
            os.remove('song.m4a')
        except FileNotFoundError:
            pass
        await ctx.send("Music stopped.")
    except AttributeError:
        await ctx.send("Bot not connected to any channels!")

@bot.command()
async def leave(ctx):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()
        try:
            os.remove('song.m4a')
        except FileNotFoundError:
            pass
        await ctx.send("Bot disconnected.")
    except AttributeError:
        await ctx.send("Bot not connected to any channels!")

bot.run(token)

