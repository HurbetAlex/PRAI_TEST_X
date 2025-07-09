import time
import openai
from openai.error import RateLimitError, OpenAIError, NotFoundError
from config import Config

openai.api_key = Config.OPENAI_API_KEY


def generate_reply(tweet_text: str) -> str:
    """
    Generate a human-like reply by trying chat models first, then a completion model.
    """
    system_prompt = "You are a friendly Twitter user. Reply concisely and naturally."
    user_prompt = f"Reply to this tweet as a real human:\n\n{tweet_text}"

    # Chat models
    for model in Config.CHAT_MODELS:
        for attempt in range(1, Config.MAX_RETRIES + 1):
            try:
                response = openai.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    timeout=Config.TIMEOUT_LONG
                )
                return response.choices[0].message.content.strip()

            except NotFoundError:
                break
            except RateLimitError:
                time.sleep(2 ** attempt)
            except OpenAIError:
                time.sleep(1)

    # Completion model fallback
    for attempt in range(1, Config.MAX_RETRIES + 1):
        try:
            response = openai.completions.create(
                model=Config.COMPLETION_MODEL,
                prompt=user_prompt,
                max_tokens=60,
                temperature=0.7,
                timeout=Config.TIMEOUT_LONG
            )
            return response.choices[0].text.strip()
        except RateLimitError:
            time.sleep(2 ** attempt)
        except OpenAIError:
            time.sleep(1)

    return "Thanks for sharing this!"