import discord
from discord.ext import commands

class Shop(commands.Cog):
  def __init__(self, client):
    self.client = client

  #events
  '''@commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.client.user:
      await message.channel.send(message.content)'''

def setup(client):
  client.add_cog(Shop(client))