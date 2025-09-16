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

        #Colour options for Embed
        self.embedBlue = 0x2c76dd
        self.embedRed = 0xdf1141
        self.embedGreen = 0x0eaa51

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

    #Function for generating embeds
    def now_playing_embed(self,ctx,song):
        title = song['title']
        link = song['link']
        thumbnail = song['thumbnail']
        author = ctx.author #author of the command message sent
        avatar = author.avatar_url

        embed = discord.Embed(
            title="Now Playing",
            description=f'[{title}]({link})', #[] is the text displayed, () is the link redirection
            colour=self.embedBlue
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f'Song added by: {str(author)}', icon_url=avatar)
        return embed

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
    
    def play_next(self, ctx):
        id = int(ctx.guild.id)
        if not self.is_playing[id]:
            return
        
        if self.queue_index[id] + 1 < self.music_queue[id]:
            self.is_playing[id] = True
            self.queue_index[id] += 1

            song = self.music_queue[id][self.queue_index[id]][0]
            message = self.now_playing_embed(ctx,song)

            #We need a co-routine function to send the message since play_next isnt asynchronous
            coro = ctx.send(message)
            fut = run_coroutine_threadsafe(coro, self.bot.loop)

            try:
                fut.result()
            except:
                pass
            
            self.vc[id].play(discord.FFmpegPCMAudio(
                song['source'], **self.FFMPEG_OPTIONS
            ), after= lambda e: self.play_next(ctx))

        else:
            self.queue_index[id] += 1
            self.is_playing[id] = False

    async def play_music(self,ctx):
        id = int(ctx.guild.id)
        #if the queue index is less than length of the music queue
        if self.queue_index[id] < len(self.music_queue[id]):
            self.is_playing[id] = True
            self.is_paused[id] = False

            #these awaits can be done only in asynchronous functions.
            await self.join_vc(ctx, self.music_queue[id][self.queue_index[id]][1]) #gives us a voice channel to join

            song = self.music_queue[id][self.queue_index[id]][0]
            message = self.now_playing_embed(ctx,song)
            await ctx.send(embed=message)
            
            #go to the vc of our server and play the song using the ffmpeg audio
            self.vc[id].play(discord.FFmpegPCMAudio(
                song['source'], **self.FFMPEG_OPTIONS
            ), after= lambda e: self.play_next(ctx))

        else:
            await ctx.send("There are no songs in the queue to be played.")
            self.queue_index[id] += 1
            self.is_playing[id] = False