# bot.py
import os
import random
import yaml
import jsons

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

TicketNumber = 0
tickets = {}

@client.event
async def on_message(message):
    print(message)
    # verify that the bot doesn't respond to itself
    if message.author == client.user:
        return
    # debug data
    print(message.channel.type)
    print(type(message.channel.type))
    # verify that message was sent via DM/PM
    if str(message.channel.type) == "private":
            guild = discord.utils.get(client.guilds)
            print(guild)
            response = 'How can I Help you'
            global tickets
            global TicketNumber
            global msgnumber
            # Check if user has submitted complaints in the past
            print(tickets.keys())
            if message.author.id not in tickets.keys():
                msgnumber = 0
                TicketNumber = int(TicketNumber) + 1
                TicketName = f'ticket-' + str(TicketNumber)
                # initilize ticket
                tickets.update({message.author.id: {
                        "count" : msgnumber,
                        "author": message.author.name + '#' + message.author.discriminator,
                        "TicketNumber": TicketNumber,
                        "TicketName" : 'ticket-' + str(TicketNumber)
                        }})

            print(msgnumber)
            msgnumber = int(tickets[message.author.id]['count']) + 1
            tickets[message.author.id]['count'] = msgnumber 
            ticketNumber = int(tickets[message.author.id]['TicketNumber'])
            TicketName = tickets[message.author.id]['TicketName']
            channel = discord.utils.get(guild.text_channels, name=TicketName)
            catagory = "mod"
            if channel is None:
                await guild.create_text_channel(TicketName, catagory=catagory)
            tickets[message.author.id].update({ msgnumber: {"content": message.content,}})
            print(tickets[message.author.id])
            print(message)
            channel = discord.utils.get(guild.text_channels, name=TicketName)
            jsons.dump(tickets)
            await channel.send(message.content)
            embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
            admin_log = client.get_channel(797996052074201088)
            await admin_log.send(embed=embedVar)
    else:
            return 

client.run(TOKEN)
