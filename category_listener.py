import os
from discord.ext import commands
import discord
import datetime

import mongo
settings = mongo.settings()
category_id = settings.get('category_id')

def setup(bot):
    bot.add_cog(responses(bot))

class responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Listen for responses in public channel
    @commands.Cog.listener()
    async def on_message(self, message):

        # Verify that the bot doesn't respond to itself
        if message.author == self.bot.user:
            return

        # If DM return
        elif not hasattr(message.channel, 'category_id'):
            return

         # Make sure its not a command
        elif message.content[0] == settings.get('prefix'):
            return

        # If message is in ticket category
        elif message.channel.category_id == category_id:

            # Figure out whose ticket it was
            TicketName = message.channel.name
            owner = mongo.search.get_owner(TicketName)
            time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H:%M:%S-%Z")
            message_data = {"content": message.content, "author": message.author.name + '#' + message.author.discriminator, "Time" : time }
            mongo.search.add_message(owner, TicketName, message_data)

            # DM user with moderators response
            user = await self.bot.fetch_user(owner)
            DM = await user.create_dm()

            # The moderator name is public
            embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
            await DM.send(embed=embedVar)
