import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token here
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Function to kick a user
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = int(context.args[0])
        chat_id = update.effective_chat.id
        await context.bot.ban_chat_member(chat_id, user_id)
        await update.message.reply_text(f"The user with ID {user_id} is kicked successfully.")
    except IndexError:
        await update.message.reply_text("Please provide a user ID.")
    except ValueError:
        await update.message.reply_text("Invalid user ID provided.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("An error occurred. Please try again.")

# Main function to set up the bot
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handler for /kick
    application.add_handler(CommandHandler("kick", kick))

    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
