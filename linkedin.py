import os
import json
import time
import random

import os
import json
import time
import random

from platform import Platform
from logger import logger
from exceptions import InvalidCookieException


class Linkedin(Platform):
    def __init__(self, browser):
        self.BASE_URL = "https://www.linkedin.com"
        self.COOKIE_PATH = "cookies/linkedin.json"
        self.TOP_BAR_FEED = (
            "div.share-box-feed-entry-toolbar__wrapper.share-box-feed-entry__tool-bar"
        )
        self.browser = browser

    def login(self):
        if not os.path.exists(self.COOKIE_PATH):
            self._manual_login()

        self._load_cookie()
        self._check_login()

        time.sleep(random.uniform(1.0, 3.0))

    def _check_login(self) -> None:
        try:
            page = self.browser.page
            page.goto(self.BASE_URL)
            page.wait_for_selector(
                self.TOP_BAR_FEED,
                timeout=10000,  # Reduced timeout for faster feedback
            )
        except Exception as e:
            logger.error("Login check failed. The cookie might be invalid or expired.")
            raise InvalidCookieException(
                "Linkedin cookie is invalid.", platform_name="LinkedIn"
            ) from e

    def _manual_login(self) -> None:
        try:
            page = self.browser.page
            page.goto(f"{self.BASE_URL}/login")
            logger.info("Please login so that the cookie can be saved!")
            page.wait_for_selector(
                self.TOP_BAR_FEED,
                timeout=300000,
            )
            self._save_cookie(page)
        except Exception as e:
            logger.error(e)
            raise e

    def _save_cookie(self, page) -> None:
        os.makedirs(os.path.dirname(self.COOKIE_PATH), exist_ok=True)

        cookie = page.context.cookies()
        with open(self.COOKIE_PATH, "w") as file:
            json.dump(cookie, file)

    def _load_cookie(self) -> None:
        if not os.path.exists(self.COOKIE_PATH):
            raise FileNotFoundError(f"Cookie file not found: {self.COOKIE_PATH}")

        with open(self.COOKIE_PATH, "r") as file:
            cookie = json.load(file)
            self.browser.add_cookie(cookie)

    def search_jobs(self, title, location, seniority, posted_time=24):
        seconds = posted_time * 60 * 60

        seniority_map = {"junior": "1", "pleno": "2", "senior": "3"}
        seniority_ids = [
            seniority_map[level.lower()]
            for level in seniority
            if level.lower() in seniority_map
        ]

        if not seniority_ids:
            raise Exception(f"Nenhuma senioridade válida encontrada em: {seniority}")

        seniority_param = ",".join(seniority_ids)

        search_url = (
            f"{self.BASE_URL}/jobs/search/"
            f"?keywords={title}"
            f"&location={location}"
            f"&f_TPR=r{seconds}"
            f"&f_E={seniority_param}"
        )

        page = self.browser.goto(search_url)
        time.sleep(random.uniform(1.0, 5.0))

        try:
            page.wait_for_selector("div.job-card-container", timeout=15000)
        except Exception as e:
            logger.error("List of jobs cannot be opened.")
            raise e

        return self._jobs_parser(page.query_selector_all("div.job-card-container"))

    def _jobs_parser(self, jobs):
        jobs_data = []
        for job in jobs:
            try:
                title_el = job.query_selector("a.job-card-container__link")
                company_el = job.query_selector("div.artdeco-entity-lockup__subtitle")
                location_el = job.query_selector(
                    "ul.job-card-container__metadata-wrapper li"
                )

                title = title_el.inner_text().strip()
                company = company_el.inner_text().strip()
                location = location_el.inner_text().strip()
                link = title_el.get_attribute("href").strip()

                if link.startswith("/"):
                    link = "https://www.linkedin.com" + link

                jobs_data.append(
                    {
                        "title": title,
                        "company": company,
                        "location": location,
                        "link": link,
                    }
                )

            except Exception as e:
                logger.error(f"An error occurred: {e}")
                continue
        return jobs_data
