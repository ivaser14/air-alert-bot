import asyncio
from telethon import TelegramClient, events
import os

# ================== НАЛАШТУВАННЯ ==================
API_ID = 30622563
API_HASH = '1298b1587c44279db1b299d6c59887b4'

SESSION_NAME = 'nebo_kr_bot'

SOURCE_CHANNEL = '@NeboSportyvu'
TARGET_CHANNEL = '@nebo_kr'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def is_alert_message(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower().strip()
    
    # М'яка перевірка
    has_red = "🔴" in text or "повітряна тривога" in text_lower
    has_green = "🟢" in text or "відбій" in text_lower
    has_kr = "криворізький район" in text_lower
    has_follow = "слідкуйте за подальшими повідомленнями" in text_lower
    
    return (has_red or has_green) and has_kr and has_follow


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
            print(f"✅ ОПУБЛІКОВАНО: {msg.text[:100]}...")
        else:
            # Для дебагу — показуємо, що бот бачить
            if "криворізький" in (msg.text or "").lower():
                print(f"📌 Побачив повідомлення з Криворізьким, але не підходить під фільтр: {msg.text[:80]}...")
    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    await client.start()
    print("🚨 Бот запущений! Чекаємо повідомлень з @NeboSportyvu")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
