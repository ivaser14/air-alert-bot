import asyncio
from telethon import TelegramClient, events
import os

# ================== НАЛАШТУВАННЯ ==================
# Заміни ці два значення на свої!
API_ID = 30622563                    # ← Твій API ID (тільки цифри)
API_HASH = '1298b1587c44279db1b299d6c59887b4'  # ← Твій API Hash

SESSION_NAME = 'nebo_kr_bot'

SOURCE_CHANNEL = '@NeboSportyvu'
TARGET_CHANNEL = '@nebo_kr'

ALERT_TEXT = "🔴  Повітряна тривога в Криворізький район"
CANCEL_TEXT = "🟢  Відбій тривоги в Криворізький район"
# =================================================

print("=== DEBUG INFO ===")
print("API_ID =", API_ID)
print("API_HASH = ✅ Заповнено")
print("==================")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

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
            print(f"✅ Опубліковано в @nebo_kr: {msg.text[:80]}...")
    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    print("🚨 Бот запускається...")
    await client.start()
    print("🚨 Бот успішно запущений і працює!")
    print(f"Слухаємо {SOURCE_CHANNEL} → публікуємо в {TARGET_CHANNEL}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
