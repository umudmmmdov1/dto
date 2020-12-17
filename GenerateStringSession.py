from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("""Xaiş my.telegram.org adresine gedin
Telegram hesabınızı işlederek giriş edin
API Development Tools yerine girin
Lazimli melumatlari girerek yeni bir app yaradın""")
APP_ID = int(input("APP ID: "))
API_HASH = input("API HASH: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print(client.session.save())
