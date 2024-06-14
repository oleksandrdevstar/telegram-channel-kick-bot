import requests
TOKEN = "7460478547:AAHyTqIQnBbxqdHZzqA5mGlcjlg6tmdn8Qw"
chat_id = "856247733"
message = "@louieworld"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json()) # this sends the message


