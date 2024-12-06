#(©)CodeXBotz

import os
from os import environ
import logging
from logging.handlers import RotatingFileHandler

import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7615868642:AAHH9uYWlRI_PJRsNTsmrTGYDTTE2FbrMMU")  

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "19863702"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "6d48cb362a97a43cfc944fd5c0f917f9")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001956516069"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "7705025239"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://zeno:zeno@zeno.5uft1.mongodb.net/?retryWrites=true&w=majority&appName=Zeno")
JOIN_REQS_DB = environ.get("JOIN_REQS_DB", DB_URI)
DB_NAME = os.environ.get("DATABASE_NAME", "Zeno")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1001983923805"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1001704801800"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello {first}\n\nI am a file store bot Powered by @Hindi_Crunchyroll ⚡</b>.")

try:
    ADMINS=[6204872199]
    for x in (os.environ.get("ADMINS", "7024179022 6204872199 6449631273 6039119180").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>Sorry Dude You Need To Join These Channels</b>\n\n<b>So Please Click Blow To Join Channel ⚡</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "🚫 Please Avoid Direct Messages. I'm Here merely for file sharing!"

ADMINS.append(OWNER_ID)


LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
