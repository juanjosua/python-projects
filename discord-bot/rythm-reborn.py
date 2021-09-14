import discord
from discord.ext import commands
import pafy
import pyglet
import urllib.request
from urllib.parse import *
from bs4 import BeautifulSoup
import requests
import os


client = commands.Bot(command_prefix='$')  # specify prefix for a command


class Youtube_mp3():
    def __init__(self):
        self.lst = []
        self.dict = {}
        self.dict_names = {}
        self.playlist = []

    def url_search(self, search_string, max_search):
        textToSearch = search_string
        query = urllib.parse.quote(textToSearch)

        # google search using site:youtube.com
        url = "https://www.google.com/search?q=site%3Ayoutube.com+=" + query
        response = requests.get(url, headers={
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'})
        soup = BeautifulSoup(response.text, "lxml")

        # search results
        results = soup.findAll(attrs={'class': 'yuRUbf'})

        i = 1
        for div in results:
            for link in div.find_all('a'):
                if len(self.dict) < max_search:
                    self.dict[i] = link['href']
                    i += 1
                else:
                    break

    def get_search_items(self, max_search):

        if self.dict != {}:
            i = 1
            for url in self.dict.values():
                try:
                    info = pafy.new(url)
                    self.dict_names[i] = info.title
                    print("{0}. {1}".format(i, info.title))
                    i += 1

                except ValueError:
                    pass

    def play_media(self, num):
        url = self.dict[int(num)]
        info = pafy.new(url)
        #audio = info.m4astreams[-1]
        audio = info.getbestaudio(preftype="m4a")
        audio.download('song.m4a', quiet=True)
        song = pyglet.media.load('song.m4a')
        player = pyglet.media.Player()
        player.queue(song)
        print("Playing: {0}.".format(self.dict_names[int(num)]))
        player.play()
        stop = ''
        while True:
            stop = input('Type "s" to stop; "p" to pause; "" to play; : ')
            if stop == 's':
                player.pause()
                os.remove("song.m4a")
                break
            elif stop == 'p':
                player.pause()
            elif stop == '':
                player.play()
            elif stop == 'r':
                # player.queue(song)
                # player.play()
                print('Replaying: {0}'.format(self.dict_names[int(num)]))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$play'):
        x = Youtube_mp3()
        search = ''
        search = msg.split('$play ', 1)[1]
        old_search = search
        max_search = 1

        x.dict = {}
        x.dict_names = {}

        await message.channel.send('\nFetching for: {0} on youtube.'.format(search.title()))
        x.url_search(search, max_search)
        x.get_search_items(max_search)
        x.play_media(1)


    if msg.startswith('$join'):
        channel = message.author.voice.channel
        await channel.connect()

    if msg.startswith('$leave'):
        await message.voice_client.disconnect()


client.run('')
