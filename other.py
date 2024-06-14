import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import BadRequest, Unauthorized
import asyncio
import platform
if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from telethon import TelegramClient

# Replace 'YOUR_API_ID' and 'YOUR_API_HASH' with your actual API ID and API hash
api_id = '20767409'
api_hash = 'ad4828ff66389557cca18d4db6c40642'

# Create the client and connect
client = TelegramClient('mysession', api_id, api_hash)

async def get_user_id(username):
    # Get the user entity
    await client.start()
    user = await client.get_entity(username)
    await client.disconnect()
    return user.id

from dotenv import load_dotenv

import telebot

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_IDS = ['-1002186586227']

removed_users = {channel_id: [] for channel_id in CHANNEL_IDS}


async def kick(update, context):
    # Get the username of the user to be removed
    username_to_remove = context.args[0]
    userid_to_remove = await get_user_id(username_to_remove)

    for channel_id in CHANNEL_IDS:
        try:
            context.bot.kick_chat_member(channel_id, userid_to_remove)

            removed_users[channel_id].append(userid_to_remove)

            context.bot.send_message(
                chat_id=channel_id, text=f"{userid_to_remove} has been removed from the channel and added to the removed users list.")
        except BadRequest as e:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"Error removing user from a channel: {e}")
        except Unauthorized:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"I don't have permission to remove users from a channel.")
        except Exception as e:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"An error occurred while removing the user: {e}")


def check_subscription(update, context):
    user = update.message.chat.username

    for channel_id in CHANNEL_IDS:
        if user in removed_users[channel_id]:
            try:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="You have been removed from this channel and can't subscribe again.")
            except BadRequest as e:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=f"Error sending message: {e}")
            except Unauthorized:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="I don't have permission to send messages in this chat.")
            except Exception as e:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=f"An error occurred: {e}")
            return

        try:
            context.bot.send_message(
                chat_id=channel_id, text=f"{user} has subscribed to the channel.")
        except BadRequest as e:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"Error sending message: {e}")
        except Unauthorized:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"I don't have permission to send messages in a channel.")
        except Exception as e:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"An error occurred while sending the message: {e}")


async def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("kick", kick))

    dispatcher.add_handler(MessageHandler(
        Filters.chat_type.channel & Filters.status_update.new_chat_members, check_subscription))

    updater.start_polling()
    updater.idle()
    print("bot is started")


asyncio.run(main())