import discord
from discord.ext import commands

class Call(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def call(self, ctx, member: discord.Member):
    call_emb = discord.Embed(title=f'Calling {member.display_name}',color=0xFFA500)
    call_msg = await ctx.send(embed = call_emb)
    try:
      dm = await member.create_dm()
    except:
      bad_emb = discord.Embed(title=f'Failed to call {member.display_name}',color=0x800000)
      await call_msg.edit(embed=bad_emb)
      return
    dm_emb = discord.Embed(title=f'{ctx.author} is Calling...',description=f'{member.display_name} is calling you. You have 1 minute to answer.',color=0xFFA500)
    dm_emb.add_field(name='How to Answer',value='To answer, reply `accept` or `answer`. To decline, ignore this message or type `decline`')
    try:
      dm_call = await dm.send('', embed = dm_emb)
    except discord.ext.commands.errors.CommandInvokeError:
      pass
    try:
      def accept_check(m):
        return(m.author==member and str(m.channel.type) == "private")
      message = await self.bot.wait_for("message",check=accept_check,timeout=60)
    except TimeoutError:
      start_emb = discord.Embed(title='No Response', description=f'{member} did not answer.',color=0x000000)
      await call_msg.edit(embed=start_emb)
      await dm_call.edit(embed=start_emb)
      return
    if message.content not in ["accept","answer"]:
      start_emb = discord.Embed(title='Call not accepted', description=f'{member} did not accept the call.',color=0x000000)
      await call_msg.edit(embed=start_emb)
      await dm_call.edit(embed=start_emb)
      return
    else:
      start_emb = discord.Embed(title='Call accepted', description=f'{member} accepted the call.',color=0x000000)
      await call_msg.edit(embed=start_emb)
      await dm_call.edit(embed=start_emb)
    call=True
    while call:
      try:
        def accept_check(m):
          return(m.author == member or m.author == ctx.author and str(m.channel.type) == "private")
        message= await self.bot.wait_for("message",check=accept_check,timeout=600)
        if message.content == "b?end":
          start_emb = discord.Embed(title='Call ended', description=f'{message.author.mention} ended the call..',color=0x000000)
          await call_msg.edit(embed=start_emb)
          await dm_call.edit(embed=start_emb)
          return
        elif message.author == member and str(message.channel.type) == "private":
          await ctx.send(f"**{message.author.display_name}#{message.author.discriminator} :**\n{message.content}")
        elif message.author == ctx.author:
          await dm.send(f"**{message.author.display_name}#{message.author.discriminator} :**\n{message.content}")
      except TimeoutError:
        start_emb = discord.Embed(title='Waiting too long', description=f'No message was sent for more then 10 minutes.',color=0x000000)
        await call_msg.edit(embed=start_emb)
        await dm_call.edit(embed=start_emb)
        return              




def setup(bot):
  bot.add_cog(Call(bot))