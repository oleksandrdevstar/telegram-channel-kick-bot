import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest
from dotenv import load_dotenv

load_dotenv()

# Load your bot token and channel ID from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Define the async function to handle the /kick command
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Extract the user ID from the command arguments
        user_id = int(context.args[0])

        # Kick the user from the channel
        await context.bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

        # Send a message confirming that the user has been kicked
        await update.message.reply_text(f"User {user_id} has been kicked from the channel successfully.")
    except (IndexError, ValueError):
        # If no user ID is provided or if the user ID is not a valid integer
        await update.message.reply_text("Please provide a valid user ID.")
    except BadRequest:
        # If an error occurs during the kick operation
        await update.message.reply_text("An error occurred while kicking the user. Please try again later.")

def main() -> None:
    # Create the Application and pass in the bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the /kick command handler
    application.add_handler(CommandHandler("kick", kick))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
