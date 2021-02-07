import os
from discord.ext import commands
import discord
import datetime

import mongo
settings = mongo.settings()
category_id = settings.get('category_id')

def setup(bot):
    bot.add_cog(DMs(bot))

# main function
class DMs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        # Verify that the bot doesn't respond to itself

        if message.author == self.bot.user:
            return

        # Verify that message is not blank
        elif not message.content:
            return
        # Make sure its not a command
        elif message.content[0] == settings.get('prefix'):
            return

        # Check to see if message was sent to bot via DM
        elif str(message.channel.type) == "private":

            # get the ticket owner and see if he has any open tickets
            owner = message.author.id
            TicketName = mongo.search.by_user_active(owner)

            # If the owner doesn't have any tickets then create one
            if not TicketName:

                user_info = {
                    "uid" : message.author.id,
                    "author": message.author.name + '#' + message.author.discriminator,
                    "channel": message.channel.id,
                    "TicketName" : "",
                    "Count" : 0,
                    "messages" : []
                    }

                TicketName = mongo.search.new_ticket(user_info)

                # Default message for new ticket
                await message.reply(f'Hey {message.author.name}, {TicketName} has been opened and a moderator will respond as soon as possible\n Please note this ModMail is anonynmous, only server admins can see who you are.\n Please provide your username, if you feel that your username may be necessary for us to help solve your problem.')

            # Set time for message log
            time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H:%M:%S-%Z")

            # Get message
            message_data = {"content": message.content, 
                    "author": message.author.name + '#' + message.author.discriminator, 
                    "Time" : time,
                    "usr_message_id" : message.id
                    }

            # Insert into DB
            mongo.search.add_message(owner, TicketName, message_data)

            guild = discord.utils.get(self.bot.guilds)
            channel = discord.utils.get(guild.text_channels, name=TicketName)
            category = discord.utils.get(guild.categories, id=category_id)

            # verify ticket has appropiate channel
            print(channel)
            if channel is None:
                print('creating_channel')
                print(category)

                # Make channel otherwise
                await guild.create_text_channel(TicketName, category=category)
                channel = discord.utils.get(guild.text_channels, name=TicketName)
                print(channel)

            # send message in channel
            sent_message = await channel.send(message.content)
            mongo.search.append_id(TicketName, message.id, sent_message)
