# bot.py

import os
import yaml
TOKEN = os.getenv('DISCORD_TOKEN')
from discord.ext import commands
from other_commands import admin
from search_commands import search
from tickets import DMs
import discord

bot = commands.Bot(command_prefix='&', status='idle', activity=discord.Activity(type=discord.ActivityType.watching, name="my DM's"))

# client = discord.Client()
# some startup Debug information and set status to watching DMs
@bot.event
async def on_ready():
#    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='DM for complaints'))    
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

bot.add_cog(DMs(bot))
bot.add_cog(admin(bot))
bot.add_cog(search(bot))

bot.run(TOKEN)
