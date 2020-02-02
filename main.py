import discord
import queue as queuepy
import youtube_dl as yt
import os
from discord.ext import commands
from configparser import ConfigParser
import logging
import asyncio
from _collections import deque
from random import choices
import string

logging.basicConfig(level=logging.WARNING)
queue_map = {}

config = ConfigParser()
config.read('config.ini')

bot = commands.Bot(command_prefix="!")
token = config.get('auth', 'token')

@bot.event
async def on_ready():
    print("Logged in!")

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
    global queue_map
    queue_map[discord.utils.get(bot.voice_clients, guild=ctx.guild)] = deque() #queuepy.Queue()


@bot.command()
async def play(ctx, arg):
    global queue_map
    if discord.utils.get(bot.voice_clients, guild=ctx.guild) is None:
        await join(ctx)
    q = queue_map.get(discord.utils.get(bot.voice_clients, guild=ctx.guild))
    # try:
    #     os.remove('song.m4a')
    # except FileNotFoundError:
    #     pass
    name = ''.join(choices(string.ascii_uppercase + string.digits, k = 6))
    params = {
        'outtmpl' : 'song_'+name+'.m4a',
        'format': 'bestaudio/best',
        'postpreocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'prefferedquality': 128,
        }],
    }
    title = yt.YoutubeDL(params).extract_info(arg, download=False).get("title", None)
    yt.YoutubeDL(params).download([arg])
    filename = 'song_'+name+'.m4a'
    if len(q) == 0:
        q.append([filename, title])
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        audio = discord.FFmpegOpusAudio(filename, bitrate=160)
        voice.play(audio)
        await ctx.send("Now playing: " + title)
    else:
        await ctx.send("Added " + title + " to the queue!")
        q.append([filename, title])

def my_after(error):
    coroutine = next()
    future = asyncio.run_coroutine_threadsafe(coro, bot.loop)
    try:
        future.result()
    except:
        pass

async def next():
    global queue_map
    q = queue_map.get(discord.utils.get(bot.voice_clients, guild=ctx.guild))
    q.pop()
    if len(q) > 0:
        data = q[-1]
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        audio = discord.FFmpegOpusAudio(data[0], bitrate=160)
        voice.play(audio, after=my_after)
        await ctx.send("Now playing: " + data[1])
    else:
        await ctx.send("Queue stopped: No more songs in the queue.")

@bot.command()
async def skip(ctx):
    global queue_map
    q = queue_map.get(discord.utils.get(bot.voice_clients, guild=ctx.guild))
    print(q)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    q.popleft()
    if len(q) > 0:
        data = q[0]
        audio = discord.FFmpegOpusAudio(data[0], bitrate=160)
        voice.play(audio)
        await ctx.send("Now playing: " + data[1])
    else:
        await ctx.send("Queue stopped: No more songs in the queue.")


@bot.command()
async def queue(ctx):
    try:
        q = queue_map.get(discord.utils.get(bot.voice_clients, guild=ctx.guild))
        if len(q) > 1:
            l = list(q)
            msg = "Songs Queued:\n"
            count = 1
            for song in l:
                msg += str(count) + " - "  + song[1] + "\n"
            await ctx.send(msg)
        else:
            await ctx.send("No songs are queued.")
    except AttributeError:
        await ctx.send("Bot not connected to any channels!")

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
            await ctx.send("Music stopped.")
        except FileNotFoundError:
            await ctx.send("Bot is not playing music!")
            pass
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

