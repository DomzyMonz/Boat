import discord
import json
import asyncio
from discord.ext import commands
import datetime

class Ex(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases = ['ct'])
  async def calltest(self, ctx, member:discord.Member):
  #------ Some Important Variables ------#
    counter = 0
    dm_mute = False
  #------ Server Channels ------#
    host_channel = self.bot.get_channel(ctx.channel.id)
    channels = [
      (self.bot.get_channel(ctx.channel.id), False)
      ]
  #------ Embed for Channel ------#
    call_emb = discord.Embed(title=f'Calling {member.display_name}',color=0xffcd75)
    call_emb.set_footer(text='React ❌ to cancel the call.')
    call_msg = await host_channel.send(embed = call_emb)
  #------ Contact Channel ------#
    try:
      dm = await member.create_dm()
    except:
      bad_emb = discord.Embed(title=f'Failed to call {member.display_name}',color=0xb13e53)
      bad_emb.set_footer(text='The recipient of this call might be the bot, or an error of the bot.')
      await call_msg.edit(embed=bad_emb)
      return
  #------ Embed for Member ------#
    dm_emb = discord.Embed(title=f'{ctx.author} is Calling...',description=f'{member.display_name} is calling you. You have 1 minute to answer.',color=0x73eff7)
    dm_emb.add_field(name='How to Answer',value='To answer, react ☑️ and react ❎ to decline a call.')
  #------ Reaction Answers ------#
    try:
      dm_call = await dm.send('', embed = dm_emb)
      reactions = ['☑️', '❎']
      await call_msg.add_reaction('❌')
      for reaction in reactions:
        await dm_call.add_reaction(reaction)
    except asyncio.TimeoutError:
      pass
  #------ Reaction Mechanism ------#
    try:
      def accept_check(reaction, user):
        return ((reaction.message.id and str(reaction.emoji) in reactions and user == member) or (str(reaction.emoji) == '❌' and user == ctx.author))
      reaction = await self.bot.wait_for("reaction_add",check=accept_check,timeout=60)
  #------ Decline ------#
      if str(reaction[0]) == '❎':
        await dm_call.delete()
        decline_emb = discord.Embed(title='Call not accepted', description=f'{member} did not accept the call.',color=0xb13e53)
        await call_msg.edit(embed=decline_emb)
        dm_call = await dm.send(embed=decline_emb)
        return
  #------ Accept ------#
      elif str(reaction[0]) == '☑️':
        await dm_call.delete()
        accept_emb = discord.Embed(title='Call accepted', description=f'{member} accepted the call.',color=0x38b764)
        await call_msg.edit(embed=accept_emb)
        dm_call = await dm.send(embed=accept_emb)
  #------ Cancel ------#
      elif str(reaction[0]) == '❌':
        await dm_call.delete()
        cancel_emb = discord.Embed(title='Canceled Call',color=0x333c57)
        await dm.send(embed = cancel_emb)
        await call_msg.clear_reactions()
        await call_msg.edit(embed = cancel_emb)
  #------ Ignore ------#
    except asyncio.TimeoutError:
      ignore_emb = discord.Embed(title='No Response', description=f'{member} did not answer.',color=0x1a1c2c)
      await dm_call.clear_reactions()
      await call_msg.edit(embed=ignore_emb)
      await dm_call.edit(embed=ignore_emb)
      return
  #------ Start Call ------#
    await call_msg.clear_reactions()
    call=True
    start=datetime.datetime.now()

def setup(bot):
  bot.add_cog(Ex(bot))
  print ('Loaded Experiment Cog Successfully!')