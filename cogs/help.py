import discord
import json
import asyncio
from discord.ext import commands
import datetime

class Home(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help(self, ctx):
    help_emb = discord.Embed(
      color = 0xffcd75
    )
    help_emb.set_author(
      name = f'Requested by: {str(ctx.author)}',
      icon_url = ctx.author.avatar_url
    )
    fields = [
      ('Call', 'Call other users or servers!', False),
      ('Info', 'Access user, guild, and server info!', False),
      ('')
    ]
    await ctx.send(embed=help_emb)

def setup(bot):
  bot.add_cog(Home(bot))
  print ('Loaded Help Cog Successfully!')