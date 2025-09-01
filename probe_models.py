import os, requests
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("OPENAI_API_KEY")
candidates = [
    "https://api.proxyapi.ru",
    "https://api.proxyapi.ru/v1",
    "https://proxyapi.ru",
    "https://proxyapi.ru/v1",
    "https://api.proxyapi.ru/openai/v1",
    "https://proxyapi.ru/openai/v1",
]
hdr = {"Authorization": f"Bearer {key}"}

for base in candidates:
    url = base.rstrip("/") + "/models"
    try:
        r = requests.get(url, headers=hdr, timeout=15)
        print(f"{url:45} -> {r.status_code} | {r.text[:120].replace(chr(10),' ')}")
    except Exception as e:
        print(f"{url:45} -> ERR  | {e}")
