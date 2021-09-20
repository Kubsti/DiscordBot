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
    file = pafy.new()
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice_client is None:
        voice_client = await voice.connect()
    else:
       await voice_client.move_to(channel) 

    async with ctx.typing():
        audio = file.getbestaudio()
        source = discord.FFmpegPCMAudio(audio.url, **ffmpeg_options)
        voice_client.play(source)
      
bot.run(TOKEN)

