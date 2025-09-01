import os
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

# Загружаем переменные окружения
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def test_proxy():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Привет! Проверка связи через ProxyAPI. Ответь одним словом."}]
        )
        print("✅ Ответ от модели:", response.choices[0].message.content)
    except Exception as e:
        print("❌ Ошибка:", e)
        raise

if __name__ == "__main__":
    test_proxy()

