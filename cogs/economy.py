import discord
import json
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import errors
import datetime
import custom
import random

class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, ctx):
    if ctx.author.bot == False:
      with open('json/member.json') as f:
        account = json.load(f)
      if str(ctx.author.id) not in account:
        account[str(ctx.author.id)] = {}
        account[str(ctx.author.id)]["points"] = 0
      account[str(ctx.author.id)]["points"] += random.randint(0, 3)
      with open('json/member.json', 'w') as f:
        json.dump(account, f)
  
  @commands.command()
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def balance(self, ctx):
    with open('json/member.json') as f:
      points = json.load(f)
    embed = discord.Embed(
      description = f'You have {points[str(ctx.author.id)]["points"]} points!',
      color = 0xffcd75)
    embed.set_author(name = ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.message.delete()
    await ctx.send(embed = embed, delete_after=25.0)
  
  @balance.error
  async def balance_error(self, ctx, error):
    if isinstance(error, errors.CommandOnCooldown):
      embed = discord.Embed(
        description = f'Hey! To avoid spam, we added a cooldown for this command. Please wait for {int(error.retry_after)} seconds to use this command again.',
        color = 0xffcd75)
      embed.set_author(name = ctx.author.name, icon_url=ctx.author.avatar_url)
      await ctx.message.delete()
      await ctx.send(embed = embed, delete_after=3.0)

  @commands.command(aliases = ['mines'])
  async def mine(self, ctx):
    await ctx.message.delete()
    count = 0
    mine=custom.files.json_load("./json/mine.json")
    x, y = 10, 10
    if str(ctx.author.id) not in mine:
      mine[str(ctx.author.id)] = {}
    if "mine" not in mine[str(ctx.author.id)]:
      mine[str(ctx.author.id)]["mine"] = ''
      maze = []
      for line in range(y):
        maze_line = []
        for _ in range(x):
          maze_line.append(random.choices(['🟩','🟫','🟨'], [4, 2, 1])[0])
        maze.append(maze_line)
      spawn_x, spawn_y = random.randint(0,x-1), random.randint(0,y-1)
      mine[str(ctx.author.id)]["position"] = {}
      mine[str(ctx.author.id)]["position"]["x"] = spawn_x
      mine[str(ctx.author.id)]["position"]["y"] = spawn_y
      mine[str(ctx.author.id)]["position"]["moves"] = 0
      mine[str(ctx.author.id)]["time"] = str(datetime.datetime.now())
      maze[spawn_y][spawn_x] = '🧍'
      mine[str(ctx.author.id)]["mine"] = maze
    await custom.files.json_save("./json/mine.json",mine)
    while True:
      text = ''
      for _ in mine[str(ctx.author.id)]["mine"]:
        text += (''.join(_)) + '\n'
      embed = discord.Embed(
        title = 'The Mines',
        description = text
      )
      embed.set_author(
        name = f'Moves = {mine[str(ctx.author.id)]["position"]["moves"]}',
        icon_url = ctx.author.avatar_url)
      try:
        await message.edit(embed = embed)
      except:
        message = await ctx.send (embed = embed)
      if count + 1 == x * y:
        duration = (datetime.datetime.now() - datetime.datetime.strptime(mine[str(ctx.author.id)]["time"], '%Y-%m-%d %H:%M:%S.%f'))
        embed = discord.Embed(
          title = 'You Win!',
          description = f'**Duration** : {str(duration)[5:-4]} seconds\n'\
          f'**Moves** : {mine[str(ctx.author.id)]["position"]["moves"]}',
          inline = False)
        await message.delete(delay = 60.0)
        await ctx.send(embed = embed, delete_after = 60.0)
        await message.clear_reactions()
        del mine[str(ctx.author.id)]
        await custom.files.json_save("./json/mine.json",mine)
        break
      pos_x = mine[str(ctx.author.id)]["position"]["x"]
      pos_y = mine[str(ctx.author.id)]["position"]["y"]
      position = f'({mine[str(ctx.author.id)]["position"]["x"]},{mine[str(ctx.author.id)]["position"]["y"]})'
      possible = {
        f"(0,{pos_y})": ['🟥','▶️','🔼','🔽'],
        f"({x-1},{pos_y})": ['◀️','🟨','🔼','🔽'],
        f"({pos_x},0)": ['◀️','▶️','🟩','🔽'],
        f"({pos_x},{y-1})": ['◀️','▶️','🔼','🟦']
      }
      reactions = possible.get(position, ['◀️','▶️','🔼','🔽'])
      possible = {
        f"(0,0)": ['🟥','▶️','🟩','🔽'],
        f"(0,{y-1})": ['🟥','▶️','🔼','🟦'],
        f"({x-1},0)": ['◀️','🟨','🟩','🔽'],
        f"({x-1},{y-1})": ['◀️','🟨','🔼','🟦'],
      }
      reactions = possible.get(position, reactions)
      for reaction in reactions:
        try:
          await message.add_reaction(reaction)
        except:
          pass
      def move (reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) in reactions and user == ctx.author
      try:
        reaction = await self.bot.wait_for('reaction_add', check=move, timeout = 20)
        pos_x = mine[str(ctx.author.id)]["position"]["x"]
        pos_y = mine[str(ctx.author.id)]["position"]["y"]
        mine[str(ctx.author.id)]["mine"][pos_y][pos_x] = '⬛'
        if str(reaction[0]) == '◀️':
          mine[str(ctx.author.id)]["position"]["x"] -= 1
        elif str(reaction[0]) == '▶️':
          mine[str(ctx.author.id)]["position"]["x"] += 1
        elif str(reaction[0]) == '🔽':
          mine[str(ctx.author.id)]["position"]["y"] += 1
        elif str(reaction[0]) == '🔼':
          mine[str(ctx.author.id)]["position"]["y"] -= 1
        await message.clear_reactions()
        await custom.files.json_save("./json/mine.json",mine)
        pos_x = mine[str(ctx.author.id)]["position"]["x"]
        pos_y = mine[str(ctx.author.id)]["position"]["y"]
        mine[str(ctx.author.id)]["mine"][pos_y][pos_x] = '🧍'
        mine[str(ctx.author.id)]["position"]["moves"] += 1
        count = 0
        for lines in mine[str(ctx.author.id)]["mine"]:
          count += lines.count('⬛') 
        await custom.files.json_save("./json/mine.json",mine)
      except asyncio.TimeoutError:
        embed.add_field(name = 'Timeout', value = 'Connection Lost', inline = False)
        await message.edit(embed = embed, delete_after = 5.0)
        await message.clear_reactions()
        break

def setup(bot):
  bot.add_cog(Economy(bot))
  print ('Loaded Economy Cog Successfully!')