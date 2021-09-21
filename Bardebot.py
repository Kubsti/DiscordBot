# Bardebot.py
from logging import NullHandler
import os, re, discord, pafy, urllib.request
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

def checklink(link):
    youtuberegex = re.compile('(http:|https:)?\/\/(www\.)?(youtube.com|youtu.be)\/(watch)?(\?v=)?(\S+)?')
    linkcontent = link.split(" ", 1)
    if youtuberegex.match(linkcontent[1]):
        m = re.search(youtuberegex, linkcontent[1])
        return ['youtube', m]
    else:
        return ['nothing found', linkcontent[1]]


def youtubesearch(searchterm):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + searchterm)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    if video_ids:
        return video_ids[0]
    else:
        None

@bot.command()
async def p(ctx):

    message = ctx.message.content
    if message:
        youtubeurl = checklink(message)
    else:
        print('no message found')
        return

    if youtubeurl[0] == 'youtube':        
        file = pafy.new(youtubeurl[1])
    else:
        searchresult = youtubesearch(youtubeurl[1].replace(' ',''))
        if searchresult:
            file = pafy.new('https://www.youtube.com/watch?v='+searchresult)
        else:
            ctx.send('Nothing found for your search') 

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

