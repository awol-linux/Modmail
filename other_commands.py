from discord.ext import commands
import discord
import mongo
log_channel_id = 801221657792479242 
class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.has_permissions(administrator=True)
    @commands.command(name='close', help='Archives the complaint putting a full log in admin log')
    async def close(self, ctx):
        TicketName = ctx.channel.name
        owner = await self.bot.fetch_user(mongo.search.get_owner(TicketName))
        try:
            await owner.send(content=f'Hey {owner.name} {TicketName} has been closed here is a transcript. Please feel free to contact us if necessary')
        except:
            await ctx.reply('owner has left the server please use force_close')
            return
        count = 0
        embedVar = discord.Embed(title=TicketName, inline=False)
        admin_log = await self.bot.fetch_channel(log_channel_id)
        for message in mongo.search.get_messages_by_tickets(TicketName):
            if count > 25:
                await admin_log.send(embed=embedVar)
                await owner.send(embed=embedVar)
                count = 1
                embedVar = discord.Embed(title=TicketName + '(cont)', inline=False)
            if len(message['content']) > 1000:
                embedVar.add_field(name=message['author'] + '\n' + message['Time'], value=message['content'][0:1000], inline=False)
                embedVar.add_field(name=message['author'] + ' (cont)', value=message['content'][1000:2005] , inline=False)
            else:
                embedVar.add_field(name=message['author'] + '\n' + message['Time'], value=message['content'] , inline=False)
                count = count + 1
        await owner.send(embed=embedVar)

        mongo.search.archive_channel(TicketName)
        await admin_log.send(embed=embedVar)
        await ctx.channel.delete()
    

    @commands.has_permissions(administrator=True)
    @commands.command(name='force_close', help='Archives the complaint putting a full log in admin log')
    async def force_close(self, ctx):
        TicketName = ctx.channel.name
        owner = await self.bot.fetch_user(mongo.search.get_owner(TicketName))
        count = 0
        embedVar = discord.Embed(title=TicketName, inline=False)
        admin_log = await self.bot.fetch_channel(log_channel_id)
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

        mongo.search.archive_channel(TicketName)
        await admin_log.send(embed=embedVar)
        await ctx.channel.delete()
