from discord.ext import commands
import discord


class hi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
       await ctx.channel.send("hi")

    async def on_message(self, message):
        print(message.content)

def setup(bot):
    bot.add_cog(hi(bot))