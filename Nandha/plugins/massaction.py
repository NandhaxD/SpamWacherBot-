import config

from pyrogram import filters
from pyrogram import enums
from pyrogram.types import *
from Nandha.help.admin import *
from Nandha import Nandha



@Nandha.on_message(filters.command(["unbanall","massunban"],config.CMDS))
async def unbanall(_, message):
     user_id = message.from_user.id
     chat_id = message.chat.id
     if not user_id in config.DEVS and (await is_owner(chat_id,user_id)) == False:
           return await message.reply("`You Can't Access This!`")
     elif message.chat.type == enums.ChatType.PRIVATE:
          return await message.reply("`This Command Only work in Groups!`")
     else:
       try:
          BANNED = []
          unban = 0
          async for m in Nandha.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
                 BANNED.append(m.user.id)
                 await Nandha.unban_chat_member(chat_id,m.user.id)
                 unban +=1
          await message.reply("**Found Banned Members**: `{}`\n**Unbanned Successfully**: `{}`".format(len(BANNED), unban))
       except Exception as e:
           print(e)

@Nandha.on_message(filters.command(["sbanall","banall","massban"],config.CMDS))
async def banall(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not user_id in config.DEVS and (await is_owner(chat_id,user_id)) == False:
           return await message.reply("`You Can't Access This!`")
    elif message.chat.type == enums.ChatType.PRIVATE:
          return await message.reply("`This Command Only work in Groups!`")
    else:  
       try: 
          Members = []
          Admins = []
          async for x in Nandha.get_chat_members(chat_id):
              if not x.privileges:
                    Members.append(x.user.id)
              else:
                    Admins.append(x.user.id)
          for user_id in Members:
               if message.text.split()[0].lower().startswith("s"):
                        m = await Nandha.ban_chat_member(chat_id, user_id)
                        await m.delete()
               else:
                   await Nandha.ban_chat_member(chat_id, user_id)
          await message.reply_text("**Successfully Banned**: `{}`\n**Remaining Admins**: `{}`".format(len(Members),len(Admins),))
       except Exception as e:
        print(e)

@Nandha.on_message(filters.command(["skickall","kickall","masskick"],config.CMDS))
async def kickall(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not user_id in config.DEVS and (await is_owner(chat_id,user_id)) == False:
           return await message.reply("`You Can't Access This!`")
    elif message.chat.type == enums.ChatType.PRIVATE:
          return await message.reply("`This Command Only work in Groups!`")
    else:  
       try: 
          Members = []
          Admins = []
          async for x in Nandha.get_chat_members(chat_id):
              if not x.privileges:
                    Members.append(x.user.id)
              else:
                    Admins.append(x.user.id)
          for user_id in Members:
               if message.text.split()[0].lower().startswith("s"):
                        m = await Nandha.ban_chat_member(chat_id, user_id)
                        await Nandha.unban_chat_member(chat_id, user_id)
                        await m.delete()
               else:
                   await Nandha.ban_chat_member(chat_id, user_id)
                   await Nandha.unban_chat_member(chat_id, user_id)
          await message.reply_text("**Successfully Kicked**: `{}`\n**Remaining Admins**: `{}`".format(len(Members),len(Admins),))
       except Exception as e:
        print(e)

__MODULE__ = "Mass-A"

__HELP__ = """
**Mass Action**:

Only work for group owners!

- `/banall`: ban all members from group.
- `/kickall`: kick all members from group.
- `/unbanall`: unban all members from group.

to avoid service messages use instead "s"
for example: /skickall /sbanall.
"""
