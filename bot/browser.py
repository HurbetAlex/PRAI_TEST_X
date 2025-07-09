import os
import re
import time
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from config import Config


def launch_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=False,
        slow_mo=Config.SLOW_MO,
        proxy={"server": Config.PROXY_URL} if Config.PROXY_URL else None
    )
    context = browser.new_context(
        user_agent=Config.USER_AGENT,
        locale=Config.LOCALE,
        timezone_id=Config.TIMEZONE
    )
    return p, browser, context


def login_to_twitter(context):
    page = context.new_page()
    page.goto("https://x.com/i/flow/login", timeout=Config.TIMEOUT_LONG)

    def click_button(texts):
        selector = ",".join([f'div[role="button"]:has-text("{t}")' for t in texts])
        page.click(selector, timeout=Config.TIMEOUT_LONG)

    # Step 1: username
    page.fill('input[name="text"]', Config.TWITTER_USERNAME, timeout=Config.TIMEOUT_LONG)
    click_button(["Next", "Далее"])
    time.sleep(1)

    # Step 2: sometimes repeat username
    try:
        page.wait_for_selector('input[name="text"]', timeout=Config.TIMEOUT_SHORT)
        page.fill('input[name="text"]', Config.TWITTER_USERNAME)
        click_button(["Next", "Далее"])
        time.sleep(1)
    except PWTimeout:
        pass

    # Step 3: password
    page.fill('input[name="password"]', Config.TWITTER_PASSWORD, timeout=Config.TIMEOUT_LONG)
    click_button(["Log in", "Войти"])
    page.wait_for_url("https://x.com/home", timeout=Config.TIMEOUT_LONG)
    return page


def interact_with_tweet(page, tweet_el, reply_text: str):
    tweet_el.scroll_into_view_if_needed()
    time.sleep(1)
    tweet_el.click()
    time.sleep(2)

    reply_btn = page.locator('button[data-testid="reply"]:visible').first
    reply_btn.click(timeout=Config.TIMEOUT_LONG)
    time.sleep(1)

    textbox = page.locator('textarea[placeholder="Post your reply"], div[role="textbox"]').first
    textbox.wait_for(state="visible", timeout=Config.TIMEOUT_LONG)
    textbox.fill(reply_text)

    send_btn = page.locator(
        'button[data-testid="tweetButtonInline"]:enabled, button[data-testid="tweetButton"]:enabled'
    ).first
    send_btn.click(timeout=Config.TIMEOUT_LONG)
    time.sleep(2)

    page.goto("https://x.com/home", timeout=Config.TIMEOUT_LONG)
    time.sleep(1)

