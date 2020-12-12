import discord
from discord.ext import commands
import asyncio
import random
import time
import json
import requests
from discord.ext import *
from serpapi import GoogleSearchResults
from googlesearch import search
from concurrent.futures import ThreadPoolExecutor
import gtr
from collections import Counter
from googletrans import Translator, LANGUAGES

color = 0x75aef5
gtr = Translator()

class General(commands.Cog):
    def __init__(self, dualipa):
        self.bot = dualipa

    @commands.command()
    async def translate(self, ctx, *args):
        wait = await ctx.send('Please wait...')
        args = list(args)
        if len(args) > 0:
            if args[0] == '--list':
                lang = ''
                for bahasa in LANGUAGES:
                    lang = lang + str(bahasa) + ' (' + str(LANGUAGES[bahasa]) + ')\n'
                embed = discord.Embed(title='List of languages', description=str(lang), colour=color)
                await wait.edit(content='', embed=embed)
            elif len(args) > 1:
                destination = args[0]
                toTrans = ' '.join(args[1:len(args)])
                translation = gtr.translate(toTrans, dest=destination)
                embed = discord.Embed(description=translation.text, colour=color)
                embed.set_footer(text=f'Translated {LANGUAGES[translation.src]} to {LANGUAGES[translation.dest]}.')
                await wait.edit(content='', embed=embed)
            else:
                await wait.edit(
                    content=f'¡Add a language! To look at the list amd it`s identification, write \n` {ctx.prefix}translate --list`.')
        else:
            await wait.edit(
                content=f'Add translations or \nUse the command `{ctx.prefix}translate --list` para los idiomas admitidos.')

def setup(bot):
    bot.add_cog(General(bot))