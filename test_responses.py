import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),   # у тебя: https://api.proxyapi.ru/openai/v1
)

try:
    r = client.responses.create(
        model=os.getenv("PAGE_SUMMARY_MODEL", "gpt-4-0613"),
        input=[{"role": "user", "content": "Скажи 'тест ок'"}],
        max_output_tokens=50,
        temperature=0
    )
    print("✅ Ответ от модели:", r.output_text)
except Exception as e:
    print("❌ Ошибка:", repr(e))
