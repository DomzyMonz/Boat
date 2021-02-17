import discord
import json
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import errors
import datetime
import custom
import random

class Games(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def ttt(self, ctx, player:discord.Member):
    if player == ctx.author:
      await ctx.send('Bruv, no play with self.')
      return
    if player.bot == True:
      await ctx.send('You play with bot? No')
      return
    player1 = ctx.message.author
    player2 = player
    c_player = random.choice([player1, player2])
    move1 = []
    move2 = []
    game_move = []
    win = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6]
    ]
    reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
    checks = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
    f=lambda a: (abs(a)+a)/2
    while True:
      if c_player == player1:
        c_player = player2
      else:
        c_player = player1
      gameboard = [['🔳','🔳','🔳'], ['🔳','🔳','🔳'],['🔳','🔳','🔳']]
      for _ in move1:
        _ -= 1
        gameboard[int(_/3)][int(f((_%3)))] = '❌'
      for _ in move2:
        _ -= 1
        gameboard[int(_/3)][int(f((_%3)))] = '⭕'
      message = ''
      for line in gameboard:
        for _ in line:
          message += _
        message += '\n'
      embed = discord.Embed(
        title = 'Tic-Tac-Toe',
        description = message
      )
      embed.set_author(name=c_player)
      try:
        await msg.edit(embed = embed)
      except:
        msg = await ctx.send(embed = embed)
      for _ in win:
        if _[0] in move1 and _[1] in move1 and _[2] in move1:
          await msg.clear_reactions()
          embed = discord.Embed()
          embed.set_author(name =f'{player1} has won the match!')
          await msg.edit(embed = embed)
          break
        elif _[0] in move2 and _[1] in move2 and _[2] in move2:
          await msg.clear_reactions()
          embed = discord.Embed()
          embed.set_author(name =f'{player2} has won the match!')
          await msg.edit(embed = embed)
          break
      if len(game_move) == 9:
        embed = discord.Embed()
        await msg.clear_reactions()
        embed.set_author(name ='Draw!')
        await msg.edit(embed = embed)
      for _ in reactions:
        await msg.add_reaction(_)
      reactions = []
      def choose(reaction, user):
        return reaction.message.id == msg.id and user == c_player and reaction.emoji in checks
      try:
        reaction = await self.bot.wait_for('reaction_add', check=choose, timeout = 20)
        pr = {
          '1️⃣':1,
          '2️⃣':2,
          '3️⃣':3,
          '4️⃣':4,
          '5️⃣':5,
          '6️⃣':6,
          '7️⃣':7,
          '8️⃣':8,
          '9️⃣':9
        }
        add = pr.get(str(reaction[0]))
        checks[add-1] = ''
        if c_player == player1:
          move1.append(add)
        else:
          move2.append(add)
        await msg.clear_reaction(str(reaction[0]))
      except asyncio.TimeoutError:
        await msg.delete()
        break

def setup(bot):
  bot.add_cog(Games(bot))
  print ('Loaded Games Cog Successfully!')