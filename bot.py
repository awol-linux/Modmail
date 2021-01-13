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



client = discord.Client()
filename = 'test'

TicketNumber = 0
tickets = {} 
print(tickets)

# some startup Debug information and set status to watching DMs
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='DM for complaints'))    
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


# main function
@client.event
async def on_message(message):
    collection = db[str(message.author.id)]
    print(message)
# verify that the bot doesn't respond to itself
    if message.author == client.user:
        return

    # debug data
    print(message.channel.type)
    print(type(message.channel.type))

    # check to see if message was sent to bot via DM
    if str(message.channel.type) == "private":
        guild = discord.utils.get(client.guilds)
        print(guild)

        # initilize ticket if user hasn't created one yet
        user_info = {
                "uid" : message.author.id,
                "author": message.author.name + '#' + message.author.discriminator,
                "channel": message.channel.id,
                "TicketNumber": TicketNumber,
                "TicketName" : 'ticket-' + str(TicketNumber)
                }
        collection.insert_one(user_info)

        query = {"uid": message.author.id }
        update = {"$inc" : { "count" : 1}}
        collection.update_one(query, update)

        channel = discord.utils.get(guild.text_channels, name=TicketName)
        catagory = discord.utils.get(guild.categories, id=798284727794270229)

        # verify ticket has appropiate channel
        if channel is None:
            await guild.create_text_channel(TicketName, category=catagory)

        # Log message 
        collection.insert_one({ 
            str(msgnumber): {
                "content": message.content,
                "author": message.author.name + '#' + message.author.discriminator, 
                }})
       

        # Debug data
        for result in collection.find(query):
            print(result)

        # Send message in channel
        await channel.send(message.content)

        # Log into admin log with message, username and discriminator
        embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
        admin_log = client.get_channel(797996052074201088)
        await admin_log.send(embed=embedVar)
           

    # If message is in ticket catagoru\y
    elif message.channel.category_id == 798284727794270229:

        # Figure out whose ticket it was
        for ticket in tickets:
            if tickets[ticket]['TicketName'] == message.channel.name:

               # DM user with moderators response 
               user = await client.fetch_user(ticket)
               print(user) # Debug data
               DM = await user.create_dm()

               # The moderator name is public

               embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
               await DM.send(embed=embedVar)


               # Log message 
               msgnumber = int(tickets[ticket]['count']) + 1
               tickets[ticket]['count'] = msgnumber 
               ticketNumber = int(tickets[ticket]['TicketNumber'])
               TicketName = tickets[ticket]['TicketName']
               tickets[ticket].update({ msgnumber: {"content": message.content, "author": message.author.name + '#' + message.author.discriminator, }})

               # Debug data
               print(tickets[ticket])

client.run(TOKEN)
