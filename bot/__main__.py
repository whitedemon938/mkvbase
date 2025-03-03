from asyncio import gather

from pyrogram.filters import command, private
from pyrogram.handlers import MessageHandler , CallbackQueryHandler

from bot import bot, bot_name, LOGGER
from bot.helper.bot_utils import set_commands
from bot.helper.bot_commands import BotCommands
from bot.helper.filters import CustomFilters
from bot.modules import *

async def main_handler():
    bot.add_handler(MessageHandler(restart_command,filters=command(BotCommands.RestartCommand) & private & CustomFilters.owner))
    bot.add_handler(MessageHandler(start, filters=command(BotCommands.StartCommand) & private & CustomFilters.owner))
    
async def bot_main():
    await gather(*[restart(),main_handler(),set_commands(bot)])
    LOGGER.info(f"MkvToolNix Bot - [@{bot_name}] Started!")

bot.loop.run_until_complete(bot_main())
bot.loop.run_forever()
