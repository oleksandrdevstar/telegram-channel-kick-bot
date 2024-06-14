from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
from telethon import TelegramClient
from telegram.error import TelegramError, BadRequest
from telethon.errors.rpcerrorlist import *
import platform
import asyncio
import os
import re
import time

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

client = TelegramClient('mysession', API_ID, API_HASH)


async def get_user_id(username):
    await client.start()
    try:
        user = await client.get_entity(username)
        user_id = user.id
        await client.disconnect()
        return user_id
    except:
        return False


def remove_at_symbol(input_string):
    if input_string.startswith("@"):
        return input_string[1:].strip()
    return input_string.strip()


def read_channel_names_file(file_path):
    channel_ids = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            channel_username = remove_at_symbol(line)
            channel_ids.append(channel_username)

    return channel_ids


def prepend_negative_100_to_integer(number):
    number_str = str(number)

    if not number_str.startswith('-100'):
        result = int('-100' + number_str)
    else:
        result = int(number_str)

    return result


async def get_channel_title(channel_id):
    await client.start()
    channel = await client.get_entity(channel_id)
    channel_title = channel.title
    await client.disconnect()
    return channel_title


def is_valid_telegram_username(username):
    # Define the regex pattern for a valid Telegram username
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]{4,31}$'

    # Use the fullmatch method to check if the entire username matches the pattern
    if re.fullmatch(pattern, username):
        return True
    else:
        return False


file_path = 'channels.txt'
channel_ids = read_channel_names_file(file_path)


async def kick(update: Update, context: CallbackContext) -> None:
    if not len(context.args) or not is_valid_telegram_username(remove_at_symbol(context.args[0])):
        await update.message.reply_text("Please provide a valid telegram user name.")
    else:
        user_name = remove_at_symbol(context.args[0])
        user_id = await get_user_id(user_name)

        if user_id:
            for channel_id in channel_ids:
                print(channel_id)
                channel_title = await get_channel_title(channel_id=int(channel_id))
                print(channel_title)

                try:
                    await context.bot.ban_chat_member(channel_id, user_id)
                    await update.message.reply_text(f"@{user_name} has been kicked from {channel_id} channel successfully.")
                    time.sleep(3)
                    continue
                except ChatNotModifiedError:
                    await update.message.reply_text(f"User @{user_name} is already banned from the {channel_id} channel.")
                except Exception as e:
                    await update.message.reply_text(f"User @{user_name} not exists in {channel_id} channel or etc.")

            return
        else:
            await update.message.reply_text(f"@{user_name} not exists in telegram.")


async def remove(update: Update, context: CallbackContext) -> None:
    if not len(context.args) or not is_valid_telegram_username(remove_at_symbol(context.args[0])):
        await update.message.reply_text("Please provide a valid telegram user name.")
    else:
        user_name = remove_at_symbol(context.args[0])
        user_id = await get_user_id(user_name)

        if user_id:
            for channel_id in channel_ids:
                try:
                    await context.bot.unban_chat_member(channel_id, user_id)
                    await update.message.reply_text(f"@{user_name} has been restored from {channel_id} channel successfully.")
                    continue
                except ChatNotModifiedError:
                    await update.message.reply_text(f"User @{user_name} is already restored from the {channel_id} channel.")
                except Exception as e:
                    await update.message.reply_text(f"User @{user_name} not exists in {channel_id} channel or etc.")

            return
        else:
            await update.message.reply_text(f"@{user_name} not exists in telegram.")


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CommandHandler("remove", remove))
    application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
