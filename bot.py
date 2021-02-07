# bot.py

import os
from discord.ext import commands
import discord
import mongo 

settings = mongo.settings()
if not settings.print_all():
    import defaults 
else:
    print(settings.print_all())

from other_commands import help
#from search_commands import search
#from tickets import DMs

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=settings.get('prefix'), 
                   status='idle',
                   help_command=help(),
                   activity=discord.Activity(
                       type=discord.ActivityType.watching, 
                       name="my DM's"))

# some startup Debug information and set status to watching DMs

@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    print('Prefix is: {}'.format(settings.get('prefix')))
    print('Category ID: {}'.format(settings.get('category_id')))


bot.load_extension('category_listener')
bot.load_extension('DM_listener')
bot.load_extension('search_commands')
bot.load_extension('other_commands')


bot.run(TOKEN)
