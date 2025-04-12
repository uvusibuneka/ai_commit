import subprocess
import os
import openai  # исправляем импорт
from telegram import Bot
import asyncio

# Получаем ключи и ID из окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Устанавливаем ключ для OpenAI
openai.api_key = OPENAI_API_KEY

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)

# Основная асинхронная функция
async def main():
    await bot.send_message(chat_id=CHAT_ID, text="ГОЛ!")
    print("✅ Отправлено в Telegram.")

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
