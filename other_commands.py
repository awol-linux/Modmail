from discord.ext import commands
import discord
import mongo 
log_channel_id = 797996052074201088
class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.has_permissions(administrator=True)
    @commands.command(name='close', help='Archives the complaint putting a full log in admin log')
    async def clear(self, ctx):
        TicketName = ctx.channel.name
        embedVar = discord.Embed(title=TicketName, inline=False)
        for message in mongo.search.get_messages_by_tickets(TicketName):
            embedVar.add_field(name=message['author'] + '\n' + message['Time'], value=message['content'] , inline=False)

        admin_log = await self.bot.fetch_channel(log_channel_id)
        owner = await self.bot.fetch_user(mongo.search.get_owner(TicketName))
        await owner.send(content=f'Hey {owner.name} {TicketName} has been closed here is a transcript. Please feel free to contact us if necessary', embed=embedVar)
        mongo.search.archive_channel(TicketName)
        await admin_log.send(embed=embedVar)
        await ctx.channel.delete()
    
#    @commands.command(name='fs', help='have the bot send the user a friend request')
#    async def sf(self, ctx):
#        await ctx.author.send_friend_request()
