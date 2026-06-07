import asyncio
from telethon import TelegramClient, events
import os

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

print("DEBUG: API_ID =", API_ID)
print("DEBUG: API_HASH =", "заповнено" if API_HASH else "ПУСТО!")

if not API_ID or not API_HASH:
    print("❌ API_ID або API_HASH не знайдено!")
    exit(1)

SESSION_NAME = 'nebo_kr_bot'

SOURCE_CHANNEL = '@NeboSportyvu'
TARGET_CHANNEL = '@nebo_kr'

ALERT_TEXT = "🔴  Повітряна тривога в Криворізький район"
CANCEL_TEXT = "🟢  Відбій тривоги в Криворізький район"

client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)

def is_alert_message(text: str) -> bool:
    if not text:
        return False
    text = text.strip()
    return (text.startswith(ALERT_TEXT) or text.startswith(CANCEL_TEXT)) and "Слідкуйте за подальшими повідомленнями" in text

@client.on(events.NewMessage(chats=[SOURCE_CHANNEL]))
async def handler(event):
    try:
        msg = event.message
        if msg and msg.text and is_alert_message(msg.text):
            await client.send_message(
                TARGET_CHANNEL,
                msg.text,
                file=msg.media if msg.media else None,
                formatting_entities=msg.entities
            )
            print(f"✅ Опубліковано: {msg.text[:80]}...")
    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    await client.start()
    print("🚨 Бот успішно запущений!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
