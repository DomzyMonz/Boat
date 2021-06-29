import discord
from discord.ext import commands
import requests
import os
import random
from os import listdir
from os.path import isfile, join
import random
from PIL import ImageDraw, ImageFont, Image, ImageColor
from ImageColor import getrgb

class Commands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(aliases = ['bec', 'mcbc'])
  async def mcbecommand(self, ctx, command):
    source = requests.get('https://raw.githubusercontent.com/Ersatz77/bedrock-data/master/generated/reports/commands.json')
    source = source.json()
    if 'redirect' in source['children'][command]:
      command = source['children'][command]['redirect'][0]
    await ctx.message.reply(source['children'][command])
  
def setup(bot):
  bot.add_cog(Commands(bot))
  print ('Loaded Commands Cog Successfully!')