Twitter Interaction Bot

This repository contains a Python application that automates Twitter (X) interactions without using the official API. It logs into your account via Playwright, scrapes the home feed, selects the most engaging tweet, reposts and replies with an AI-generated response, and logs all actions to a SQLite database.

Features

Browser Automation: Uses Playwright to simulate human-like browsing and interaction.

Cloudflare Bypass: Handles login flow and Cloudflare checks reliably.

Feed Scraping: Extracts the latest 20 tweets from the home feed and scores them by likes + retweets.

AI Response: Generates context-aware, human-like replies via OpenAI models (gpt-4 → gpt-3.5-turbo → text-davinci-003 fallback).

Database Logging: Records each session’s handle, tweet content, AI reply, and engagement metrics in SQLite.

Config-Driven: All secrets and settings live in a central config.py loaded from .env.

Project Structure

├── README.md            # This file
├── config.py            # Central configuration
├── main.py              # Entry point
├── bot/
│   ├── ai.py            # AI reply generation
│   ├── browser.py       # Playwright login & interaction
│   ├── scraper.py       # Tweet scraping
│   └── database.py      # SQLite init & logging
└── .env                 # Environment variables (not committed)

Setup

Clone the repo

git clone <repo-url>
cd twitter-bot

Create a virtual environment & install dependencies

python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
playwright install

**Populate **.env (base directory)

TWITTER_USERNAME=your_username_or_email
TWITTER_PASSWORD=your_password
PROXY_URL=                 # optional
USER_AGENT=               # optional custom UA
OPENAI_API_KEY=your_key
SQLITE_PATH=twitterbot.sqlite3
MAX_RETRIES=2
TIMEOUT_SHORT=5000
TIMEOUT_LONG=30000
SLOW_MO=80
LOCALE=en-US
TIMEZONE=America/New_York

Run the bot

python main.py

How It Works

Initialization: main.py loads config, initializes the SQLite database, and launches Playwright.

Login: bot/browser.py carries out the login flow, handling both username & password steps and waiting for the home feed.

Scrape Feed: bot/scraper.py scrolls the feed, grabs the first 20 tweets, and ranks them by engagement.

Generate Reply: bot/ai.py tries OpenAI chat models, falling back to a completion model if needed, with retries.

Interact: bot/browser.py reposts and replies to the top tweet, then returns to the feed.

Log: bot/database.py saves the tweet, reply, and metrics to SQLite.

Customization

Models & Retries: Adjust CHAT_MODELS, COMPLETION_MODEL, and MAX_RETRIES in config.py.

Timeouts & Pace: Tune TIMEOUT_SHORT, TIMEOUT_LONG, and SLOW_MO for your network and machine.

Proxy & UA: Set PROXY_URL and USER_AGENT in .env to use custom proxies or user agents.

Troubleshooting

Login Issues: Ensure .env credentials are correct and that you can log in manually. Increase timeouts if needed.

Cloudflare Check: You may need to manually complete a CF challenge once; consider saving storage state.

OpenAI Errors: Verify your API key and model access. The bot automatically falls back to available models.

License

MIT License © Oleksandr Matiushenko