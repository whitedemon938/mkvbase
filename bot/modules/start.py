from pyrogram import Client

async def start(client, message):
    text = "Hello testing"
    return await message.reply(text)
  
