from telethon import TelegramClient

# Replace 'YOUR_API_ID' and 'YOUR_API_HASH' with your actual API ID and API hash
api_id = '20767409'
api_hash = 'ad4828ff66389557cca18d4db6c40642'

# Create the client and connect
client = TelegramClient('mysession', api_id, api_hash)

async def get_user_id(username):
    # Get the user entity
    user = await client.get_entity(username)
    print(user)

    # Print user ID
    print(f"User ID of {username} is {user.id}")

async def main():
    await client.start()  # No need to pass phone number here
    await get_user_id('louieworld')
    await client.disconnect()

# Example usage
import asyncio
import platform
if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
