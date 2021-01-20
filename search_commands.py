import discord
from discord.ext import commands
import mongo

log_channel_id = 801221657792479242
class search(commands.Cog):     
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.has_permissions(administrator=True)
    @commands.command(name='ticket_search', help='Type in the search you want to use can be -before -after -author and term is the search term')
    async def ticket_search(self, ctx, ticket_name):
        embedVar = discord.Embed(title=ticket_name, inline=False)
        for message in mongo.search.get_messages_by_tickets(ticket_name):
            embedVar.add_field(name=message['author'] + '\n' + message['Time'], value=message['content'] , inline=False)

        admin_log = await self.bot.fetch_channel(log_channel_id)
        await admin_log.send(embed=embedVar)

    @commands.has_permissions(administrator=True)
    @commands.command(name='user_search', help='Type in the search you want to use can be -before -after -author and term is the search term')
    async def user_search(self, ctx, user):
        for TicketName in mongo.search.all_tickets_for_user(user):
            embedVar = discord.Embed(title=TicketName, inline=False)
            message_logs = mongo.search.get_messages_by_tickets(TicketName)
            for message in message_logs:
                embedVar.add_field(name=message['author'] + '\n' + message['Time'], value=message['content'] , inline=False)
            admin_log = await self.bot.fetch_channel(log_channel_id)
            await admin_log.send(embed=embedVar)

    @commands.has_permissions(administrator=True)
    @commands.command(name='mod_search', help='Type in the search you want to use can be -before -after -authopr and term is the search term')
    async def mod_search(self, ctx, user):
        usero = await self.bot.fetch_user(user)
        username = usero.name + '#' + usero.discriminator
        for ticket in mongo.search.all_messages_by_user(username):
            TicketName = ticket['TicketName']
            embedVar = discord.Embed(title=TicketName, inline=False)
            for message in ticket['messages']:
                embedVar.add_field(name=message['author'] + '\n' + message['Time'], value=message['content'    ] , inline=False)
            admin_log = await self.bot.fetch_channel(log_channel_id)
            await admin_log.send(embed=embedVar)
