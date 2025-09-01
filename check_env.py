import os
from dotenv import load_dotenv

load_dotenv()  # подгружаем .env

print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("OPENAI_BASE_URL:", os.getenv("OPENAI_BASE_URL"))
print("PAGE_SUMMARY_MODEL:", os.getenv("PAGE_SUMMARY_MODEL"))
