import discord
import discord.ext
import random
import typing
from datetime import datetime
from PIL import ImageColor, Image
from discord.ext import commands

class Info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=["si"])
  async def serverinfo(self, ctx):

    statuses = [len(list(filter(lambda m: str(m.status) == "online" and not m.bot, ctx.guild.members))),
		len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
		len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
		len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
    info_emb=discord.Embed(
      title= 'Information',
      timestamp=datetime.utcnow(),
    )
    info_emb.set_thumbnail(url=ctx.guild.icon_url)
    info_emb.set_footer(text=f'Server Created At | {ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S")}', icon_url=ctx.guild.icon_url)
    fields=[
      ('__Server Information__',
      f'**Server Name** : {ctx.message.guild.name}\n'\
      f'**ID** : {ctx.guild.id}\n'\
      f'**Owner** : <@{ctx.guild.owner.id}>\n'\
      f'**Region** : {str(ctx.guild.region).capitalize()}\n'\
      f'**Created at** : {ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S")}',False),
      ('__Server Boosts__',
      f'**Server Boost Level** : {ctx.guild.premium_tier}\n'\
      f'**Server Boosts** : {ctx.guild.premium_subscription_count}', False),
      ('__Member Information__',
      f'**Members** : {len(ctx.guild.members)} = \n'\
      f' **- Users** : {len(list(filter(lambda m: not m.bot, ctx.guild.members)))}\n'\
      f' **- Bots** : {len(list(filter(lambda m: m.bot, ctx.guild.members)))}\n'\
      f'**Status** =\n'\
      f' **- :green_circle: Online : ** {statuses[0]}\n'\
      f' **- :crescent_moon: Idle : ** {statuses[1]}\n'\
      f' **- :o: Do Not Disturb : ** {statuses[2]}\n'\
      f' **- :radio_button: Offline : ** {statuses[3]}\n'\
      f'**Banned Members** : {len(await ctx.guild.bans())}', False),
      ('__Channel Information__',
      f'**Channel Categories** : {len(ctx.guild.categories)}\n'\
      f'**Channels** : {len(ctx.guild.channels)} =\n'\
      f' **- Text Channels** : {len(ctx.guild.text_channels)}\n **- Voice Channels** : {len(ctx.guild.voice_channels)}\n'\
      f'**Roles** : {len(ctx.guild.roles)}\n'\
      f'**Invites** : {len(await ctx.guild.invites())}', False),
      ('__Emoji Information__',
      f'**Emoji Limit** : {50 if ctx.guild.premium_tier == 0 else(100 if ctx.guild.premium_tier == 1 else(150 if ctx.guild.premium_tier == 2 else 250))}\n'\
      f'**Emojis** : {len(ctx.guild.emojis)} =\n'\
      f'**- Animated** : {len(list(filter(lambda e: e.animated,ctx.guild.emojis)))}\n'\
      f' **- Static** : {len(list(filter(lambda e: e.animated == False,ctx.guild.emojis)))}', False)
    ]
    for name, value, inline in fields:
      info_emb.add_field(
        name=name,
        value=value,
        inline=inline
      )
    await ctx.send(embed=info_emb)

  @commands.command(aliases=["memberinfo", "ui", "mi"])
  async def userinfo(self, ctx, target:discord.Member=None):
    target = target if target != None else ctx.author
    status = ':green_circle: Online' if str(target.status).title() == 'Online' else (':crescent_moon: Idle' if str(target.status).title() == 'Idle' else (':o: Do Not Disturb' if str(target.status).title() == 'Dnd' else ':radio_button: Offline'))
    activity = f"{str(target.activity.type).split('.')[-1].title() if target.activity else ''} {':' if target.activity != None else ''} {str(target.activity)}"
    info_emb=discord.Embed(
      title= 'User Information',
      timestamp=datetime.utcnow(),
      colour=target.colour
    )
    info_emb.set_thumbnail(url=target.avatar_url)
    info_emb.set_footer(text=f'Member Joined At | {target.joined_at.strftime("%d/%m/%Y %H:%M:%S")}', icon_url=ctx.guild.icon_url)
    roles_str=""
    for role in target.roles:
      roles_str+=f"{role.mention}\n"
    fields=[
      ('__General Information__',
      f'**Name** : {str(target)}\n'\
      f'**Display Name** : {target.display_name}\n'\
      f'**ID** : {target.id}\n'\
      f'**Created At** : {target.created_at.strftime("%d/%m/%Y %H:%M:%S")}\n'\
      f'**Bot?** {target.bot}', False),
      ('__Status and Activity__',
      f'**Status** : {status}\n'\
      f'**Activity** : {activity}', False),
      ('__Server Information__',
      f'**Top Role** : {target.top_role.mention}\n'\
      f'**Joined At** : {target.joined_at.strftime("%d/%m/%Y %H:%M:%S")}\n'\
      f'**Server Booster?** : {bool(target.premium_since)}\n', False),
      ('__Roles__', f'{roles_str}', False),
    ]
    for name, value, inline in fields:
      info_emb.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=info_emb)

def setup(bot):
    bot.add_cog(Info(bot))