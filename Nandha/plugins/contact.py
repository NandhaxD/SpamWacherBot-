import config

from Nandha import Nandha
from pyrogram import filters
from pyrogram.types import *
from pyrogram import enums

@Nandha.on_message(filters.command("contact",config.CMDS))
async def contact(_, message):
     user = message.from_user
     if message.chat.type == enums.ChatType.PRIVATE:
          return await message.reply("Are You Sure? this command for contact to my creator if you sure please press confirm!",
           reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Confirm", callback_data="contact"),
            InlineKeyboardButton("❌ Delete", callback_data="delete:{user.id}")]]))
     else: return await message.reply("hello Mr fucker this command only work in my dm 🤖!")

@Nandha.on_callback_query(filters.regex("contact"))
async def contact(_, query):
    chat = query.message.chat
    await query.message.delete()
    x = "Ok Send Me What Else You Want To Say to My Owner!")
    format = "Send Media Text ect !"
    ASK = await Nandha.ask(chat.id, text=x, reply_markup=ForceReply(selective=True, placeholder=format))
    if ASK.text[1:7] == "cancel":
          return await message.reply("Ok cancelled Process 🤖!")
    else: await Nandha.forward_messages(config.OWNER_ID, chat.id, ask.id)
    await ASK.edit("Your Message Successfully Send into my Owner 🤖!")
