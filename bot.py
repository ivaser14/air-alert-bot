import asyncio
from telethon import TelegramClient, events
import time

API_ID = 30622563
API_HASH = '1298b1587c44279db1b299d6c59887b4'

SESSION_NAME = 'nebo_kr_bot'

SOURCE_CHANNEL = '@NeboSportyvu'
TARGET_CHANNEL = '@nebo_kr'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def is_alert_message(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    return ("криворізький район" in text_lower and 
            "слідкуйте за подальшими повідомленнями" in text_lower and
            ("🔴" in text or "🟢" in text or "тривога" in text_lower or "відбій" in text_lower))

@client.on(events.NewMessage(chats=[SOURCE_CHANNEL]))
async def handler(event):
    try:
        if event.message and event.message.text:
            text = event.message.text.strip()
            print(f"📨 Отримано: {text[:150]}...")
            
            if is_alert_message(text):
                await client.send_message(TARGET_CHANNEL, text)
                print("✅ УСПІШНО ОПУБЛІКОВАНО!")
            else:
                print("⏭ Пропущено")
    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    await client.start()
    print("🚨 Бот запущений (polling mode)")
    print("Слухаємо @NeboSportyvu...")
    
    # Keep-alive
    while True:
        await asyncio.sleep(30)
        print(f"[{time.strftime('%H:%M:%S')}] Бот живий...")

if __name__ == '__main__':
    asyncio.run(main())
