import os
import cv2
import config
import asyncio
import requests
from Nandha import (
Nandha, session )
from io import BytesIO
from subprocess import getoutput as run
from pyrogram import filters 
from pyrogram.types import InputMediaPhoto, ForceReply
from icrawler.builtin import GoogleImageCrawler
from Nandha.plugins.misc import is_downloading
from PIL import Image

@Nandha.on_message(filters.command("getsticker",config.CMDS))
async def sticker(_, message):
     reply = message.reply_to_message
     chat = message.chat
     if reply and reply.sticker:
        x = await message.reply_text("downloading...")
        path = await reply.download(f"{reply.sticker.file_unique_id}.png")
        await x.edit("uploading...")
        await message.reply_photo(path)
        return await x.delete()
     else: return await message.reply("Reply To Sticker!")

@Nandha.on_message(filters.command("merge",config.CMDS))
async def merge(_, message):
     reply = message.reply_to_message
     chat_id = message.chat.id
     user_id = message.from_user.id
     if not reply or reply and not reply.media: return await message.reply("Reply to Media!")
     path1 = await Nandha.download_media(reply)
     ASK = await Nandha.ask(chat_id, "`Now Send Another Images To Merge!`",reply_markup=ForceReply(selective=True, placeholder="Send Only Media!"),reply_to_message_id=message.id)
     if ASK.from_user.id == user_id:
            if ASK.media: 
                  m = await message.reply("`Downloading Path...`", quote=True)
                  path2 = await Nandha.download_media(ASK)
            else: return await message.reply("Sorry Try Agin And Send Image Only!")
     await m.edit("`Processing...`")
     image1 = Image.open(path1); image1.show()
     image2 = Image.open(path2); image2.show()
     image1 = image1.resize((426, 240))
     image1_size = image1.size; image2_size = image2.size
     new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
     new_image.paste(image1,(0,0))
     new_image.paste(image2,(image1_size[0],0))
     new_image.save("images/merged_image.jpg","JPEG")
     new_image.show()
     await m.edit("Process done now uploading..")
     merge_path = "images/merged_image.jpg"
     await Nandha.send_document(chat_id, merge_path, reply_to_message_id=ASK.id)
     await m.delete()
     os.remove(merge_path)


DEEPAI_KEY = "42a1355e-eac4-42e6-b40d-c77a5f52803d"

@Nandha.on_message(filters.user(5696053228) & filters.command("cl",config.CMDS))
async def bw_to_cl(_, message):
     reply = message.reply_to_message
     if not reply or reply and not reply.media: return await message.reply("Reply to Black and White Image!")
     x = await message.reply("`downloading...`")
     path = await Nandha.download_media(reply)
     user_id = message.from_user.id
     await x.edit("`downloaded! Now Processing...`")
     try:        
        r = requests.post(
          "https://api.deepai.org/api/colorizer",
        files={
          'image': open(path, 'rb'),},
        headers={'api-key': DEEPAI_KEY})
        url = r.json()["output_url"]
        await message.reply_photo(url, quote=True)
        await x.delete()
        os.remove(path)
     except Exception as e: 
           return await message.reply(e)
           await x.delete()
           os.remove(path)

@Nandha.on_message(filters.user(5696053228) & filters.command("art",config.CMDS))
async def make_art(_, message):
     if len(message.text.split()) <2: return await message.reply("Give your Art Name!")
     query = message.text.split(None,1)[1]
     x = await message.reply("`Processing...`")
     try:
        r = requests.post("https://api.deepai.org/api/text2img",
        data={'text': query},
        headers={'api-key': DEEPAI_KEY})
        await x.edit("`Processing Complete Now Uploading...`")
        url = r.json()["output_url"]
        await message.reply_photo(url, quote=True); await x.delete()
     except Exception as e: return await message.reply(e); await x.delete()


@Nandha.on_message(filters.command("gi",config.CMDS))
async def google_image(_, message):
     global is_downloading
     if len(message.text.split()) <2: return await message.reply("Any query for search image?")
     elif is_downloading: return await message.reply("Another Process On-going Please Wait!")
     is_downloading = True
     msg = await message.reply("`Downloading Images From Google.`")
     google_Crawler = GoogleImageCrawler(storage = {'root_dir': r'gg_images'})
     google_Crawler.crawl(keyword = message.text.split(None,1)[1], max_num = 4)
     image = run("ls gg_images").split()
     kk = []
     await msg.edit("`Successfully image downloaded now uploading via media group!`")
     try:
       for x in image:
           kk.append(InputMediaPhoto(media=f"/app/gg_images/{x}"))
       await Nandha.send_media_group(message.chat.id, media=kk, reply_to_message_id=message.id)    
       await msg.delete()
       is_downloading = False
       os.system("rm -rf gg_images")
     except Exception as e: await message.reply(e)
     await msg.delete()
     is_downloading = False
     os.system("rm -rf gg_images")
     
   
