import os
from discord.ext import commands
import discord
import datetime

from pymongo import MongoClient
USER = os.getenv('MONGO_USER')
PASS = os.getenv('MONGO_PASSWORD')
mdbclient = MongoClient('172.20.0.10', 27017, username=USER, password=PASS)
ticket_first = mdbclient['tickets']
user_first = mdbclient['userid']


# main function
class DMs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        #    verify that the bot doesn't respond to itself
#        print(message)

        if message.author == self.bot.user or message.content[0] == '&':
            return

            # check to see if message was sent to bot via DM
        if str(message.channel.type) == "private":

            get_ticket_number = user_first[str(message.author.id)]
            RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}

            # run a query to check for tickets

            find_old_tickets = get_ticket_number.find({ "status" : "active"}, RemoveID)
            for ticket_found in find_old_tickets:

                # debugging data

                print(ticket_found)

                # only show active tickets

                if ticket_found['status'] ==  "active":
                    print(ticket_first.list_collection_names())
                    TicketName = ticket_found['TicketName']
                    print('Ticketname is ' + TicketName)
                    already_has_ticket = True

            # If there is no ticket created make a new one 
            print(ticket_first.list_collection_names())
            amount = len(ticket_first.list_collection_names()) + 1
            if 'TicketName' not in locals():
                TicketName = 'ticket-' + str(amount)
                user_info = {"TicketName": TicketName, "status" : "active", }
                get_ticket_number.insert_one(user_info)
                already_has_ticket = False

                # debug data
                print('78 getnumber.insert_one(user_info)')
                print(TicketName)
                print(ticket_first.list_collection_names())
                print(len(ticket_first.list_collection_names()))
                print('couldnt find ticket')

            collection = ticket_first[str(TicketName)]
        
            guild = discord.utils.get(self.bot.guilds)
            print(guild)

            # create vars to help query mongoDB
            author = {"uid": message.author.id }
            update_count = {"$inc" : { "Count" : 1}}
            RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}
            search = collection.find(author, RemoveID)

            # initilize ticket if user hasn't created one yet
            list_of_tickets = ticket_first.list_collection_names()
            print(list_of_tickets)
            if not already_has_ticket:
                print(TicketName)
                user_info = {
                    "uid" : message.author.id,
                    "author": message.author.name + '#' + message.author.discriminator,
                    "channel": message.channel.id,
                    "TicketName" : TicketName,
                    "Count" : 0,
                    "messages" : []
                    }
            
                print('115 kp.insert_one({"uid" : message.author.id})')
                print('111 collection.insert(user_info)')
                collection.insert(user_info)

            collection.update_one(author, update_count)

            # Log message 
            time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H:%M:%S-%Z")
            message_data = {"content": message.content, 
                    "author": message.author.name + '#' + message.author.discriminator, 
                    "Time" : time }
            collection.update_one({'uid': message.author.id }, {'$push': {'messages': message_data}})

            # get total ticket count
            for total in search:
                print('#############################################################################################')
                print(total)
                print(total['TicketName'])
                TicketName = total['TicketName']
                print('#############################################################################################')

            channel = discord.utils.get(guild.text_channels, name=TicketName)
            catagory = discord.utils.get(guild.categories, id=798284727794270229)

            # verify ticket has appropiate channel
            print(channel)
            if channel is None:
                print('creating_channel')
                await guild.create_text_channel(TicketName, category=catagory)
                channel = discord.utils.get(guild.text_channels, name=TicketName)
                print(channel)


            # Debug data
            for result in search:
                print(result)

            # Send message in channel
            print('sending_message')
            await channel.send(message.content)

        # If message is in ticket catagoru\y
        elif message.channel.category_id == 798284727794270229:

            # Figure out whose ticket it was
            author = {"uid": message.author.id }
            address = { "uid" : {"$exists" : "true" } }
            RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}
            update_count = {"$inc" : { "Count" : 1}}
            ticket_list = ticket_first[message.channel.name]
            query = ticket_list.find(address)
            for ticket in query:
                print(ticket['uid'])
                uid = ticket['uid']
            collection = ticket_first[message.channel.name]
            print(uid)

            # Log message
            time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H:%M:%S-%Z")
            message_data = {"content": message.content, "author": message.author.name + '#' + message.author.discriminator, "Time" : time }
            collection.update_one({'uid': uid }, {'$push': {'messages': message_data}})
            update_count = {"$inc" : { "Count" : 1}}
            owner = {"uid": int(uid) }
            collection.update_one(owner, update_count)


            search = collection.find(owner, RemoveID)
            for total in search:
                print('#############################################################################################')
                print(total)
                print(total['Count'])
                Count = (total['Count'])

                print(total['TicketName'])
                TicketName = total['TicketName']
                print('#############################################################################################')



            # DM user with moderators response
            print(uid)
            user = await self.bot.fetch_user(uid)
            print(user) # Debug data
            DM = await user.create_dm()

            # The moderator name is public

            embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
            await DM.send(embed=embedVar)

