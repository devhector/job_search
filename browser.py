class Browser:
    def __init__(self, playwright, headless=False, proxy_settings=None, slow_mo=0):
        self.playwright = playwright
        self.browser = self.new_browser(
            headless=headless, proxy_settings=proxy_settings, slow_mo=slow_mo
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def goto(self, url, timeout=60000):
        self.page.goto(url=url, timeout=timeout)
        return self.page

    def add_cookie(self, cookie) -> None:
        self.context.add_cookies(cookie)

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def new_browser(self, headless=False, proxy_settings=None, slow_mo=0):
        return self.playwright.chromium.launch(
            headless=headless, proxy=proxy_settings, slow_mo=slow_mo
        )
