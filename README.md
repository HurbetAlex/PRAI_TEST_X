# Twitter Interaction Bot

A Python application that automates Twitter (X) interactions without using the official API. It logs into your account via Playwright, scrapes the home feed, selects the most engaging tweet, reposts and replies with an AI-generated response, and logs actions to a SQLite database.

## Setup and Environment Configuration

1. **Clone the Repository**

   ```bash
   git clone <repo-url>
   cd twitter-bot
   ```

2. **Create a Virtual Environment & Install Dependencies**

   ```bash
   python -m venv .venv
   # Activate the environment:
   source .venv/bin/activate   # macOS/Linux
   .\.venv\Scripts\activate  # Windows

   pip install -r requirements.txt
   playwright install
   ```

3. **Configure Environment Variables**
   Create a file named `.env` in the repository root with the following:

   ```dotenv
   # Twitter credentials
   TWITTER_USERNAME=your_username_or_email
   TWITTER_PASSWORD=your_password

   # Optional proxy settings
   PROXY_URL=socks5://user:pass@proxy.host:port
   USER_AGENT=Your custom User-Agent string

   # OpenAI API key
   OPENAI_API_KEY=sk-...

   # SQLite database file path
   SQLITE_PATH=twitterbot.sqlite3

   # Retry and timeout settings
   MAX_RETRIES=2
   TIMEOUT_SHORT=5000
   TIMEOUT_LONG=30000
   SLOW_MO=80

   # Localization
   LOCALE=en-US
   TIMEZONE=America/New_York
   ```

## Instructions on How to Run the Script

1. Ensure your `.env` is populated and your virtual environment is active.
2. Initialize or migrate the database (creates tables if needed):

   ```bash
   python main.py --init-db
   ```
3. Run the bot to perform one interaction cycle:

   ```bash
   python main.py
   ```
4. (Optional) To save authenticated session and bypass Cloudflare checks later:

   ```bash
   python save_auth.py
   ```

## Example of a Successful Repost and AI-Generated Reply

```text
[2025-07-09 18:03:27] Logged in as @YourHandle
Selected tweet by @FabrizioRomano with 372 likes and 797 retweets:
> "Club Brugge are still not giving green light to AC Milan final €38m package bid for Ardon Jashari..."
Reposted and replied:
> "Exciting times ahead, let's see how this transfer saga unfolds!"
✅ Action logged to database.
```

## SQL Schema File

```sql
-- schema.sql
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handle TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweet TEXT NOT NULL,
    reply TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    retweets INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp);
```

---

For more details, see the code modules in the `bot/` directory and adjust settings in `config.py` as needed.
