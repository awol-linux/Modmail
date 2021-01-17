# bot.py

import os
import yaml
import discord

from dotenv import load_dotenv
from pymongo import MongoClient

USER='root'
PASS='rootpassword'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

mdbclient = MongoClient('172.20.0.10', 27017 , username=USER, password=PASS)

db = mdbclient['tickets']
tn = mdbclient['userid']

client = discord.Client()

# some startup Debug information and set status to watching DMs
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='DM for complaints'))    
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


# main function

@client.event
async def on_message(message):
        #    print(message)
        #    verify that the bot doesn't respond to itself

    if message.author == client.user:
        return

        # debug data
        # print(message.channel.type)
        # print(type(message.channel.type))

        # check to see if message was sent to bot via DM
    if str(message.channel.type) == "private":

        getnumber = tn[str(message.author.id)]
        RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}

            # TicketNumber = 204
            # TicketName = 'test'

            # run a query to check for tickets

        find_old_tickets = getnumber.find({ "status" : "active"}, RemoveID)
        for ticket_found in find_old_tickets:

                # debugging data

            print(ticket_found)

                # only show active tickets

            if ticket_found['status'] ==  "active":
                print(tn.list_collection_names())
                TicketName = ticket_found['TicketName']
                print('Ticketname is ' + TicketName)

        # If there is no ticket created make a new one 
        amount = len(tn.list_collection_names()) + 1
        if 'TicketName' not in locals():
            print('couldnt find ticket')
            print(tn.list_collection_names())
            print('before ' + str(len(tn.list_collection_names())))
            TicketName = 'ticket-' + str(amount)
            user_info = {"TicketName": TicketName, "status" : "active", }
            print('78 getnumber.insert_one(user_info)')
            getnumber.insert_one(user_info)
            print(TicketName)
            print(tn.list_collection_names())
            print(len(tn.list_collection_names()))

        collection = db[str(TicketName)]
        
        guild = discord.utils.get(client.guilds)
        print(guild)

        # create vars to help query mongoDB
        author = {"uid": message.author.id }
        update_count = {"$inc" : { "Count" : 1}}
        RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}
        search = collection.find(author, RemoveID)

        # initilize ticket if user hasn't created one yet
        ticket_list = db.list_collection_names()
        print(ticket_list)
        if str(message.author.id) not in ticket_list:
        #            TicketCount = len(ticket_list)
        #            TicketName = 'ticket-' + str(TicketCount)
            print(TicketName)
            user_info = {
                "uid" : message.author.id,
                "author": message.author.name + '#' + message.author.discriminator,
                "channel": message.channel.id,
        #                "TicketNumber": TicketNumber,
                "TicketName" : TicketName,
                "messages" : []
                }
            
            print('111 collection.insert(user_info)')
            collection.insert(user_info)
            kp = tn[TicketName]
            kp.insert_one({"uid" : message.author.id})
            print('115 kp.insert_one({"uid" : message.author.id})')

        collection.update_one(author, update_count)

        # get total ticket count
        for total in search:
             print('#############################################################################################')
             print(total)
             # print(total['Count'])
             #Count = (total['Count'])
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

        # Log message 
        message_data = {"content": message.content, "author": message.author.name + '#' + message.author.discriminator }
        collection.update({'uid': message.author.id }, {'$push': {'messages': message_data}})
        # print(message_data)



        # Debug data
        for result in search:
            print(result)

        # Send message in channel
        await channel.send(message.content)

        # Log into admin log with message, username and discriminator
        embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
        admin_log = client.get_channel(797996052074201088)
        await admin_log.send(embed=embedVar)
           

    # If message is in ticket catagoru\y
    elif message.channel.category_id == 798284727794270229:
        return

        # Figure out whose ticket it was
    elif False:
               author = {"uid": message.author.id }
               address = { "uid" : {"$exists" : "true" } }
               RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}
               update_count = {"$inc" : { "Count" : 1}}
               kp = tn[message.channel.name]
               query = kp.find(address)
               for ticket in query:
                   print(ticket['uid'])
                   uid = ticket['uid']
               collection = db[str(uid)]

               search = collection.find(author, RemoveID)
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
               user = await client.fetch_user(uid)
               print(user) # Debug data
               DM = await user.create_dm()

               # The moderator name is public

               embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
               await DM.send(embed=embedVar)


               # Log message
               message_data = { "$set":{ str(Count):{
                    "content": message.content,
                    "author": message.author.name + '#' + message.author.discriminator, 
                    }}}
               collection.update_one(author, message_data)
               print(message_data)

               # Debug data

client.run(TOKEN)
