# Bardebot.py
import os

import discord
import asyncio
from discord.player import FFmpegAudio
import pafy
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="+")
client = discord.Client()
ffmpeg_options = {
    'options': '-vn'
}


@bot.command()
async def p(ctx):
    file = pafy.new('')
    
    if ctx.author.voice is None or ctx.author.voice.channel is None:
            return await ctx.send('You need to be in a voice channel to use this command!')

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    elif ctx.voice_client.channel is ctx.author.voice.channel:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client

    async with ctx.typing():
        audio = file.getbestaudio()
        source = discord.FFmpegPCMAudio(audio.url, **ffmpeg_options)
        vc.play(source)
      
bot.run(TOKEN)

