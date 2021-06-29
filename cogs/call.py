import discord
import discord_components as dc
from discord_components import DiscordComponents, InteractionType
import json
import asyncio
import uuid
from discord.ext import commands
import datetime

class Call(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.ddb = DiscordComponents(self.bot)

  @commands.command()
  async def call(self, ctx, member:discord.User):
    cid = uuid.uuid4()
    embed = discord.Embed(
      title = f'Calling {member}',
      description = f'```Call Id: {cid}\n'\
                    f'Caller: {ctx.author}\n'\
                    f'Calling: {member}```'
    )
    chnlmsg = await ctx.send(
      embed = embed,
      components = [
        dc.Button(
          style = dc.ButtonStyle.red,
          label = "Cancel",
          emoji = "✖️",
          id = "cancel"
    )])

    try:
      dm = await member.create_dm()
    except:
      embed.title = f"Failed to call {member.name}#{member.discriminator}"
      await chnlmsg.edit(embed = embed,
        components = [
          dc.Button(
            style = dc.ButtonStyle.red,
            label = "Cancel",
            emoji = "✖️",
            id = "cancel",
            disabled = True
      )])
      return
    dmembed = discord.Embed(
      title = f"{ctx.author} is calling...",
      description = f'```Call Id: {cid}\n'\
                    f'Caller: {ctx.author.name}#{ctx.author.discriminator}\n'\
                    f'Calling: {member.name}#{member.discriminator}```'
    )
    await dm.send(
      embed = dmembed,
      components = [
        [
          dc.Button(
            style = dc.ButtonStyle.green,
            label = "Accept",
            emoji = "📞",
            id = "accept"
          ),
          dc.Button(
            style = dc.ButtonStyle.red,
            label = "Decline",
            emoji = "✖️",
            id = "decline",
          )
        ]
      ]
    )
    def check(res):
     return (res.user.id == ctx.author.id and res.channel.id == ctx.channel.id) or (res.user == member)
    try:
      res = await self.bot.wait_for("button_click", check = check, timeout=10)
      if res.component.id == "cancel":
        embed.title = "Cancelled Current Call"
        await chnlmsg.edit(embed = embed,
          components = [
          dc.Button(style=dc.ButtonStyle.red, label="Cancelled", emoji="✖️", id="cancel", disabled=True)
        ])
        await res.respond(type=6)
    except asyncio.TimeoutError:
      await chnlmsg.edit(content = 'Failed to Call...', components = [])
      return
      
def setup(bot):
  bot.add_cog(Call(bot))
  print ('Loaded Call Cog Successfully!')