import discord
from discord.ext import commands
import mongo

command_channel_id = 797996052074201088
class search(commands.Cog):     
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

#    @commands.has_permissions(administrator=True)
    @commands.command(name='ticket_search', help='Type in the search you want to use can be -before -after -author and term is the search term')
    async def ticket_search(self, ctx, TicketName):
        admin_log = await self.bot.fetch_channel(command_channel_id)
        count = 0
        embedVar = discord.Embed(title=TicketName, inline=False)
        for message in mongo.search.get_messages_by_tickets(TicketName):
            if count > 25:
                await admin_log.send(embed=embedVar)
                count = 1
                embedVar = discord.Embed(title=TicketName + '(cont)', inline=False)
            if len(message['content']) > 1000:
                embedVar.add_field(name=message['author'] + '\n' + message['Time'], value=message['content'][0:1000], inline=False)
                embedVar.add_field(name=message['author'] + ' (cont)', value=message['content'][1000:2005] , inline=False)
            else:
                embedVar.add_field(name=message['author'] + '\n' + message['Time'], value=message['content'] , inline=False)
                count = count + 1
            await admin_log.send(embed=embedVar)

    @commands.has_permissions(administrator=True)
    @commands.command(name='user_search', help='Type in the search you want to use can be -before -after -author and term is the search term')
    async def user_search(self, ctx, user):
        for TicketName in mongo.search.all_tickets_for_user(user):
            print(TicketName)
            await self.ticket_search(ctx, TicketName)

    @commands.has_permissions(administrator=True)
    @commands.command(name='mod_search', help='Type in the search you want to use can be -before -after -authopr and term is the search term')
    async def mod_search(self, ctx, user):
        user_object = await self.bot.fetch_user(user)
        username = user_object.name + '#' + user_object.discriminator
        for ticket in mongo.search.all_messages_by_user(username):
            TicketName = ticket['TicketName']
            await self.ticket_search(ctx, TicketName)
