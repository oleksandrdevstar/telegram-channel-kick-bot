from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os
import requests
from telethon import TelegramClient
from telegram.error import BadRequest
import platform, asyncio

if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

# Create the client and connect
client = TelegramClient('mysession', api_id, api_hash)

async def get_user_id(username):
    await client.start()  # No need to pass phone number here
    # Get the user entity
    user = await client.get_entity(username)
    return user.id

# Define the function to handle the /kick command
async def kick(update: Update, context: CallbackContext) -> None:
    try:
        # Extract the user ID from the command arguments
        user_name = context.args[0]
        user_id = await get_user_id(username=user_name)
        # Kick the user from the channel
        await context.bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

        # Send a message confirming that the user has been kicked
        await update.message.reply_text(f"User @{user_name} has been kicked from the channel successfully.")
    except (IndexError, ValueError):
        # If no user ID is provided or if the user ID is not a valid integer
        await update.message.reply_text("Please provide a valid user name.")
    except BadRequest:
        # If an error occurs during the kick operation
        await update.message.reply_text("An error occurred while kicking the user. Please check the user is neither an admin or a member of your channel.")

def main() -> None:
    # Create the Application and pass in the bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the /kick command handler
    application.add_handler(CommandHandler("kick", kick))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
