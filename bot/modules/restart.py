from asyncio import create_subprocess_exec
from os import path as ospath, execl
from sys import executable

from bot import bot, LOGGER

async def restart_command(client, message):
    restart_message = await message.reply(
      '<i>Restarting...</i>'
    )
    await (await create_subprocess_exec('python3', 'update.py')).wait()
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    execl(executable, executable, "-m", "bot")

async def restart():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await bot.edit_message_text(
              chat_id=chat_id,
              message_id=msg_id,
              text="<i>Restarted !</i>"
            )
        except Exception as e:
            LOGGER.error(e)
