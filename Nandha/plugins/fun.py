import config
import asyncio
import re
import random
import requests
from Nandha import Nandha
from pyrogram import filters          

@Nandha.on_message(filters.command(["cat","kitty"],config.CMDS))
async def cate(_, message):
      api = requests.get("https://api.thecatapi.com/v1/images/search").json()
      url = api[0]["url"]
      if url.endswith(".gif"): await message.reply_animation(url)
      else: await message.reply_photo(url)

@Nandha.on_message(filters.regex("baka"))
async def baka(_, message):
       reply = message.reply_to_message
       api = requests.get("https://nekos.best/api/v2/baka").json()
       url = api["results"][0]['url']
       anime = api["results"][0]["anime_name"]     
       if reply:
            name = reply.from_user.first_name
            await reply.reply_animation(url,caption="**• {}**\n**Baka! {}**".format(anime, name))
       else:
           name = message.from_user.first_name
           await message.reply_animation(url,caption="**• {}**\n**Baka! {}**".format(anime, name))

@Nandha.on_message(filters.regex("hug"))
async def hug(_, message):
       reply = message.reply_to_message
       api = requests.get("https://nekos.best/api/v2/hug").json()
       url = api["results"][0]['url']
       anime = api["results"][0]["anime_name"]     
       if reply:
            name = reply.from_user.first_name
            await reply.reply_animation(url,caption="**• {}**\n**Hugs! {}**".format(anime, name))
       else:
           name = message.from_user.first_name
           await message.reply_animation(url,caption="**• {}**\n**Hugs! {}**".format(anime, name))

@Nandha.on_message(filters.command("insult",config.CMDS))
async def insult(_, message):
      reply = message.reply_to_message
      try:
          insult = requests.get("https://insult.mattbas.org/api/insult").text
          if reply:
               string = insult.replace("You are",reply.from_user.first_name)
               await message.reply(string)
          else:
              string = insult.replace("You are",message.from_user.first_name)
              await message.reply(string)
      except Exception as e:
          await message.reply(e)

@Nandha.on_message(filters.command("riddle",config.CMDS))
async def riddle(_, message):
     riddle = requests.get("https://riddles-api.vercel.app/random").json()
     question = riddle["riddle"]
     answer = riddle["answer"]
     msg = await message.reply(f"**• Riddle**:\n[ `{question}` ]\n\n[ `The Answer will show automaticly 20seconds after tell me your guess's!` ]")
     await asyncio.sleep(20)
     await msg.edit(f"**• Riddle**:\n[ `{question}` ]\n\n• **Answer**: [ `{answer}` ]")
     

@Nandha.on_message(filters.command("quote",config.CMDS))
async def quote(_, m):
    api = random.choice(requests.get("https://type.fit/api/quotes").json())
    string = api["text"]
    author = api["author"]
    await m.reply(
        f"**Quotes**:\n`{string}`\n\n"
        f"   ~ **{author}**")
        

__MODULE__ = "Fun"

__HELP__ = """
- `/quote`: get random quotes.
- `/riddle`: get random riddle question.
- `/insult`: reply to user or self for insult.
- `/cat`: cute cat random images 
- `/dog`: dog random funny video and images .

**Regex**:
baka - hug
reply to or it slef.
"""
