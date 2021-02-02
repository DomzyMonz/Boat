import discord
import os
import re
import requests
import asyncio
import random
import datetime
from PIL import Image
from PIL import ImageColor
from discord.ext import commands

'''    activeservers = list(self.bot.guilds)
    servers=[]
    for activeserver in activeservers:
      servers.append(activeserver.name)'''

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def test(self, ctx):
    number = 1
    gap = 1
    message = await ctx.send(number)
    while True:
      reactions = ['⏪', '⏺' ,'⏩']
      for reaction in reactions:
        await message.add_reaction(reaction)
      def check (reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) in reactions and user == ctx.author
      reaction = await self.bot.wait_for('reaction_add', check=check)
      if str(reaction[0]) == '⏪':
        try:
          number = number - gap
          await message.remove_reaction(str(reaction[0]), ctx.author)
          await message.edit (content=number)
        except:
          await message.delete()
          message = await ctx.send(number)
      elif str(reaction[0]) == '⏩':
        try:
          number = number + gap
          await message.remove_reaction(str(reaction[0]), ctx.author)
        except:
          await message.delete()
          message = await ctx.send(number)
        await message.edit (content=number)
      else:
        try:
          await message.remove_reaction(str(reaction[0]), ctx.author)
          await message.delete()
          await ctx.send (number)
          break
        except:
          await message.delete()
          message = await ctx.send(number)
          break

  @commands.command()
  async def test2(self, ctx):
    server = requests.get('https://api.bedrockinfo.com/v1/status?server=jesser101.pocketmine.live&port=25573')
    js = server.json()
    embed = discord.Embed(title = 'HARDCORE SMP')
    embed.add_field(name="Server Name",value=re.sub(r"§[0-9A-GK-OR]","",js["ServerName"],count=0,flags=(re.I)),inline=False)
    embed.add_field(name="Online Players",value=js["Players"])
    embed.add_field(name="Max Players",value=js["MaxPlayers"])
    embed.add_field(name="Map Name",value=js["MapName"])
    embed.add_field(name="Default Gamemode",value=js["GameMode"],inline=False)
    embed.add_field(name="Minecraft Version",value=js["Version"])
    embed.add_field(name="Minecraft Server Timestamp",value=js["CheckTimestamp"])
    await ctx.send(embed=embed)#cool

    
def setup(client):
  client.add_cog(Fun(client))