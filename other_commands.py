from discord.ext import commands
from pymongo import MongoClient
import discord
from dotenv import load_dotenv
import os

# mongo data
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PASS = os.getenv('MONGO_PASSWORD')
USER = os.getenv('MONGO_USER')
mdbclient = MongoClient('172.20.0.10', 27017, username=USER, password=PASS)
ticket_first = mdbclient['tickets']
user_first = mdbclient['userid']



class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.has_role(789329882605813760)
    @commands.command(name='close', help='Archives the complaint putting a full log in admin log')
    async def clear(self, ctx):
         RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}
         ticket_list = ticket_first[ctx.channel.name]
         address = { "uid" : {"$exists" : "true" } } 
         query = ticket_list.find(address)
         for ticket in query:
             print('query result = ' + str(ticket['uid']))
             uid = ticket['uid']
         collection = ticket_first[ctx.channel.name]
         owner = {"uid": int(uid)}
         deactivate = { '$set': { 'status' : 'closed' } } 
         search = collection.find(owner, RemoveID)
         embedVar = discord.Embed(title=ctx.channel.name, inline=False)
         for total in search:
             for log in total['messages']:
                 embedVar.add_field(name=log['author'], value=log['content'] , inline=False)
                 print(log)
         admin_log = await self.bot.fetch_channel(797996052074201088)
         print(admin_log)
         await admin_log.send(embed=embedVar)
         user_first[str(uid)].update({'status' : 'active' }, deactivate)
         await ctx.channel.delete()
    
    @commands.command(name='fs', help='have the bot send the user a friend request')
    async def sf(self, ctx):
        await ctx.author.send_friend_request()
