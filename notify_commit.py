import subprocess
import os
import openai  # исправляем импорт
from telegram import Bot

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_TOKEN)

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="ГОЛ!")
    print("✅ Отправлено в Telegram.")

if __name__ == "__main__":
    main()
