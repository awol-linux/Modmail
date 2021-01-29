# bot.py

import os
from discord.ext import commands
import discord
import mongo 

if not mongo.settings.print_all():
    import defaults 
else:
    print(mongo.settings.print_all())

from other_commands import admin
from search_commands import search
from tickets import DMs

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=mongo.settings.get('prefix'), 
                   status='idle', 
                   activity=discord.Activity(
                       type=discord.ActivityType.watching, 
                       name="my DM's"))

# some startup Debug information and set status to watching DMs

@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))

bot.add_cog(DMs(bot))
bot.add_cog(admin(bot))
bot.add_cog(search(bot))

bot.run(TOKEN)
