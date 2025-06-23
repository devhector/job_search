import os
import json


class Linkedin:
    def __init__(self, browser):
        self.BASE_URL = "https://www.linkedin.com"
        self.COOKIE_PATH = "cookies/linkedin.json"
        self.browser = browser

    def login(self):
        if not os.path.exists(self.COOKIE_PATH):
            self._manual_login()

        self._load_cookie()

    def _manual_login(self) -> None:
        new_browser = self.browser.new_browser()

        try:
            new_context = new_browser.new_context()
            page = new_context.new_page()
            page.goto(f"{self.BASE_URL}/login")
            print("Please login so that the cookie can be saved!")
            page.wait_for_selector(
                "div.share-box-feed-entry-toolbar__wrapper.share-box-feed-entry__tool-bar",
                timeout=300000,
            )
            self._save_cookie(page)
        except Exception as e:
            print(e)
        finally:
            new_browser.close()

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
        seniority_param = ",".join(seniority)
        search_url = (
            f"{self.BASE_URL}/jobs/search/"
            f"?keywords={title}"
            f"&location={location}"
            f"&f_TPR=r{seconds}"
            f"&f_E={seniority_param}"
        )

        page = self.browser.goto(search_url)

        try:
            page.wait_for_selector("div.job-card-container", timeout=15000)
        except Exception as e:
            print("List of jobs cannot be opened.")
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
                print(f"An error occurred: {e}")
                continue
        return jobs_data
