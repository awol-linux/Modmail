# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

asdfqwert = discord.Client()

@asdfqwert.event
async def on_message(message):
    person = await asdfqwert.get_user(id=723183706054983721)
    print(person)
    await asdfqwert.send('�~_~Q')
asdfqwert.run(TOKEN)
