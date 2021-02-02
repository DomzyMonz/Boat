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
    ch_mute = False
    dm_mute = False
  #------ Embed for Channel ------#
    call_emb = discord.Embed(title=f'Calling {member.display_name}',color=0xffcd75)
    call_emb.set_footer(text='React ❌ to cancel the call.')
    call_msg = await ctx.send(embed = call_emb)
  #------ Contact Channel ------#
    try:
      dm = await member.create_dm()
    except:
      bad_emb = discord.Embed(title=f'Failed to call {member.display_name}',color=0xb13e53)
      bad_emb.set_footer(text='The recipient of this call might be the bot, or an error of the bot.')
      await call_msg.edit(embed=bad_emb)
      return
  #------ Author Channel ------#
    channel = self.bot.get_channel(ctx.channel.id)
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
    while call:
      try:
  #------ Wait for Member Response ------#
        def accept_check(m):
          return(m.author.bot == False)
        message= await self.bot.wait_for("message",check=accept_check,timeout=600)
        duration=(datetime.datetime.now()-start).total_seconds()
  #------- Settings - DM -------#
        if message.content == 'b?settings' and (str (message.channel.type) == 'private' or (message.channel == channel)):
          if str(message.channel.type) == 'private':
            embed = discord.Embed (
              title = 'Settings',
              description = 'React using the corresponding emojis to toggle the settings',
              color = 0xffcd75

            )
            fields = [
              (':mute: Mute :mute:', f'Muted = {dm_mute}',
              True),
              (':envelope: End :envelope:', 'Ends call.', True),
              (':arrow_backward: Back :arrow_backward:', '-------------', True)
            ]
            for name, value, inline in fields:
              embed.add_field(
                name = name,
                value = value,
                inline = inline
              )
            reactions = ['🔇','✉️','📻','◀️']
            setting = await dm.send (embed = embed)
            for reaction in reactions:
              await setting.add_reaction(reaction)
            def reaction_check(reaction, user):
              return (reaction.message.id and str(reaction.emoji) in reactions and user == member)
            setting_r = await self.bot.wait_for("reaction_add",check=reaction_check)
  #------ Mute ------#
            if str(setting_r[0]) == '🔇':
              dm_mute = not dm_mute
              await setting.delete ()
              embed = discord.Embed (
                title = f'Mute = {dm_mute}',
                color = 0xffcd75
              )
              await dm.send (embed = embed)
  #------ New End ------#
            elif str(setting_r[0]) == '✉️':
              await setting.delete()
              confirm_emb = discord.Embed(
                title = 'End?',
                color = 0xffcd75
              )
              confirm = await channel.send(embed = confirm_emb)
              reactions = ['☑️', '❎']
              for reaction in reactions:
                await confirm.add_reaction(reaction)
              def reaction (reaction, user):
                return (reaction.message.id) == confirm.id and (user.bot == False) and str(reaction.emoji) in reactions
              end_confirm = await self.bot.wait_for("reaction_add",check=reaction)
              if str(end_confirm[0]) == '☑️':
                show_duration = True
                break
              else:
                await confirm.delete ()
                embed = discord.Embed(
                  title = f'{end_confirm[1].name} declined to end the call.',
                  color = 0xffcd75
                )
                await dm.send(embed = embed)
  #------ Back ------#
            elif str(setting_r[0]) == '◀️':
              await setting.delete ()
  #------ Settings - Channel ------#
          else:
            embed = discord.Embed (
              title = 'Settings',
              description = 'React using the corresponding emojis to toggle the settings',
              color = 0xffcd75
            )
            fields = [
              (':mute: Mute :mute:', f'Muted = {ch_mute}',
              True),
              (':envelope: End :envelope:', 'Ends call.', True),
              (':arrow_backward: Back :arrow_backward:', '-------------', True)
            ]
            for name, value, inline in fields:
              embed.add_field(
                name = name,
                value = value,
                inline = inline
              )
            reactions = ['🔇','✉️','📻','◀️']
            setting = await channel.send (embed = embed)
            for reaction in reactions:
              await setting.add_reaction(reaction)
            def reaction_check(reaction, user):
              return (reaction.message.id and str(reaction.emoji) in reactions and user == member)
            setting_r = await self.bot.wait_for("reaction_add",check=reaction_check)
  #------ Mute ------#
            if str(setting_r[0]) == '🔇':
              ch_mute = not ch_mute
              await setting.delete ()
              embed = discord.Embed (
                title = f'Mute = {ch_mute}',
                color = 0xffcd75
              )
              await channel.send (embed = embed)
  #------ New End ------#
            elif str(setting_r[0]) == '✉️':
              await setting.delete()
              confirm_emb = discord.Embed(
                title = 'End?',
                color = 0xffcd75
              )
              confirm = await dm.send(embed = confirm_emb)
              reactions = ['☑️', '❎']
              for reaction in reactions:
                await confirm.add_reaction(reaction)
              def reaction (reaction, user):
                return (reaction.message.id) == confirm.id and (user.bot == False) and str(reaction.emoji) in reactions
              end_confirm = await self.bot.wait_for("reaction_add",check=reaction)
              if str(end_confirm[0]) == '☑️':
                show_duration = True
                break
              else:
                await confirm.delete ()
                embed = discord.Embed(
                  title = f'{end_confirm[1].name} declined to end the call.',
                  color = 0xffcd75
                )
                await channel.send(embed = embed)
  #------ Back ------#
            elif str(setting_r[0]) == '◀️':
              await setting.delete ()
        elif message.author == member and str(message.channel.type) == "private":
          if dm_mute == False:
            await channel.send(f"**{message.author.display_name}#{message.author.discriminator} :**\n{message.content}")
            counter = counter + 1
        elif message.channel == channel:
          if ch_mute == False:
            await dm.send(f"**{message.author.display_name}#{message.author.discriminator} :**\n{message.content}")
            counter = counter + 1
  #------ No Response ------#
      except asyncio.TimeoutError:
        start_emb = discord.Embed(title='Waiting too long', description='No message was sent for more then 10 minutes.',color=0x73eff7)
        await channel.send(embed=start_emb)
        await dm.send(embed=start_emb)
        show_duration = True
        break
  #------ End Embed ------#
    if show_duration == True:
      end_emb = discord.Embed(title='Call ended', description=f'{message.author.mention} ended the call..',color=0x73eff7)
      end_emb.add_field(name = 'Duration', value = f'Duaration: {str(duration)[:-3]}s')
      end_emb.add_field(name = 'Messages', value = f'Messages: {counter} messages')
      await channel.send(embed=end_emb)
      await dm.send(embed=end_emb)

def setup(bot):
  bot.add_cog(Ex(bot))