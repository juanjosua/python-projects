import discord
from discord.ext import commands

client = commands.Bot(command_prefix='$') # specify prefix for a command

@client.event
async def on_ready():
    print('The Bot is now ready for use!')
    print('-------------------------------')


@client.command()
async def hello(ctx):
    await ctx.send('Hello, I am Ariel and I am a Bot.')


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


client.run('')
