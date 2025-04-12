import subprocess
import os
import openai  
from telegram import Bot
import asyncio

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)

async def main():
    await bot.send_message(chat_id=CHAT_ID, text="ГОЛ!")
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Git Status Output:")
        print(result.stdout)  
    else:
        print("Ошибка при выполнении git status:")
        print(result.stderr) 
    print("✅ Отправлено в Telegram.")


if __name__ == "__main__":
    asyncio.run(main())
