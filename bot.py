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
    text_lower = text.lower()
    
    has_krivorizky = "криворізький район" in text_lower
    has_sleduyte = "слідкуйте за подальшими повідомленнями" in text_lower
    
    has_trivoga = ("🔴" in text or "повітряна тривога" in text_lower)
    has_vidbiy = ("🟢" in text or "відбій" in text_lower)
    
    return (has_krivorizky and has_sleduyte) and (has_trivoga or has_vidbiy)


@client.on(events.NewMessage(chats=[SOURCE_CHANNEL]))
async def handler(event):
    try:
        msg = event.message
        if not msg or not msg.text:
            return
            
        text = msg.text.strip()
        
        print(f"📨 Отримано з @NeboSportyvu:")
        print(f"   {text[:180]}..." if len(text) > 180 else f"   {text}")
        
        if is_alert_message(text):
            await client.send_message(
                TARGET_CHANNEL,
                text,
                file=msg.media if msg.media else None,
                formatting_entities=msg.entities
            )
            print(f"✅ УСПІШНО ОПУБЛІКОВАНО в @nebo_kr!")
        else:
            print(f"⏭ Пропущено (не підходить під фільтр)")
            
    except Exception as e:
        print(f"Помилка: {e}")


async def main():
    await client.start()
    print("🚨 Бот запущений!")
    print("Слухаємо @NeboSportyvu → публікуємо в @nebo_kr")
    print("Очікуємо повідомлень про тривогу...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
