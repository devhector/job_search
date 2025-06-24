import os
from bot import Telegram_bot
from browser import Browser
from db import Job_database
from dotenv import load_dotenv
from linkedin import Linkedin
from playwright.sync_api import sync_playwright


def main():
    load_dotenv()

    telegram_api_key = os.getenv("TELEGRAM_API_KEY")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    with sync_playwright() as p:
        db = Job_database()
        browser = Browser(playwright=p, headless=True)
        linkedin = Linkedin(browser)
        bot = Telegram_bot(telegram_api_key, chat_id)

        seniority = {"junior": "1", "pleno": "2", "senior": "3"}

        try:
            linkedin.login()
            jobs = linkedin.search_jobs(
                title="Java",
                location="Brasil",
                seniority=[seniority["junior"], seniority["pleno"]],
                posted_time=24,
            )

            new_jobs = db.filter_new_jobs(jobs)
            for job in new_jobs:
                print(f"send job: {job['title']}")
                bot.send(prettify(job))

            db.save(new_jobs)
            db.close()
        except Exception as e:
            print(e)
        finally:
            browser.close()


def prettify(job):
    return (
        f"📌 *{job['title']}*\n"
        f"🏢 {job['company']}\n"
        f"📍 {job['location']}\n"
        f"🔗 [Ver vaga]({job['link']})\n"
        "-----------------------------"
    )


if __name__ == "__main__":
    main()
