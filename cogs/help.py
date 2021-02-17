import discord
import json
import asyncio
from discord.ext import commands
import datetime

class Home(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help2(self, ctx, cmd:str=None):
    help_emb = discord.Embed(
      color = 0xffcd75
    )
    help_emb.set_author(
      name = f'Requested by: {str(ctx.author)}',
      icon_url = ctx.author.avatar_url
    )
    if cmd == None:
      fields = [
        ('Call', 'Call other users or servers!', False),
        ('Economy', 'Be richer than your friends!', False),
        ('Info', 'Access user, guild, and server info!', False),
      ]
    else:
      command = commands.Bot.get_command(self.bot,cmd)
      cmd_list = [str(command)]
      for _ in command.aliases:
        cmd_list.append(_)
      await ctx.send(command.signature)
      await ctx.send(commands.MinimalHelpCommand.get_command_signature(command(command)))
    for name, value, inline in fields:
      help_emb.add_field(
        name = name,
        value = value,
        inline = inline
      )
    await ctx.send(embed=help_emb)

def setup(bot):
  bot.add_cog(Home(bot))
  print ('Loaded Help Cog Successfully!')