from telethon import TelegramClient, events

# Вставте ваші дані з сайту Telegram
api_id = 1234567 
api_hash = 'ваш_hash_тут'

# 'session_name' - це назва файлу, де збережеться ваш вхід
client = TelegramClient('session_name', api_id, api_hash)

# Налаштування: звідки читати і куди пересилати
SOURCE = 'username_чужого_каналу'
TARGET = 'username_вашого_каналу'

@client.on(events.NewMessage(chats=SOURCE))
async def handler(event):
    # Тут можна додати фільтр (наприклад, тільки повідомлення зі словом "знижка")
    if "знижка" in event.raw_text.lower():
        await client.send_message(TARGET, event.message)
        print("Повідомлення переслано!")

print("Бот запущений...")
client.start()
client.run_until_disconnected()