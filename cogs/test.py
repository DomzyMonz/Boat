import discord
from discord.ext import commands

class Test(commands.Cog):
  def __init__(self, client):
    self.client = client

  #events
  @commands.Cog.listener()
  async def on_ready(self):
      print('Bot joined/Updated successfully!')

  #commands
  @commands.command()
  async def ping (self, ctx):
    await ctx.send ('Pong!')
  
  @commands.command()
  async def say (self, ctx, message):
    await ctx.send (message)

def setup(client):
  client.add_cog(Test(client))