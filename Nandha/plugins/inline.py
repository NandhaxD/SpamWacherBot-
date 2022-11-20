from pyrogram import filters
from pyrogram.types import *
from Nandha import Nandha


@Nandha.on_inline_query(filters.regex("^pfp"))
async def inline(_, query):
     user_id = query.from_user.id
     answers = []
     async for photo in Nandha.get_chat_photos(user_id):
        answers.append(
            InlineQueryResultCachedPhoto(
                caption="Made by @NandhaBots",
                photo_file_id=photo.file_id
            )
           )

     await query.answer(answers, cache_time=30)
     
