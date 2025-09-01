import os
import re
import textwrap
import requests
from requests.utils import requote_uri
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI

# Загружаем переменные окружения из .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.proxyapi.ru/openai/v1")
MODEL = os.getenv("PAGE_SUMMARY_MODEL", "gpt-4-0613")  # проверенная модель на твоём ProxyAPI

# Клиент OpenAI/ProxyAPI
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def extract_text_from_url(url: str) -> str:
    """Скачивает HTML по URL и извлекает чистый текст (с поддержкой кириллицы в ссылке)."""
    safe_url = requote_uri(url)  # корректно процентизирует кириллицу/пробелы
    r = requests.get(safe_url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Удаляем скрипты/стили
    for t in soup(["script", "style", "noscript"]):
        t.decompose()

    text = " ".join(soup.get_text(" ").split())
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text

SYSTEM_PROMPT = (
    "Ты аналитик. Кратко перескажи суть текста страницы в 3–5 предложениях. "
    "Пиши простым языком, без воды и повторов. Не выдумывай фактов."
)

@retry(wait=wait_random_exponential(min=1, max=6), stop=stop_after_attempt(3))
def summarize(page_text: str) -> str:
    """Создаёт резюме текста через Responses API (совместимо с ProxyAPI)."""
    snippet = page_text[:8000]  # безопасная усечка
    user = textwrap.dedent(f"""
    Вот текст страницы. Сформулируй краткое резюме в 3–5 предложениях.

    ТЕКСТ:
    {snippet}
    """).strip()

    # Используем Responses API (на твоём прокси chat.completions не поддержан)
    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
        max_output_tokens=400,
    )
    out = resp.output_text.strip()

    # Оставим не больше 5 предложений
    sents = re.split(r"(?<=[.!?])\s+", out)
    return " ".join(sents[:5]).strip()

def run(url: str) -> str:
    text = extract_text_from_url(url)
    if not text:
        raise RuntimeError("Не удалось извлечь текст со страницы")
    return summarize(text)

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    else:
        # дефолт — русская Википедия (теперь кириллица обрабатывается корректно)
        url = "https://ru.wikipedia.org/wiki/Искусственный_интеллект"

    print("\n=== КРАТКОЕ РЕЗЮМЕ ===\n")
    print(run(url))
