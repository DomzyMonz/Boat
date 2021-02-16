import json
import re
from replit import db
import aiohttp
import io
from discord import Webhook, AsyncWebhookAdapter,TextChannel

class files:
  async def json_save(path,data):
    match = re.search(r"(?:\.\/json\/)(.+)(?=\.json)",path)
    name = match.group(1)
    print(name)
    with open (path,"w") as f:
      json.dump(data,f)
    f.close()
    db[name] = data

  def json_load_backup(name):
    data = db[name]
    with open (f"./json/{name}.json","w") as f:
      json.dump(data,f)
    f.close()
    print(f"Loaded db {name} successfully.")

  def json_load(path):
    with open (path,"r") as f:
      data = json.load(f)
    f.close()
    return data

class webhook:
  async def send(channel:TextChannel,name:str,file:str,message:str):
    with open(file, 'rb') as img:	
      webhook_session = await message.channel.create_webhook(name = name, avatar = img.read())
    async with aiohttp.ClientSession() as session:
      webhook = Webhook.from_url(webhook_session.url, adapter=AsyncWebhookAdapter(session))
      await webhook.send(message, username=name)
      await webhook.delete()

  async def send_from_url(channel:TextChannel,name:str,img_url:str,message:str):
    async with aiohttp.ClientSession() as session:
      async with session.get(img_url) as emoji_img:
        img = io.BytesIO(await emoji_img.read())
      webhook_session = await channel.create_webhook(name = name, avatar = img.read())
    async with aiohttp.ClientSession() as session:
      webhook = Webhook.from_url(webhook_session.url, adapter=AsyncWebhookAdapter(session))
      await webhook.send(message, username=name)
      await webhook.delete()

class reaction_menu:
  ...

class AsyncIter:    
    def __init__(self, items):    
        self.items = items    

    async def __aiter__(self):    
        for item in self.items:    
            yield item  

def to_word(_object):
  return str(_object).replace("True","Yes").replace("False","No").replace("None","N/A")