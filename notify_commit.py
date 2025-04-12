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

def get_commit_info():
    result = subprocess.run(["git", "log", "-1", "--pretty=format:%h - %an, %ar : %s"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        print("Ошибка при получении информации о последнем коммите")
        return None

def get_git_diff():
    result = subprocess.run(["git", "diff", "HEAD~1", "HEAD"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        print("Ошибка при выполнении git diff")
        return None

def truncate_diff(diff_text, max_length=1000):
    if len(diff_text) > max_length:
        return diff_text[:max_length] + "\n... (truncated)"
    return diff_text

def analyze_changes(diff_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": "Ты анализируешь изменения в коде и кратко поясняешь, что было сделано."},
                {"role": "user", "content": f"Вот изменения в коде:\n\n{diff_text}"}
            ],
            max_tokens=500  
        )
        return response.choices[0].message['content'].strip()  
    except Exception as e:
        return f"Ошибка при анализе: {str(e)}"

async def main():
    commit_info = get_commit_info()
    if commit_info:
        print(f"Последний коммит: {commit_info}")
    
    diff_text = get_git_diff()
    if diff_text:
        print(f"Изменения в коде:\n{diff_text}")

        truncated_diff = truncate_diff(diff_text)
        
        analysis = analyze_changes(truncated_diff)
        
        message = f"📦 Последний коммит: {commit_info}\n\n🔹 Изменения:\n{analysis}"

        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("✅ Отправлено в Telegram.")
    else:
        print("Нет изменений для анализа.")

if __name__ == "__main__":
    asyncio.run(main())
