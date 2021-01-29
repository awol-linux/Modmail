import os
from discord.ext import commands
import discord
import datetime

import mongo
catagory_id = mongo.settings.get('category_id')
print(f' category ID = {category_id}')
# main function
class DMs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        #    verify that the bot doesn't respond to itself

        if message.author == self.bot.user:
            return
        elif not message.content:
            return
        elif message.content[0] == mongo.settings.get('prefix'):
            return
            # check to see if message was sent to bot via DM
        elif str(message.channel.type) == "private":

            owner = message.author.id
            TicketName = mongo.search.by_user_active(owner)
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
                await message.reply(f'Hey {message.author.name}, {TicketName} has been opened and a moderator will respond as soon as possible\n Please note this ModMail is anonynmous, only server admins can see who you are.\n Please provide your username, if you feel that your username may be necessary for us to help solve your problem.')


            time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H:%M:%S-%Z")
            message_data = {"content": message.content, 
                    "author": message.author.name + '#' + message.author.discriminator, 
                    "Time" : time }

            mongo.search.add_message(owner, TicketName, message_data)
            guild = discord.utils.get(self.bot.guilds)


                       # for total in search:
            #    print('#############################################################################################')
            #    print(total)
            #    print(total['TicketName'])
            #    TicketName = total['TicketName']
            #    print('#############################################################################################')

            channel = discord.utils.get(guild.text_channels, name=TicketName)
            category = discord.utils.get(guild.categories, id=category_id)

            # verify ticket has appropiate channel
            print(channel)
            if channel is None:
                print('creating_channel')
                print(category)
                await guild.create_text_channel(TicketName, category=category)
                channel = discord.utils.get(guild.text_channels, name=TicketName)
                print(channel)


            await channel.send(message.content)

        # If message is in ticket category
        elif message.channel.category_id == category_id:

            # Figure out whose ticket it was
            TicketName = message.channel.name
            owner = mongo.search.get_owner(TicketName)
            time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H:%M:%S-%Z")
            message_data = {"content": message.content, "author": message.author.name + '#' + message.author.discriminator, "Time" : time }
            mongo.search.add_message(owner, TicketName, message_data)
            
            #search = collection.find(owner, RemoveID)
            #for total in search:
            #    print('#############################################################################################')
            #    print(total)
            #    print(total['Count'])
            #    Count = (total['Count'])

            #    print(total['TicketName'])
            #    TicketName = total['TicketName']
            #    print('#############################################################################################')



            # DM user with moderators response
            user = await self.bot.fetch_user(owner)
            DM = await user.create_dm()

            # The moderator name is public

            embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
            await DM.send(embed=embedVar)
