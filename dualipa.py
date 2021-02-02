import json
import logging
import os
import sys
import re
import json
import sys
import requests
import urllib.request
import os
import discord
from discord.ext import *
from discord.ext import commands
from discord.utils import oauth_url
import asyncio
import random

from utils.settings import Funcs, GlobalVars

globalVars = GlobalVars()
logging.getLogger('discord').setLevel(logging.CRITICAL)


globalVars = GlobalVars()
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.basicConfig(filename=globalVars.path + 'dualipa.log', level=logging.INFO, filemode='a', format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%d-%m-%Y:%H:%M:%S')

class dualipa(commands.Bot):
  def __init__(self):
    self.prefix = globalVars.prefix
    super().__init__(command_prefix=self.prefix)
    self.remove_command('help')

    for cog in globalVars.cogs:
      self.load_extension(cog)
      print('[INFO] {} loaded'.format(cog))

  async def on_ready(self):
    print('[INFO] Dua Lipa loaded')

  async def on_message(self, message):
    if message.author == self.user:
      return
    elif message.content.startswith('{}help'.format(self.prefix)):
      data = json.loads(Funcs().readFile(GlobalVars().path + 'db/commands.json'))
      msg = '```'
      for item in range(len(data)):
        msg += '{}{} - {}\n'.format(self.prefix, data[item]['command'], data[item]['info'])
      msg += '```'
      await message.channel.send(msg)
    else:
      await self.process_commands(message)

  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
      await ctx.send('The command `{}` do not exists!'.format(ctx.message.content.split()[0]))
    elif isinstance(error, commands.errors.MissingRequiredArgument):
      await ctx.send('That command `{}` requires more arguments'.format(ctx.message.content.split()[0]))


INSTAGRAM_USERNAME = "dualipa"  # Example: ladygaga
WEBHOOK_URL = ""  # Url to your discord webhook
DATABASE = "database.txt"


def write_to_file(content, filename):
  try:
    f = open(filename, "w")
    f.write(content)
    f.close()
  except IOError:
    print("Error occured trying to read the file " + filename + ".")


def read_from_file(filename):
  try:
    f = open(filename, "r")
    content = f.read()
    f.close()
    return content
  except IOError:
    print("Error occured trying to read the file " + filename + ".")


def get_user_fullname(html):
  return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
  return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
  return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html):
  return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html):
  return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html):
  return \
  html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][
    0]["node"]["text"]


def webhook(webhook_url, html):
  data = {}
  data["embeds"] = []
  embed = {}
  embed["color"] = 15467852
  embed["title"] = "New pic of @" + INSTAGRAM_USERNAME + ""
  embed["url"] = "https://www.instagram.com/p/" + get_last_publication_url(html) + "/"
  embed["description"] = get_description_photo(html)
  embed["image"] = {"url":get_last_thumb_url(html)} 
  embed["thumbnail"] = {"url": get_last_thumb_url(html)}
  data["embeds"].append(embed)
  result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
  try:
    result.raise_for_status()
  except requests.exceptions.HTTPError as err:
    print(err)
  else:
    print("Image successfully posted in Discod, code {}.".format(result.status_code))


def get_instagram_html(INSTAGRAM_USERNAME):
  html = requests.get("https://www.instagram.com/" + INSTAGRAM_USERNAME + "/?__a=1")
  return html


def main():
  try:
    html = get_instagram_html(INSTAGRAM_USERNAME)
    if (read_from_file(DATABASE) == get_last_publication_url(html)):
      print("Not new image to post in discord.")
    else:
      write_to_file(get_last_publication_url(html), DATABASE)
      print("New image to post in discord.")
      webhook(WEBHOOK_URL, get_instagram_html(INSTAGRAM_USERNAME))
  except:
    print("An error occured.")


if __name__ == "__main__":
  main()


bot = dualipa()
bot.run(globalVars.token)
