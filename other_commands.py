from discord.ext import commands
import discord
import mongo
from difflib import get_close_matches
settings = mongo.settings()
log_channel_id = settings.get('log_channel_id')

def setup(bot):
    bot.add_cog(admin(bot))
    bot.add_cog(settings_commands(bot))

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
            await ctx.reply('The ticket owner has left the server. Please use force_close')
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
        await admin_log.send(embed=embedVar)
        mongo.search.archive_channel(TicketName)
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



class settings_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.has_permissions(administrator=True)
    @commands.command(name='lookup', help='Shows the closest settings and their value')
    async def lookup(self, ctx, arg):
        settingkeys = []
        for setting in settings.print_all():
            settingkeys.append(setting['name'])
        embedVar = discord.Embed(title='Settings', inline=False)
        matches = (get_close_matches(arg, settingkeys))
        for match in matches:
            embedVar.add_field(name=match + ' = ' + str(settings.get(match)), value=settings.get_description(arg), inline=False)
        await ctx.reply(embed=embedVar)

    @commands.has_permissions(administrator=True)
    @commands.command(name='set', help='Changes the value of a setting')
    async def set(self, ctx, arg1, arg2 , *args):
        embedVar = discord.Embed(title='Settings', inline=False)
        update = settings.update(arg1, arg2)
        if update:
            embedVar.add_field(name='Old', value=update['oldkey'], inline=True)
            embedVar.add_field(name='New', value=update['newkey'], inline=True)
            embedVar.add_field(name='Description', value=settings.get_description(arg1))
            await self.reload(ctx)
            await ctx.reply(embed=embedVar, content='reloaded')
        else:
            await ctx.reply(f"{arg1} didn't have any results. Try {settings.get('prefix')}lookup {arg1} to search.")

    @commands.has_permissions(administrator=True)
    @commands.command(name='reload', help='Manually reload config')
    async def reload(self, ctx):
        await ctx.channel.send(ctx.command)
        self.bot.reload_extension('other_commands')
        self.bot.reload_extension('search_commands')
        self.bot.reload_extension('category_listener')
        self.bot.reload_extension('DM_listener')
        self.bot.command_prefix = settings.get('prefix')
        if str(ctx.command) == 'reload':
            await ctx.reply('reloaded')

    @commands.has_permissions(administrator=True)
    @commands.command(name='show', help='Shows the settings and their value')
    async def show(self, ctx):
        settingkeys = []
        embedVar = discord.Embed(title='Settings', inline=False)
        for setting in settings.print_all():
            embedVar.add_field(name=setting['name'] + ' = ' + str(setting['value']), value=setting['Description'], inline=False)
        await ctx.reply(embed=embedVar)


class help(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)
