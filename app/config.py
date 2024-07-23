import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # path
    ROOT_PATH = Path(__file__).parent.parent
    STATIC_PATH = ROOT_PATH / "static"

    # llm
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    GROQ_API_BASE = os.environ.get("GROQ_API_BASE", "")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

    # api key
    API_KEYS = [key.strip() for key in os.environ.get("API_KEYS", "").split(",")]

    # memos
    MEMOS_API_BASE = os.environ.get("MEMOS_API_BASE", "")
    MEMOS_API_KEY = os.environ.get("MEMOS_API_KEY", "")

    # test
    TEST_BASE_URL = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:8000")


settings = Settings()
