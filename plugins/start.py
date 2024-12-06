import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant

from bot import Bot, restart_bot
from users import handle_senduser_command
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed1, subscribed2, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

# In-memory dictionary to keep track of ongoing /start commands
processing_users = {}



async def delete_after_delay(message: Message, delay):
    await asyncio.sleep(delay)
    await message.delete()

@Bot.on_message(filters.command('start') & filters.private & subscribed1 & subscribed2)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id in processing_users and processing_users[user_id]:
        await message.reply_text("Please wait, your previous request is still being processed.")
        return

    processing_users[user_id] = True

    try:
        if not await present_user(user_id):
            try:
                await add_user(user_id)
            except:
                pass

        text = message.text
        if len(text) > 7:
            try:
                base64_string = text.split(" ", 1)[1]
            except:
                processing_users[user_id] = False
                return

            string = await decode(base64_string)
            argument = string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    processing_users[user_id] = False
                    return
                if start <= end:
                    ids = range(start, end + 1)
                else:
                    ids = []
                    i = start
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < end:
                            break
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    processing_users[user_id] = False
                    return

            temp_msg = await message.reply("Please wait...")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("Something went wrong..!")
                processing_users[user_id] = False
                return

            await temp_msg.delete()

            for msg in messages:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None

                try:
                    if msg and (msg.text or msg.photo or msg.document or msg.video or msg.audio or msg.sticker or msg.voice or msg.animation or msg.video_note or msg.contact or msg.location or msg.venue or msg.poll):
                        k = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        await asyncio.sleep(0.5)
                        if k is not None:
                            asyncio.create_task(delete_after_delay(k, 1800))
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    k=await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    if k is not None:
                        asyncio.create_task(delete_after_delay(k, 1800))
                except:
                    pass

            

                await message.reply_text(
                    "<b><i>» Save These Files In Your Saved Messages. They Will Be Deleted In 30 Minutes.</i>\n"
                    "<blockquote>» Must Join\n~ @hindi_crunchyroll\n~ @anime_in_hind\n~ @Crypto_Airdrop_Live</blockquote></b>",
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("😊 About Me", callback_data="about")],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")]
                ]
            )
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
    finally:
        processing_users[user_id] = False


#=====================================================================================##

WAIT_MSG = """"<b>Processing ....</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

#=====================================================================================##

is_restarting = False
@Bot.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_bot(b, m):
    global is_restarting
    if not is_restarting:
        is_restarting = True
        await m.reply_text("**Restarting.....**")

        # Gracefully stop the bot's event loop
        b.stop()
        time.sleep(2)  # Adjust the delay duration based on your bot's shutdown time

        # Restart the bot process
        os.execl(sys.executable, sys.executable, *sys.argv)

is_restarting = False  
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink),
            InlineKeyboardButton(text="Join Channel", url=client.invitelink2),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcast ho rha till then FUCK OFF </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

@Bot.on_message(filters.command("senduser"))
async def on_senduser_command(client, message):
    await handle_senduser_command(client, message)


