import discord
from discord.ui import Button, Select, View, SelectOption
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