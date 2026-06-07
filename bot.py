import asyncio
from telethon import TelegramClient, events

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
            ("🔴" in text or "повітряна тривога" in text_lower or 
             "🟢" in text or "відбій" in text_lower))

@client.on(events.NewMessage(chats=[SOURCE_CHANNEL]))
async def handler(event):
    try:
        msg = event.message
        if msg and msg.text:
            text = msg.text.strip()
            print(f"📨 Отримано: {text[:120]}...")
            
            if is_alert_message(text):
                await client.send_message(TARGET_CHANNEL, text)
                print("✅ ОПУБЛІКОВАНО в @nebo_kr")
            else:
                print("⏭ Пропущено")
    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    await client.start()
    print("🚨 Бот запущений і готовий!")
    print("Слухаємо @NeboSportyvu → @nebo_kr")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
