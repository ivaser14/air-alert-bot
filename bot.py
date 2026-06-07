import asyncio
import logging
import os
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import time

# ================== НАЛАШТУВАННЯ ==================
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

SOURCE_CHANNEL = '@NeboSportyvu'
TARGET_CHANNEL = '@nebo_kr'
# =================================================

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

client = TelegramClient('nebo_kr_session', API_ID, API_HASH)

def is_alert_message(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return ("криворізький район" in t and 
            "слідкуйте за подальшими повідомленнями" in t and
            any(word in t for word in ["тривога", "відбій", "🔴", "🟢"]))

@client.on(events.NewMessage(chats=[SOURCE_CHANNEL]))
async def handler(event):
    try:
        if not event.message or not event.message.text:
            return
            
        text = event.message.text.strip()
        
        logging.info(f"📨 Отримано: {text[:120]}...")
        
        if is_alert_message(text):
            await client.send_message(TARGET_CHANNEL, text)
            logging.info("✅ УСПІШНО ОПУБЛІКОВАНО в @nebo_kr")
        else:
            logging.info("⏭ Пропущено (не підходить під фільтр)")
            
    except FloodWaitError as e:
        logging.warning(f"❌ Flood wait: {e.seconds} секунд")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logging.error(f"❌ Помилка: {e}")

async def main():
    await client.start()
    logging.info("🚀 Бот успішно запущений і слухає @NeboSportyvu")
    logging.info("Очікуємо повідомлень про тривогу...")

    # Keep-alive
    while True:
        await asyncio.sleep(60)
        logging.info(f"[{time.strftime('%H:%M:%S')}] Бот живий...")

if __name__ == '__main__':
    asyncio.run(main())
