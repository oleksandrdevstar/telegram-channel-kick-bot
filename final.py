from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv
from telethon import TelegramClient
from telegram.error import BadRequest
import platform, asyncio, os, ast

if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_IDS = os.getenv('CHANNEL_IDS')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

client = TelegramClient('mysession', api_id, api_hash)

CHANNEL_IDS = ast.literal_eval(CHANNEL_IDS)

async def get_user_id(username):
    await client.start()
    user = await client.get_entity(username)
    user_id = user.id
    await client.disconnect()
    return user_id

async def get_channel_title(channel_id):
    print(channel_id)
    await client.start()
    channel = await client.get_entity(channel_id)
    channel_title = channel.title
    await client.disconnect()
    return channel_title

async def kick(update: Update, context: CallbackContext) -> None:
    user_name = context.args[0]
    user_id = await get_user_id(username=user_name)
    
    for CHANNEL_ID in CHANNEL_IDS:
        channel_title = await get_channel_title(channel_id=CHANNEL_ID)
        try:
            await context.bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
            await update.message.reply_text(f"User @{user_name} has been kicked from @{channel_title} channel successfully.")
        except BadRequest:
            await update.message.reply_text(f"An error occurred while kicking the @{user_name} from @{channel_title}. Please check the user is either an admin or member of your channel.")
        except (IndexError, ValueError):
            await update.message.reply_text("Please provide a valid user name.")
        except Exception as e:
            await update.message.reply_text("An error occurred. Please try again.")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("kick", kick))
    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
