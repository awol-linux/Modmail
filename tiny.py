# bot.py

import os
from discord.ext import commands
from dotenv import load_dotenv
from commands import admin

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# some startup Debug information and set status to watching DMs

bot = commands.Bot(command_prefix='&')

# main function
class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.content[0] == '&':
             return
        print(message)
        await message.channel.send('GotIt')

bot.add_cog(test(bot))
bot.add_cog(admin(bot))
bot.run(TOKEN)
