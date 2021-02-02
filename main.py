import discord
import os
import sys
import letitlive
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or('b?', 'B?'),intents=discord.Intents.all(),owners=[737422322431950962,557599092931559447])
bot.remove_command('help')

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 737422322431950962
    return commands.check(predicate)

@bot.event
async def on_ready():
  print("Ready!")

fail_emb = discord.Embed(title = 'Error: Missing extension', color = 0xFFFFFF)

@bot.command(aliases = ['l'])
@is_owner()
async def load(ctx, extension = None):
  if extension == None:
    await ctx.send(embed=fail_emb, delete_after=10.0)
    return 0
  bot.load_extension(f'cogs.{extension}')
  embed=discord.Embed(title = f'Loading: cogs.{extension}', color = 0x228B22)
  await ctx.send(embed=embed, delete_after=10.0)

@bot.command(aliases = ['u'])
@is_owner()
async def unload(ctx, extension):
  if extension == None:
    await ctx.send(embed=fail_emb, delete_after=10.0)
    return 0
  bot.unload_extension(f'cogs.{extension}')
  embed=discord.Embed(title = f'Unloading: cogs.{extension}', color = 0x800000)
  await ctx.send(embed = embed, delete_after=10.0)

@bot.command(aliases = ['r'])
@is_owner()
async def reload(ctx, extension):
  if extension == None:
    await ctx.send(embed=fail_emb, delete_after=10.0)
    return 0
  if extension == 'all':
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        try:
          bot.unload_extension(f'cogs.{filename[:-3]}')
        finally:
          bot.load_extension(f'cogs.{filename[:-3]}')
          embed=discord.Embed(title = f'Reloading: cogs.{filename}', color = 0x241571)
          await ctx.send(embed=embed, delete_after=10.0)
    return 0
  try:
    bot.unload_extension(f'cogs.{extension}')
  except:
    pass
  finally:
    bot.load_extension(f'cogs.{extension}')
    embed=discord.Embed(title = f'Reloading: cogs.{extension}', color = 0x241571)
    await ctx.send(embed=embed, delete_after=10.0)

@bot.command()
@is_owner()
async def list(ctx):
  loaded = []
  emb_desc = []
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      try:
        bot.load_extension(f'cogs.{filename[:-3]}')
        bot.unload_extension(f'cogs.{filename[:-3]}')
      except discord.ext.commands.ExtensionAlreadyLoaded:
        loaded.append(filename[:-3])
  for cog in loaded:
    emb_desc.append(f'- {cog}')
  load_emb = discord.Embed(title = 'Loaded Cogs', description = ('\n'.join(emb_desc)), color = 0xFFA500)
  await ctx.send(embed=load_emb, delete_after=10.0)

@bot.command()
@is_owner()
async def restart(ctx):
  restart_emb = discord.Embed(title = 'Restarting...', color = 0xFFA500)
  await ctx.send(embed=restart_emb, delete_after=10.0)
  os.execl(sys.executable, sys.executable, *sys.argv)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

letitlive.keep_alive()
bot.run(os.environ.get("TOKEN"))

