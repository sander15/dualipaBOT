import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, dualipa):
        self.bot = dualipa

@commands.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

def setup(bot):
    bot.add_cog(General(bot))