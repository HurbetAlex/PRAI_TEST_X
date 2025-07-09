import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Twitter credentials
    TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
    TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
    PROXY_URL = os.getenv("PROXY_URL")
    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    LOCALE = os.getenv("LOCALE", "en-US")
    TIMEZONE = os.getenv("TIMEZONE", "America/New_York")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CHAT_MODELS = ["gpt-4", "gpt-3.5-turbo"]
    COMPLETION_MODEL = "text-davinci-003"
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 2))

    # Database
    SQLITE_PATH = os.getenv("SQLITE_PATH", "twitterbot.sqlite3")

    # Playwright
    SLOW_MO = int(os.getenv("SLOW_MO", 80))
    TIMEOUT_SHORT = int(os.getenv("TIMEOUT_SHORT", 5000))  # ms
    TIMEOUT_LONG = int(os.getenv("TIMEOUT_LONG", 30000))  # ms