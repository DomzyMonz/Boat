import discord
import json
import asyncio
from discord.ext import commands
import datetime

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def help2(self, ctx, cmd:str=None):
    prefix = ctx.message.content[:2]
    command = commands.Bot.get_command(self.bot,cmd)
    cmd_list = [str(command)]
    if len(cmd_list) != 1:
      for _ in command.aliases:
        cmd_list.append(_)
      cmd_syn = f'[{"|".join(cmd_list)}]'
    else:
      cmd_syn = cmd_list[0]
    cmd_syn = f'```{prefix}{cmd_syn} {(command.signature)}```'
    await ctx.send(command.description or command.name)
    await ctx.send(cmd_syn)

  @commands.command()
  async def help3(self, ctx, page:int=1):
    command_list = []
    for command in self.bot.commands:
      if not command.hidden:
        if len(command.aliases) != 0:
          cmd_syn = f"{ctx.prefix}[{command.name}|{'|'.join([i for i in command.aliases])}] {command.signature}"
        else:
          cmd_syn = f"{ctx.prefix}{command.name} {command.signature}"
        command_list.append((command.name, cmd_syn))
    page = page
    message = await ctx.send(embed = discord.Embed(title = 'Sending...'))
    while True:
      start=page*10-10
      end=page*10
      embed = discord.Embed(
        title = f"Commands: Page {page} of {(len(command_list) // 10) + 1}")
      for _ in command_list[start:end]:
        embed.add_field(
          name = _[0],
          value = f'```{_[1]}```',
          inline=False
        )
      await message.edit(embed = embed)
      reactions = ['⬅️', '➡️']
      if page == (len(command_list) // 10) + 1:
        reactions.remove('➡️')
      if page == 1:
        reactions.remove('⬅️')
      for i in reactions:
        await message.add_reaction(i)
      def check (reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) in reactions and user == ctx.author
      reaction = await self.bot.wait_for('reaction_add', check=check)
      page += -1 if str(reaction[0]) == '⬅️' else 1
      await message.clear_reactions()

  @commands.command()
  async def help4(self, ctx):
    for _ in self.bot.cogs:
      _ = self.bot.get_cog(_)
      for __ in _.walk_commands():
        await ctx.send(f'{ctx.prefix}{__} {__.signature}')

def setup(bot):
  bot.add_cog(Help(bot))
  print ('Loaded Help Cog Successfully!')