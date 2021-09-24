import discord
from discord.ext import commands
import asyncio
import os
import youtube_dl
from discord.player import FFmpegPCMAudio
import json

class music(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.song_queue = []
        self.title_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.loop = False

    @commands.command(aliases=['p'])
    async def play(self, ctx, url):
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")
            return
        await self.join(ctx)
        await self.queueMusic(ctx, url)
        if ctx.voice_client.is_playing() is False:
            await self.playMusic(ctx)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await self.message.clear_reaction('▶️')
        await self.message.add_reaction('⏸️')

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await self.message.clear_reaction('⏸️')
        await self.message.add_reaction('▶️')

    @commands.command(aliases=['stop'])
    async def skip(self, ctx):
        ctx.voice_client.stop()
        self.loop = False

    @commands.command()
    async def clearl(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        self.song_queue.clear()
        self.title_queue.clear()

    @commands.command()
    async def view(self, ctx):
        if len(self.title_queue) == 0:
            embed = discord.Embed(title=":scroll: Song queue", description=":warning: List is empty", color=0x71368a)
        else:
            str_list = "```Elm\n"
            for i in range(len(self.title_queue)):
                str_list += f'{str(i+1)}) {self.title_queue[i]}' + '\n'
            str_list += "```"
            embed = discord.Embed(title=":scroll: Song queue", description=str_list, color=0x71368a)
        message = await ctx.send(embed=embed)
        await message.delete(delay = 10)

    @commands.command()
    async def loop(self, ctx, option):
        if option == "on":
            self.loop = True
        elif option == "off":
            self.loop = False
        embed = discord.Embed(title="", description=f':arrows_counterclockwise: loop is {option}', color=0x71368a)
        message = await ctx.send(embed=embed)
        await message.delete(delay=5)

    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await self.queue.clear()
            await ctx.voice_client.move_to(voice_channel)
    
    async def leave(self, ctx):
        channel_connected = ctx.voice_client.channel
        while len(channel_connected.members) > 1:
            await asyncio.sleep(3)
            if ctx.voice_client.is_playing():
                return;
            continue
        self.song_queue.clear()
        self.title_queue.clear()
        await ctx.voice_client.disconnect()

    async def queueMusic(self, ctx, url):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            song_info = ydl.extract_info(url, download=False)
        self.song_queue.append(song_info['formats'][0]['url'])
        self.title_queue.append(song_info['title'])
        embed = discord.Embed(title="", description=f':clipboard: Added {self.title_queue[len(self.title_queue)-1]} to queue', color=0x71368a)
        message = await ctx.send(embed=embed)
        await message.delete(delay = 5)

    async def playMusic(self, ctx):
        vc = ctx.voice_client
        SOURCE = await discord.FFmpegOpusAudio.from_probe(self.song_queue[0], **self.FFMPEG_OPTIONS)
        try:
            vc.play(SOURCE)
            embed = discord.Embed(title="", description=f':musical_note: Now playing {self.title_queue[0]}', color=0x71368a)
            self.message = await ctx.send(embed=embed)
            await self.message.add_reaction('▶️')
        except:
            pass
        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(3)
        await self.message.clear_reactions()
        await self.message.delete()
        if len(self.song_queue) > 0 and self.loop == False:
            self.song_queue.pop(0)
            self.title_queue.pop(0)
        if len(self.song_queue) > 0:
            await self.playMusic(ctx)
        else:
            await self.leave(ctx)

def setup(client):
    client.add_cog(music(client))