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

# bot = commands.Bot(command_prefix='&')
class search(commands.Cog):     
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.has_role(789329882605813760)
    @commands.command(name='ticket_search', help='Type in the search you want to use can be -before -after -author and term is the search term')
    async def ticket_search(self, ctx, ticket_name):
        RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}
        ticket_list = ticket_first[ticket_name]
        address = { "uid" : {"$exists" : "true" } }
        query = ticket_list.find(address)
        for ticket in query:
            print('query result = ' + str(ticket['uid']))
            uid = ticket['uid']
        collection = ticket_first[ticket_name]
        owner = {"uid": int(uid)}
        search = collection.find(owner, RemoveID)
        embedVar = discord.Embed(title=ticket_name, inline=False)
        for total in search:
            for log in total['messages']:
                embedVar.add_field(name=log['author'] + '\n' + log['Time'], value=log['content'] , inline=False)
                print(log)
        admin_log = await self.bot.fetch_channel(797996052074201088)
        print(admin_log)
        await admin_log.send(embed=embedVar)

    @commands.has_role(789329882605813760)
    @commands.command(name='user_search', help='Type in the search you want to use can be -before -after -author and term is the search term')
    async def user_search(self, ctx, user):
        userlist = user_first[str(user)].find( { 'TicketName': { '$exists' : "true" }} )
        print(userlist)
        for ticket in userlist:
            print(ticket)
            RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}
            ticket_list = ticket_first[ticket['TicketName']]
            embedVar = discord.Embed(title=ticket['TicketName'], inline=False)
            collection = ticket_first[ticket['TicketName']]
            owner = {"uid": int(user)}
            search = collection.find(owner, RemoveID)
            for total in search:
                    for log in total['messages']:
                        embedVar.add_field(name=log['author'] + '\n' + log['Time'], value=log['content'] , inline=False)
                        print(log)
            admin_log = await self.bot.fetch_channel(797996052074201088)
            print(admin_log)
            await admin_log.send(embed=embedVar)

    @commands.has_role(789329882605813760)
    @commands.command(name='mod_search', help='Type in the search you want to use can be -before -after -authopr and term is the search term')
    async def mod_search(self, ctx, user):
        userid = await self.bot.fetch_user(user)
        username = userid.name + '#' + userid.discriminator
        print(username)
        for ticket in sorted(ticket_first.list_collection_names()):
            embedVar = discord.Embed(title=ticket, inline=False)
            for total in ticket_first[ticket].find({ 'messages.author' : username }):
               found_message = False 
               for log in total['messages']:
                   embedVar.add_field(name=log['author'], value=log['content'] , inline=False)
                   found_message = True
                   print(log)
               if found_message:
                   admin_log = await self.bot.fetch_channel(797996052074201088)
                   await admin_log.send(embed=embedVar)
      
