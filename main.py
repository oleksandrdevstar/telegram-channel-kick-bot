import requests

# Replace these variables with your bot token, channel ID, and user ID
BOT_TOKEN = '7460478547:AAHyTqIQnBbxqdHZzqA5mGlcjlg6tmdn8Qw'
CHANNEL_ID = '-1002161323205'  # e.g., -1001234567890
USER_ID = '5446693065'

url = f"https://api.telegram.org/bot{BOT_TOKEN}/kickChatMember"
params = {
    'chat_id': CHANNEL_ID,
    'user_id': USER_ID
}

response = requests.post(url, params=params)

if response.status_code == 200:
    print("User removed successfully.")
else:
    print("Failed to remove user:", response.json())
