import subprocess
import os
from openai import OpenAI
from telegram import Bot

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)

def get_git_diff():
    result = subprocess.run(["git", "diff", "HEAD~1", "HEAD", "--unified=5"], capture_output=True, text=True)
    return result.stdout

def filter_relevant_chunks(diff_text):
    chunks = diff_text.split("diff --git ")
    return ["diff --git " + c for c in chunks if c.strip() and (".py" in c or ".ipynb" in c)]

def summarize_chunk(chunk):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ты анализируешь изменения в коде и кратко формулируешь, что было сделано."},
            {"role": "user", "content": f"Вот изменения в коде:\n\n{chunk}\n\nСформулируй кратко, что изменилось."}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    diff_text = get_git_diff()
    chunks = filter_relevant_chunks(diff_text)
    
    if not chunks:
        print("Нет релевантных изменений.")
        return
    
    summaries = []
    for i, chunk in enumerate(chunks, 1):
        try:
            print(f"🧠 Анализируем файл {i}/{len(chunks)}...")
            summary = summarize_chunk(chunk)
            summaries.append(f"🔸 {summary}")
        except Exception as e:
            summaries.append(f"⚠️ Ошибка при анализе: {e}")

    final_message = "📦 Изменения в последнем коммите:\n\n" + "\n\n".join(summaries)
    bot.send_message(chat_id=CHAT_ID, text=final_message)
    print("✅ Отправлено в Telegram.")

if __name__ == "__main__":
    main()
