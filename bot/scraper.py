import time
from playwright.sync_api import Page
from config import Config


def get_feed_tweets(page: Page) -> list:
    page.mouse.wheel(0, 800)
    time.sleep(2)
    articles = page.query_selector_all("article")
    tweets = []
    for el in articles:
        content = el.inner_text().strip()
        if not content:
            continue
        def metric(key):
            sel = f'div[data-testid="{key}"]'
            try:
                return int(el.query_selector(sel).inner_text().replace(',', ''))
            except:
                return 0
        tweets.append({
            "element": el,
            "content": content,
            "likes": metric("like"),
            "retweets": metric("retweet")
        })
        if len(tweets) >= 20:
            break
    return sorted(tweets, key=lambda x: x["likes"] + x["retweets"], reverse=True)