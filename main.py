import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View

from music_cog import music_cog #imports the class music_cog from music_cog file

#Read the textfile
with open('token.txt', 'r') as file :
    token = file.readlines()[0] #read the first line

# Create bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents) #giving a prefix so that the bot knows the user is trying to access it

bot.add_cog(music_cog(bot))

bot.run(token)