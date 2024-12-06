#(©)AnimeXyz

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import sys
import os
import git
from datetime import datetime
import pyrogram.utils
pyrogram.utils.MIN_CHANNEL_ID = -1002475424150

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT

name ="""
░█████╗░███╗░░██╗██╗███╗░░░███╗███████╗  ██╗░░██╗██╗░░░██╗███████╗
██╔══██╗████╗░██║██║████╗░████║██╔════╝  ╚██╗██╔╝╚██╗░██╔╝╚════██║
███████║██╔██╗██║██║██╔████╔██║█████╗░░  ░╚███╔╝░░╚████╔╝░░░███╔═╝
██╔══██║██║╚████║██║██║╚██╔╝██║██╔══╝░░  ░██╔██╗░░░╚██╔╝░░██╔══╝░░
██║░░██║██║░╚███║██║██║░╚═╝░██║███████╗  ██╔╝╚██╗░░░██║░░░███████╗
╚═╝░░╚═╝╚═╝░░╚══╝╚═╝╚═╝░░░░░╚═╝╚══════╝  ╚═╝░░╚═╝░░░╚═╝░░░╚══════╝
"""

AUTHORIZED_USERS = [7030439873, 987654321]  # Replace with actual user IDs

UPSTREAM_REPO_URL = "https://github.com/Itzmepapa123/faired.git"
UPSTREAM_BRANCH = "Updated"


# Function to initialize and update from upstream repository

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    try:
        if len(UPSTREAM_REPO) == 0:
           raise TypeError
    except:
        UPSTREAM_REPO = None

    try:
        if len(UPSTREAM_BRANCH) == 0:
           raise TypeError
    except:
        UPSTREAM_BRANCH = 'master'

    async def initialize_and_update_repo():
        if UPSTREAM_REPO is not None:
            if os.path.exists('.git'):
                subprocess.run(["rm", "-rf", ".git"])

            update = subprocess.run([f"git init -q \
                         && git config --global user.email yashoswal18@gmail.com \
                         && git config --global user.name mergebot \
                         && git add . \
                         && git commit -sm update -q \
                         && git remote add origin {UPSTREAM_REPO} \
                         && git fetch origin -q \
                         && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

        if update.returncode == 0:
            print("Repository initialized and updated successfully.")
        else:
            print("Failed to initialize or update repository.")
            
    

    async def send_started_message(self, user_id: int):
        try:
            await self.send_message(
                chat_id=user_id,
                text="Bot has started!"
            )
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {str(e)}")

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        user_id = 7024179022  # Replace with your desired user ID
        await self.send_started_message(user_id)

        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.create_chat_invite_link(chat_id=FORCE_SUB_CHANNEL2, creates_join_request=True)).invite_link 
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/Animetalks0 for support")
                sys.exit()
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL2}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/Animetalks0 for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/Animetalks0 for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/Animes_Xyz")
        self.LOGGER(__name__).info(f""" \n\n       
░█████╗░███╗░░██╗██╗███╗░░░███╗███████╗  ██╗░░██╗██╗░░░██╗███████╗
██╔══██╗████╗░██║██║████╗░████║██╔════╝  ╚██╗██╔╝╚██╗░██╔╝╚════██║
███████║██╔██╗██║██║██╔████╔██║█████╗░░  ░╚███╔╝░░╚████╔╝░░░███╔═╝
██╔══██║██║╚████║██║██║╚██╔╝██║██╔══╝░░  ░██╔██╗░░░╚██╔╝░░██╔══╝░░
██║░░██║██║░╚███║██║██║░╚═╝░██║███████╗  ██╔╝╚██╗░░░██║░░░███████╗
╚═╝░░╚═╝╚═╝░░╚══╝╚═╝╚═╝░░░░░╚═╝╚══════╝  ╚═╝░░╚═╝░░░╚═╝░░░╚══════╝
                                          """)
        self.username = usr_bot_me.username
        # Web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

# Add the restart command handler
@Bot.on_message(filters.command("restart") & filters.user(AUTHORIZED_USERS))
async def restart(client, message):
    await message.reply_text("Updating from the repository and restarting the bot...")
    update_from_upstream()
    restart_bot()


