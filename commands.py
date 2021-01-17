from discord.ext import commands
import discord

class admin(commands.Cog):
    def __init__(self, client):
             self.client = client
    @commands.command(name='close', help='Archives the complaint putting a full log in admin log')
    async def clear(self, ctx):
        RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}
        ticket_list = ticket_first[ctx.channel.name]
        query = ticket_list.find(address)
        for ticket in query:
            print(ticket['uid'])
            uid = ticket['uid']
            collection = ticket_first[ctx.channel.name]
        owner = {"uid": int(uid) }
        search = collection.find(owner, RemoveID)
        for total in search:
             print(total)
