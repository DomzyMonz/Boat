import discord
from discord.ext import commands
import os
import letitlive

bot = commands.Bot(command_prefix=['b?', 'B?'],intents=discord.Intents.all())
#bot.remove_command('help')

@bot.event
async def on_ready():
  print("Ready!")

fail_emb = discord.Embed(title = 'Error: Missing extension', color = 0xFFFFFF)

#@bot.event
#async def on_message(message):
#  print(message)
#  await message.channel.send(content=message.content)

@bot.command(aliases = ['l'])
async def load(ctx, extension = None):
  if extension == None:
    await ctx.send(embed=fail_emb)
    return 0
  bot.load_extension(f'cogs.{extension}')
  embed=discord.Embed(title = f'Loading: cogs.{extension}', color = 0x228B22)
  await ctx.send(embed=embed)

@bot.command(aliases = ['u'])
async def unload(ctx, extension):
  if extension == None:
    await ctx.send(embed=fail_emb)
    return 0
  bot.unload_extension(f'cogs.{extension}')
  embed=discord.Embed(title = f'Unloading: cogs.{extension}', color = 0x800000)
  await ctx.send(embed = embed)

@bot.command(aliases = ['r'])
async def reload(ctx, extension):
  if extension == None:
    await ctx.send(embed=fail_emb)
    return 0
  bot.unload_extension(f'cogs.{extension}')
  bot.load_extension(f'cogs.{extension}')
  embed=discord.Embed(title = f'Reloading: cogs.{extension}', color = 0x241571)
  await ctx.send(embed=embed)

@bot.command()
async def list(ctx):
  loaded = []
  emb_desc = []
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      try:
        bot.load_extension(f'cogs.{filename[:-3]}')
      except discord.ext.commands.ExtensionAlreadyLoaded:
        loaded.append(filename[:-3])
  for cog in loaded:
    emb_desc.append(f'- {cog}')
  load_emb = discord.Embed(title = 'Loaded Cogs', description = ('\n'.join(emb_desc)), color = 0xFFA500)
  await ctx.send(embed=load_emb)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

letitlive.keep_alive()
bot.run(os.environ.get("TOKEN"))#use this its better imo