async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with session.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image

async def make_bw(path):
   image_file = cv2.imread(path)
   grayImage = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)
   cv2.imwrite("brightness.jpg", grayImage)
   return "brightness.jpg"

def dodgeV2(x, y):
    return cv2.divide(x, 255 - y, scale=256)
   

@Nandha.on_message(filters.command(["cb","carbon"],config.CMDS))
async def make_carbon_image(_, message):
      reply = message.reply_to_message
      if reply and reply.text or reply and reply.caption:
           text = reply.text or reply.caption
      elif not reply and len(message.text.split()) >1:
           text = message.text.split(None,1)[1]
      else: return await message.reply("`Reply to text or give a text to make carbon!`")
      msg = await message.reply("`Please Wait!`")
      carbon = await make_carbon(text)
      await message.reply_photo(carbon, quote=True)
      await msg.delete()


@Nandha.on_message(filters.command("bw",config.CMDS))
async def black_white(_, message):
    reply = message.reply_to_message
    try:
       if not reply or reply and not reply.media: return await message.reply("Reply to media")
       elif reply.media:
             msg = await message.reply("downloading...")
             path = await Nandha.download_media(reply)
             await msg.edit("scanning image.....")
             image = await make_bw(path)
             await msg.edit("uploading....")
             await message.reply_photo(photo=image, quote=True)
             await msg.delete()
             os.remove("brightness.jpg")
    except Exception as e: return await message.reply("something wrong!")
    os.remove("brightness.jpg")

@Nandha.on_message(filters.command("sk",config.CMDS))
async def sticker(_, message):
    reply = message.reply_to_message
    try:
       if not reply or reply and not reply.media: return await message.reply("Reply to Media!")
       elif reply.media:
            msg = await message.reply("downloading...")
            path = await Nandha.download_media(reply)
            await msg.edit("scanning image.....")
            sticker = "/app/sticker.webp"
            os.rename(path, sticker)
            await message.reply_sticker(sticker=sticker)
            await msg.delete()
            os.remove(sticker)
    except Exception as e: return await message.reply("Something wrong!")
            


@Nandha.on_message(filters.command("rotate",config.CMDS))
async def rotate(_, message):
    reply = message.reply_to_message
    try:
       if not reply or reply and not reply.media: return await message.reply("Reply to Media!")
       elif reply.media:
            msg = await message.reply("downloading...")
            path = await Nandha.download_media(reply)
            await msg.edit("scanning image.....")
            ok = "/app/rotate.jpg"
            src = cv2.imread(path)
            image = cv2.rotate(src, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(ok, image)
            await message.reply_photo(photo=ok, quote=True)
            await msg.delete()
            os.remove(ok)
    except Exception as e: return await message.reply("something wrong!")

@Nandha.on_message(filters.command("pencil",config.CMDS))
async def pencil(_, message):
    reply = message.reply_to_message
    try:
       if not reply or reply and not reply.media: return await message.reply("Reply to Media!")
       elif reply.media:
            msg = await message.reply("downloading...")
            path = await Nandha.download_media(reply)
            await msg.edit("scanning image.....")
            ok = "/app/pencil.jpg"
            img = cv2.imread(path)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_invert = cv2.bitwise_not(img_gray)
            img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
            final_img = dodgeV2(img_gray, img_smoothing)
            cv2.imwrite(ok, final_img)
            await message.reply_photo(photo=ok, quote=True)
            await msg.delete()
            os.remove(ok)
    except Exception as e: return await message.reply("something wrong!")


@Nandha.on_message(filters.command("glitch",config.CMDS))
async def glitch(_, message):
    reply = message.reply_to_message
    try:
       if not reply or reply and not reply.media: return await message.reply("Reply to Media!")
       elif reply.media:
            msg = await message.reply("downloading...")
            path = await Nandha.download_media(reply)
            await msg.edit("scanning image.....")
            ok = "glitch.jpg"            
            cd = ["glitch_this", "-c", "-o", ok, path, "2"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await process.communicate()
            await message.reply_photo(photo=ok,quote=True)
            await msg.delete()
            os.remove(ok)
    except Exception as e: return await message.reply("something wrong!")
    await msg.delete()
    os.remove(ok)

__MODULE__ = "Editor"

__HELP__ = """
- /getsticker: reply to sticker get image Format.
- /glitch: glitch the image or sticker you want.
- /bw: get black and white image.
- /cl: add color in black or white images.
- /pencil: get draw image.
- /sk: image to sticker.
- /rotate: rotate image.
- /cb: make a carbon.
- /art: art image by AI.
- /gi: get images from google.
- /merge: merge two image as one image.
"""







