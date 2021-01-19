import discord
from discord.ext import commands
from paramsGetter import getParams


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        params = getParams()
        embed = discord.Embed(
            title = '<:info:778627586976514058>  Choix des rôles  <:info:778627586976514058>',
            colour = discord.Colour.purple()
        )
        roles = params['roles']
        for role in roles:
            embed.add_field(name=role['roleName'], value=role['emoji'], inline=True)
        message = await ctx.send(embed=embed)
        for role in roles:
            await message.add_reaction(role['emoji'])

def setup(bot):
    bot.add_cog(Roles(bot))