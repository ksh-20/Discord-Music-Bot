import discord #SelectOption is present in this itself
from discord.ui import Button, Select, View
from discord.ext import commands #allows bot to recognise the commands
import asyncio #asynchronous function tool
from asyncio import run_coroutine_threadsafe
from urllib import parse, request #processing the yt links
import re
import json
import os
from youtube_dl import YoutubeDL #downloads audio from yt videos

class music_cog(commands.Cog):
    def __init__(self, bot): #self is the function itself, bot is in the main.py
        self.bot = bot

        #The below code is such that the bot can be present in multiple servers and can play the songs without getting mixed up with other servers.
        self.is_playing = {}
        self.is_paused = {}
        self.music_queue = {}
        self.queue_index = {} #number of songs in the queue

        self.YTDL_OPTIONS = {'format':'bestaudio', 'nonplaylist': 'True'} #options for downloading the song
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} #options for playing the song


        self.vc = {}  #status for if the bot is in a voice channel or not

    @commands.Cog.listener()
    #function which runs evertime the bot reebots(comes online)
    #Asynchronous functions doesnt wait to execute until a function is completed.
    async def on_ready(self):
        #for every server the bot has joined
        for guild in self.bot.guilds:
            id = int(guild.id)
            self.music_queue[id] = []
            self.queue_index[id] = 0
            self.vc[id] = None
            self.is_paused[id] = self.is_playing[id] = False

    #The function below is for user sending the msg and channel. ctx refers to the context of the message.
    async def join_vc(self, ctx, channel):
        id = int(ctx.guild.id)
        #If not connected to a channel
        if self.vc[id] == None or not self.vc[id].is_connected:
            #Connect the channel and assign it to the vc
            self.vc[id] = await channel.connect()

            #If the connection still fails:
            if self.vc[id] == None:
                await ctx.send("Could not connect to the Voice Channel.")
                return
        #If already connected to a channel, then move to a different one.
        else:
            await self.vc[id].move_to(channel)

    #Function for getting the song from YT
    def search_YT(self, search):
        queryString = parse.urlencode({'search_query': search})
        #Search YT with the user provided String. Returns an array with all related search results
        htmContent = request.urlopen('http://www.youtube.com/results?' + queryString)
        searchResults = re.findall('/watch\?v=(.{11})', htmContent.read().decode()) #returns the first 10 result links.
        return searchResults[0:10] #returns first 10
    
    #Function to extract information from YT video
    def extract_YT(self, url):
        with YoutubeDL(self.YTDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False) #doesnt download the file to system
            
            except:
                return False
        
        return {
            'link': 'https://www.youtube.com/watch?v=' + url,
            'thumbnail': 'https://i.ytimg.com/vi/' + url + '/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD5uL4xKN-IUfez6KIW_j5y70mlig',
            'source': info['formats'][0]['url'], 
            'title': info['title']
        }