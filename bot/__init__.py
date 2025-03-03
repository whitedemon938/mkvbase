import asyncio
from os import remove as osremove, path as ospath, environ, getcwd
from time import time
from dotenv import load_dotenv, dotenv_values
from pyrogram import Client as tgClient, enums
from pymongo import MongoClient
from logging import getLogger, ERROR,Formatter, FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info, warning as log_warning

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s",
            datefmt="%d-%b-%y %I:%M:%S %p",
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

getLogger("pyrogram").setLevel(ERROR)
LOGGER = getLogger(__name__)

load_dotenv('config.env', override=True)
BOT_START = time()

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)
            
bot_id = BOT_TOKEN.split(':', 1)[0]

DATABASE_URL = environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    DATABASE_URL = ''

if DATABASE_URL:
    conn = MongoClient(DATABASE_URL)
    db = conn.shortener
    current_config = dict(dotenv_values('config.env'))
    old_config = db.settings.deployConfig.find_one({'_id': bot_id})
    if old_config is None:
        db.settings.deployConfig.replace_one(
            {'_id': bot_id}, current_config, upsert=True)
    else:
        del old_config['_id']
    if old_config and old_config != current_config:
        db.settings.deployConfig.replace_one(
            {'_id': bot_id}, current_config, upsert=True)
    elif config_dict := db.settings.config.find_one({'_id': bot_id}):
        del config_dict['_id']
        for key, value in config_dict.items():
            environ[key] = str(value)
    conn.close()
    BOT_TOKEN = environ.get('BOT_TOKEN', '')
    bot_id = BOT_TOKEN.split(':', 1)[0]
    DATABASE_URL = environ.get('DATABASE_URL', '')
else:
    config_dict = {}

OWNER_ID = environ.get('OWNER_ID', '')
if len(OWNER_ID) == 0:
    log_error("OWNER_ID variable is missing! Exiting now")
    exit(1)
else:
    OWNER_ID = int(OWNER_ID)

CHANNEL_STORE_ID = environ.get('CHANNEL_STORE_ID', '')
if len(CHANNEL_STORE_ID) == 0:
    CHANNEL_STORE_ID = "" 

TELEGRAM_API = environ.get('TELEGRAM_API', '')
if len(TELEGRAM_API) == 0:
    log_error("TELEGRAM_API variable is missing! Exiting now")
    exit(1)
else:
    TELEGRAM_API = int(TELEGRAM_API)

TELEGRAM_HASH = environ.get('TELEGRAM_HASH', '')
if len(TELEGRAM_HASH) == 0:
    log_error("TELEGRAM_HASH variable is missing! Exiting now")
    exit(1)
            
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH','')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = ""

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = ""

config_dict = {'BOT_TOKEN': BOT_TOKEN,
               'CHANNEL_STORE_ID': CHANNEL_STORE_ID,
               'DATABASE_URL': DATABASE_URL,
               'OWNER_ID': OWNER_ID,
               'TELEGRAM_HASH': TELEGRAM_HASH,
               'TELEGRAM_API': TELEGRAM_API,
               'UPSTREAM_BRANCH': UPSTREAM_BRANCH,
               'UPSTREAM_REPO': UPSTREAM_REPO}

log_info("Creating client from BOT_TOKEN")
bot = tgClient('bot', TELEGRAM_API, TELEGRAM_HASH, bot_token=BOT_TOKEN,in_memory=True, workers=1000).start()
bot_loop = bot.loop
bot_name = bot.me.username
