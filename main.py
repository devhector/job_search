import os
import time
import random
from bot import Telegram_bot
from browser import Browser
from db import Job_database
from dotenv import load_dotenv
from linkedin import Linkedin
from playwright.sync_api import sync_playwright


def main():
    load_dotenv()

    while True:
        try:
            print("\nBuscando busca de vagas...")
            search()

            wait_time = random.randint(300, 3600)
            next_run = time.strftime(
                "%H:%M:%S", time.localtime(time.time() + wait_time)
            )
            print(f"\nPróxima execução em {wait_time // 60} minutos ({next_run})...")
            time.sleep(wait_time)

        except KeyboardInterrupt:
            print("\ninterrompido pelo usuário")
            break
        except Exception as e:
            print(f"\nErro durante a execução: {e}")
            print("Reiniciando busca após 5 minutos...")
            time.sleep(300)


def search():
    telegram_api_key = os.getenv("TELEGRAM_API_KEY")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    browser = None
    db = None

    with sync_playwright() as p:
        try:
            browser = Browser(
                playwright=p,
                headless=True,
                slow_mo=random.randint(500, 2000),
            )

            db = Job_database()
            linkedin = Linkedin(browser)
            bot = Telegram_bot(telegram_api_key, chat_id)

            seniority = {"junior": "1", "pleno": "2", "senior": "3"}

            linkedin.login()

            job_title = random_job_title()
            posted_time = random.randint(24, 36)
            seniority_codes = random_seniority(seniority)
            location = random_location()

            jobs = linkedin.search_jobs(
                title=job_title,
                location=location,
                seniority=seniority_codes,
                posted_time=posted_time,
            )

            new_jobs = db.filter_new_jobs(jobs)
            for job in new_jobs:
                print(f"Enviando vaga: {job['title']}")
                bot.send(prettify(job))

            db.save(new_jobs)

        except Exception as e:
            print(f"Erro durante a busca: {e}")
        finally:
            if db:
                db.close()
            if browser:
                browser.close()


def random_job_title():
    terms = ["Java", "Java Developer", "Desenvolvedor Java", "Java Backend"]
    return random.choice(terms)


def random_location():
    terms = ["Brasil", "Brazil", "Rio de Janeiro", "Remoto", "Rio de Janeiro (Remoto)"]
    return random.choice(terms)


def random_seniority(seniority_map):
    levels = ["junior", "pleno", "senior"]
    selected = random.sample(levels, random.randint(1, 2))
    return [seniority_map[level] for level in selected]


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
