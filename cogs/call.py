import discord
import json
import asyncio
from discord.ext import commands
import datetime

class Call(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command(aliases=['usertelegraph', 'ut', 'us', 'usertele'])
  async def usercall(self, ctx, member: discord.Member):
    counter = 0
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
    except asyncio.TimeoutError:
      pass
    try:
      def accept_check(m):
        return(m.author==member and str(m.channel.type) == "private")
      message = await self.bot.wait_for("message",check=accept_check,timeout=60)
    except asyncio.TimeoutError:
      start_emb = discord.Embed(title='No Response', description=f'{member} did not answer.',color=0x000000)
      await call_msg.edit(embed=start_emb)
      await dm_call.edit(embed=start_emb)
      show_duration = False
      return
    if message.content not in ["accept","answer","hi","hello"]:
      start_emb = discord.Embed(title='Call not accepted', description=f'{member} did not accept the call.',color=0x800000)
      await call_msg.edit(embed=start_emb)
      await dm_call.edit(embed=start_emb)
      return
    else:
      start_emb = discord.Embed(title='Call accepted', description=f'{member} accepted the call.',color=0x288B22)
      await call_msg.edit(embed=start_emb)
      await dm_call.edit(embed=start_emb)
    call=True
    start=datetime.datetime.now()
    while call:
      try:
        def accept_check(m):
          return(m.author == member or m.author == ctx.author and str(m.channel.type) == "private")
        message= await self.bot.wait_for("message",check=accept_check,timeout=600)
        duration=(datetime.datetime.now()-start).total_seconds()
        if message.content == "b?end" and message.channel == ctx.channel:
          show_duration = True
          break
        elif message.content == "b?end" and str(message.channel.type) == "private":
          show_duration = True
          break
        elif message.author == member and str(message.channel.type) == "private":
          await ctx.send(f"**{message.author.display_name}#{message.author.discriminator} :**\n{message.content}")
          counter = counter + 1
        elif message.channel == ctx.channel:
          await dm.send(f"**{message.author.display_name}#{message.author.discriminator} :**\n{message.content}")
          counter = counter + 1
      except asyncio.TimeoutError:
        start_emb = discord.Embed(title='Waiting too long', description=f'No message was sent for more then 10 minutes.',color=0x00FFFF)
        await ctx.send(embed=start_emb)
        await dm.send(embed=start_emb)
        show_duration = True
        break
    if show_duration == True:
      end_emb = discord.Embed(title='Call ended', description=f'{message.author.mention} ended the call..',color=0x00FFFF)
      end_emb.add_field(name = 'Duration', value = f'Duaration: {str(duration)[:-3]}s')
      end_emb.add_field(name = 'Messages', value = f'Messages: {counter} messages')
      await ctx.send(embed=end_emb)
      await dm.send(embed=end_emb)

  @commands.command(aliases=['servertelegraph', 'sc', 'st', 'servertele'])
  async def servercall(self, ctx):
    servers=[]
    for activeserver in list(self.bot.guilds):
      if activeserver != ctx.guild:
        servers.append(activeserver)
    index = 0
    embed = discord.Embed(
      title = 'Select Server',
      description = 'Please select the server you want to call. You can do so by reacting with the corresponding emote.'
    )
    embed.add_field(
      name = f'{index + 1}: {servers[index].name}',
      value = f'ID: {servers[index].id}',
      inline = False
    )
    message = await ctx.send(embed=embed)
    while True:
      if index == 0:
        reactions = ['⏺' ,'⏩']
        add = ['🟦', '⏺' ,'⏩']
      elif index + 1 == len(servers):
        reactions = ['⏪', '⏺']
        add = ['⏪', '⏺', '🟦']
      else:
        reactions = ['⏪', '⏺' ,'⏩']
        add = reactions
      for reaction in add:
        await message.add_reaction(reaction)
      def check (reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) in reactions and user == ctx.author
      reaction = await self.bot.wait_for('reaction_add', check=check)
      if str(reaction[0]) == '⏪':
        index = index - 1
        embed = discord.Embed(
          title = 'Select Server',
          description = 'Please select the server you want to call. You can do so by reacting with the corresponding emote.'
        )
        embed.add_field(
          name = f'{index + 1}: {servers[index].name}',
          value = f'ID: {servers[index].id}',
          inline = False
        )
        try:
          await message.clear_reactions()
          await message.edit (embed = embed)
        except:
          await message.delete()
          message = await ctx.send(embed = embed)
      elif str(reaction[0]) == '⏩':
        index = index + 1
        embed = discord.Embed(
          title = 'Select Server',
          description = 'Please select the server you want to call. You can do so by reacting with the corresponding emote.'
        )
        embed.add_field(
          name = f'{index + 1}: {servers[index].name}',
          value = f'ID: {servers[index].id}',
          inline = False
        )
        try:
          await message.clear_reactions()
          await message.edit (embed = embed)
        except:
          await message.delete()
          message = await ctx.send(embed = embed)
      else:
        await message.delete()
        id = servers[index].id
        channels = []
        guild = self.bot.get_guild(id)
        for channel in guild.text_channels:
          channels.append(channel)
        index = 0
        embed = discord.Embed(
          title = 'Select Channel',
          description = 'Please select the channel you want to call. You can do so by reacting with the corresponding emote.'
        )
        embed.add_field(
          name = f'{index + 1}: {channels[index].name}',
          value = f'ID: {channels[index].id}',
          inline = False
        )
        message = await ctx.send(embed=embed)
        while True:
          if index == 0:
            reactions = ['⏺' ,'⏩', '🔙']
            add = ['🟦', '⏺' ,'⏩', '🔙']
          elif index + 1 == len(channels):
            reactions = ['⏪', '⏺', '🔙']
            add = ['⏪', '⏺', '🟦', '🔙']
          else:
            reactions = ['⏪', '⏺' ,'⏩', '🔙']
            add = reactions
          for reaction in add:
            await message.add_reaction(reaction)
          def check (reaction, user):
            return reaction.message.id == message.id and str(reaction.emoji) in reactions and user == ctx.author
          reaction = await self.bot.wait_for('reaction_add', check=check)
          if str(reaction[0]) == '⏪':
            index = index - 1
            embed = discord.Embed(
              title = 'Select Channel',
              description = 'Please select the channel you want to call. You can do so by reacting with the corresponding emote.'
            )
            embed.add_field(
              name = f'{index + 1}: {channels[index].name}',
              value = f'ID: {channels[index].id}',
              inline = False
            )
            try:
              await message.clear_reactions()
              await message.edit (embed = embed)
            except:
              await message.delete()
              message = await ctx.send(embed = embed)
          elif str(reaction[0]) == '⏩':
            index = index + 1
            embed = discord.Embed(
              title = 'Select Server',
              description = 'Please select the server you want to call. You can do so by reacting with the corresponding emote.'
            )
            embed.add_field(
              name = f'{index + 1}: {channels[index].name}',
              value = f'ID: {channels[index].id}',
              inline = False
            )
            try:
              await message.clear_reactions()
              await message.edit (embed = embed)
            except:
              await message.delete()
              message = await ctx.send(embed = embed)
          elif str(reaction[0]) == '⏺':
            await message.delete()
            id = channels[index].id
            break
            channel = self.bot.get_channel(id)
            counter = 0
            call_emb1 = discord.Embed(title=f'Calling **{channel.name}** from **{guild.name}**',color=0xFFA500)
            call_msg1 = await ctx.send (embed = call_emb1)
            call_emb2 = discord.Embed(title=f'**{ctx.channel.name}** is Calling...',description=f'**{ctx.channel.name}** from **{ctx.guild.name}** is calling you. You have 1 minute to answer.',color=0xFFA500)
            call_emb2.add_field(name='How to Answer',value='To answer, reply `accept` or `answer`. To decline, ignore this message or type `decline`')
            call_msg2 = await channel.send (embed = call_emb2)
            try:
              def accept_check(m):
                return(m.channel == channel)
              message = await self.bot.wait_for("message",check=accept_check,timeout=60)
            except asyncio.TimeoutError:
              start_emb = discord.Embed(title='No Response', description=f'{channel.name} did not answer.',color=0x000000)
              await call_msg1.edit(embed=start_emb)
              await call_msg2.edit(embed=start_emb)
              show_duration = False
              return
            if message.content not in ["accept","answer","hi","hello"]:
              start_emb = discord.Embed(title='Call not accepted', description=f'{channel.name} did not accept the call.',color=0x800000)
              await call_msg1.edit(embed=start_emb)
              await call_msg2.edit(embed=start_emb)
              return
            else:
              start_emb = discord.Embed(title='Call accepted', description=f'{channel.name} accepted the call.',color=0x288B22)
              await call_msg1.edit(embed=start_emb)
              await call_msg2.edit(embed=start_emb)
              call = True
              start=datetime.datetime.now()
            while call:
              try:
                def accept_check(m):
                  return((m.channel == channel or m.channel == ctx.channel) and not m.author.bot)
                message= await self.bot.wait_for("message",check=accept_check,timeout=600)
                if message.content == "b?end" and (message.channel == ctx.channel or message.channel == channel):
                  show_duration = True
                  break
                elif message.channel == channel:
                  await ctx.send(f"**{message.author.display_name}#{message.author.discriminator} :**\n{message.content}")
                  counter = counter + 1
                elif message.channel == ctx.channel:
                  await channel.send(f"**{message.author.display_name}#{message.author.discriminator} :**\n{message.content}")
                  counter = counter + 1
              except asyncio.TimeoutError:
                start_emb = discord.Embed(title='Waiting too long', description='No message was sent for more then 10 minutes.',color=0x00FFFF)
                await ctx.send(embed=start_emb)
                await channel.send(embed=start_emb)
                show_duration = True
                break
            if show_duration == True:
              end_emb = discord.Embed(title='Call ended', description=f'{message.author.mention} ended the call..',color=0x00FFFF)
              end_emb.add_field(name = 'Duration', value = f'Duaration: {str((datetime.datetime.now()-start).total_seconds())[:-3]}s')
              end_emb.add_field(name = 'Messages', value = f'Messages: {counter} messages')
              await ctx.send(embed=end_emb)
              await channel.send(embed=end_emb)
          else:
            index = 0
            embed = discord.Embed(
              title = 'Select Server',
              description = 'Please select the server you want to call. You can do so by reacting with the corresponding emote.'
            )
            embed.add_field(
              name = f'{index + 1}: {servers[index].name}',
              value = f'ID: {servers[index].id}',
              inline = False
            )
            try:
              await message.clear_reactions()
              await message.edit (embed = embed)
            except:
              await message.delete()
              message = await ctx.send(embed = embed)
            break

  @commands.command(aliases = ['settings'])
  async def end(self, ctx):
    pass

def setup(bot):
  bot.add_cog(Call(bot))