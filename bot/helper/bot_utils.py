from pyrogram.types import BotCommand

from bot import bot, LOGGER

async def set_commands(bot):
    user_commands = [
        BotCommand(BotCommands.StartCommand, "Start")
    ]
  
    name = (await bot.get_me()).username
    
    await bot.set_bot_commands(user_commands)
    LOGGER.info(f"User Commands Are Set successfully for @{name}")
