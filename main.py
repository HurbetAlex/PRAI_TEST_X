import sys
from config import Config
from bot.browser import launch_browser, login_to_twitter, interact_with_tweet
from bot.scraper import get_feed_tweets
from bot.ai import generate_reply
from bot.database import init_db, log_to_db


def main():
    init_db()
    p, browser, context = launch_browser()
    try:
        page = login_to_twitter(context)
        tweets = get_feed_tweets(page)
        if not tweets:
            print("No tweets found.")
            return
        top = tweets[0]
        reply = generate_reply(top["content"])
        interact_with_tweet(page, top["element"], reply)
        log_to_db({
            "handle": Config.TWITTER_USERNAME,
            "tweet": top["content"],
            "reply": reply,
            "likes": top["likes"],
            "retweets": top["retweets"]
        })
        print("✅ Done and logged.")
    finally:
        browser.close()
        p.stop()


if __name__ == "__main__":
    main()