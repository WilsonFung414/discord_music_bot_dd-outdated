import discord
from discord.ext import commands
import time

class common(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command() # Same as client.command
    async def ping(self, ctx):
        message = await ctx.send(f'{round(self.client.latency*1000)}ms')

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)
        message = await ctx.send(f'Deleted {amount} messages')
        await message.delete(delay=5)

    @commands.command()
    async def jp(self, ctx):
        await ctx.send(f'あ　い　う　え　お\nか　き　く　け　こ\nさ　し　す　せ　そ\nた　ち　つ　て　と\nな　に　ぬ　ね　の\nは　ひ　ふ　へ　ほ\nま　み　む　め　も\nや　ゆ　よ\nら　り　る　れ　ろ\nわ　を\nん\nWah')
def setup(client):
    client.add_cog(common(client))