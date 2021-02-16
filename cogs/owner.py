import discord
from discord.ext import commands
import requests
import os
from os import listdir
from os.path import isfile, join

class Owner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases = ['rd', 'readdirs', 'readdirectory', 'readdirectories'])
  @commands.is_owner()
  async def read(self, ctx, *, message):
    await ctx.message.delete()
    message = open(message, 'r').read()
    message = message.replace("```", "`‌`‌`")
    await ctx.send(f"```py\n{message}\n```")

  @commands.command(aliases = ['filesread', 'fr'])
  @commands.is_owner()
  async def fileread(self, ctx, path:str='./'):
    await ctx.message.delete()
    description = f'Current Directory: {path}\n/'
    for f in listdir(path):
      if isfile(join(path, f)):
        description = join(description, f'\📄 {f}\n')
      else:
        description = join(description, f'\📁 {f}\n')
    embed = discord.Embed(
      title = 'Files',
      description = description
    )
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Owner(bot))
  print ('Loaded Owner Cog Successfully!')