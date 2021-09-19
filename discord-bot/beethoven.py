import discord
from discord.ext import commands
import pafy
import pyglet
import urllib.request
from urllib.parse import *
from bs4 import BeautifulSoup
import requests
import os
from pathlib import Path
import hashlib


client = commands.Bot(command_prefix='$')  # specify prefix for a command
player = pyglet.media.Player()
song_list = []


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@client.command()
async def search(ctx, *args):
    global song_list

    # make the sentence user insert url safe
    textToSearch = " ".join(args)
    await ctx.channel.send('\nFetching for: {0} on youtube.'.format(textToSearch))
    query = urllib.parse.quote(textToSearch)

    # google search using google dork site:youtube.com
    url = "https://www.google.com/search?q=site%3Ayoutube.com+=" + query
    response = requests.get(url, headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'})
    soup = BeautifulSoup(response.text, "lxml")

    # search results
    results = soup.findAll(attrs={'class': 'yuRUbf'})

    # add search result into list of songs
    for div in results:
        for link in div.find_all('a'):
            if len(song_list) >= 5:
                break

            if link['href'].startswith('https://www.youtube.com'):
                song_list.append(link['href'])

    # print result titles on discord
    for i, url in enumerate(song_list):
        try:
            info = pafy.new(url)
            await ctx.channel.send("{0}. {1}".format(i+1, info.title))

        except ValueError:
            pass


@client.command()
async def play(ctx, num):
    global song_list

    # select which song to play
    url = song_list[int(num)-1]

    # get the song url
    info = pafy.new(url)

    # download the audio
    song_title = hashlib.sha1(info.title.encode("UTF-8")).hexdigest()
    song_file = Path('queue/{}.m4a'.format(song_title))
    if not song_file.exists():
        audio = info.getbestaudio(preftype="m4a")
        audio.download('queue/{}.m4a'.format(song_title), quiet=True)

    # load the downloaded song
    song = pyglet.media.load('queue/{}.m4a'.format(song_title))
    player.queue(song)

    # play the song
    if player.playing == True:
        await ctx.channel.send("{0} added to queue.".format(info.title))
    else:
        await ctx.channel.send("Playing: {0}.".format(info.title))
        player.play()


@client.command()
async def pause(ctx):
    await ctx.channel.send("Pause song.")
    player.pause()


@client.command()
async def stop(ctx):
    global song_list

    await ctx.channel.send("Stop song.")
    player.pause()
    os.remove("song.m4a")

    # create new player and new song list
    song_list = []


@client.command()
async def resume(ctx):
    await ctx.channel.send("Resume song.")
    player.play()


@client.command()
async def queue(ctx):
    await ctx.channel.send("Song queue:")
    for i, song in enumerate(song_list):
        await ctx.channel.send("{}. {}".format(i, song))


@client.command()
async def skip(ctx):
    player.next_source()


@client.command()
async def is_playing(ctx):
    print(player.playing)
    print(player.source)
    print(player.loop)


client.run('')
