# bot.py
import os
import random
import yaml

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

ticketNumber = 1
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.channel.type)
    print(type(message.channel.type))
    if str(message.channel.type) == "private":
            guild = discord.utils.get(client.guilds)
            response = 'How can I Help you'
            global ticketNumber
            TicketName = f'ticket-' + str(ticketNumber)
            print(TicketName)
            guild.create_text_channel(TicketName)
            ticketNumber = int(ticketNumber) + 1
            channel = discord.utils.get(guild.text_channels, name=TicketName)
            message.channel.send(message)
            channel.send(message.content)
            embedVar = discord.Embed(title=message.author.name + '#' + message.author.discriminator,description=message.content ,inline=False)
            admin_log = client.get_channel(797996052074201088)
            await admin_log.send(embed=embedVar)
            


    else:
            return 

client.run(TOKEN)
