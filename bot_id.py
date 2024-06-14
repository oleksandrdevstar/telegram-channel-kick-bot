from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
from telethon import TelegramClient
from telegram.error import TelegramError, BadRequest
from telethon.errors.rpcerrorlist import UsernameNotOccupiedError
import platform, asyncio, os, re
if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

client = TelegramClient('mysession', API_ID, API_HASH)

async def get_user_id(username):
    await client.start()
    user = await client.get_entity(username)         
    user_id = user.id
    await client.disconnect()
    return user_id

async def get_channel_id(channel_username):
    await client.start()
    channel = await client.get_entity(channel_username)
    channel_id = channel.id
    await client.disconnect()
    return channel_id

def remove_at_symbol(input_string):
    if input_string.startswith("@"):
        return input_string[1:].strip()
    return input_string.strip()

def read_channel_names_file(file_path):
    channel_usernames = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            channel_username = remove_at_symbol(line)
            channel_usernames.append(channel_username)

    return channel_usernames

def prepend_negative_100_to_integer(number):
    number_str = str(number)
    
    if not number_str.startswith('-100'):
        result = int('-100' + number_str)
    else:
        result = int(number_str)
    
    return result

def is_valid_telegram_username(username):
    # Define the regex pattern for a valid Telegram username
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]{4,31}$'
    
    # Use the fullmatch method to check if the entire username matches the pattern
    if re.fullmatch(pattern, username):
        return True
    else:
        return False

file_path = 'channels.txt'
channel_usernames = read_channel_names_file(file_path)

async def kick(update: Update, context: CallbackContext) -> None:
    if not len(context.args) or not is_valid_telegram_username(remove_at_symbol(context.args[0])):
        await update.message.reply_text("Please provide a valid user name.")
    else:
        user_id = 0
        try:
            user_name = remove_at_symbol(context.args[0])
            user_id = await get_user_id(username=user_name)
        except:
            await update.message.reply_text(f"{user_name} is not in use by anyone else yet.")
        if user_id:        
            for channel_username in channel_usernames:
                try:
                    channel_id = await get_channel_id(channel_username=channel_username)
                    channel_id = prepend_negative_100_to_integer(channel_id)
                except:
                    await update.message.reply_text(f"@{channel_username} is not valid.")
                    continue
                try:
                    await context.bot.ban_chat_member(chat_id=channel_id, user_id=user_id)
                    await update.message.reply_text(f"User @{user_name} has been kicked from @{channel_username} channel successfully.")
                except BadRequest as e:
                    await update.message.reply_text(f"Bad request: {e}")
                except Exception as e:
                    await update.message.reply_text(f"An unexpected error occurred: {e}")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("kick", kick))
    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
