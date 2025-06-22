from typing import Self
from playwright.sync_api import sync_playwright


class Browser:
    def __init__(self, headless=False):
        self.playwright = sync_playwright.start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def goto(self, url, timeout):
        self.page.goto(url=url, timeout=timeout)
        return self.page

    def close(self):
        self.browser.close()
        self.playwright.stop()
