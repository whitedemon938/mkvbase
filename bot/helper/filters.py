from pyrogram.filters import create

from bot import OWNER_ID

class CustomFilters:
    async def owner_filter(self , _, message):
        user = message.from_user or message.sender_chat
        uid = user.id
        return uid == OWNER_ID

    owner = create(owner_filter)
