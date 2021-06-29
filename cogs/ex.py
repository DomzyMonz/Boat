import discord
import json
import asyncio
from discord.ext import commands
import datetime

class Ex(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def membercall(self, ctx, member:discord.User):
    await member.send('Calling...')
  
  @commands.command()
  async def profile(self, ctx):
    await ctx.send(ctx.author.profile())

def setup(bot):
  bot.add_cog(Ex(bot))
  print ('Loaded Experiment Cog Successfully!')