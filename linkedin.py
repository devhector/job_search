import json
import os


class Linkedin:
    def __init__(self, browser):
        self.BASE_URL = "https://www.linkedin.com/"
        self.COOKIE_PATH = "cookies/linkedin.json"
        self.browser = browser

    def login(self):
        if not os.path.exists(self.COOKIE_PATH):
            self._manual_login()

        self._load_cookie()

    def _manual_login(self) -> None:
        new_browser = self.browser.new_browser()
        new_context = new_browser.new_context()
        page = new_context.new_page()
        page.goto(f"{self.BASE_URL}/login")
        print("Please login so that the cookie can be saved!")
        page.wait_for_timeout(60000)
        try:
            self._save_cookie(page)
        except Exception as e:
            print(e)
        new_browser.close()

    def _save_cookie(self, page) -> None:
        cookie = page.context.cookies()
        with open(self.COOKIE_PATH, "w") as file:
            json.dump(cookie, file)

    def _load_cookie(self) -> None:
        with open(self.COOKIE_PATH, "r") as file:
            cookie = json.load(file)
            self.browser.add_cookie(cookie)
