import os
import random
import time

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from authenticator import Authenticator
from browser import Browser
from db import Job_database
from linkedin import Linkedin
from messenger import Messenger
from searcher import Searcher
from telegram_bot import Telegram_bot


def main():
    load_dotenv()

    db = None
    browser = None

    with sync_playwright() as p:
        try:
            messenger, searcher, db, browser = config(p)

            while True:
                try:
                    job_title = random_job_title()
                    location = random_location()
                    seniority_map = {"junior": "1",
                                     "pleno": "2", "senior": "3"}
                    seniority = random_seniority(seniority_map)
                    posted_time = random.randint(24, 36)

                    terms = {
                        "title": job_title,
                        "location": location,
                        "seniority": seniority,
                        "posted_time": posted_time,
                    }

                    message = (
                        "Buscando vagas com os termos:\n"
                        f"- *Título:* `{terms['title']}`\n"
                        f"- *Local:* `{terms['location']}`\n"
                        f"- *Senioridade:* `{', '.join(terms['seniority'])}`\n"
                        f"- *Postado nas últimas:* `{terms['posted_time']}h`"
                    )

                    print(f"\n{message}")
                    messenger.send("info", {"title": message})

                    all_jobs = searcher.search(terms)
                    all_jobs = [job for group in all_jobs for job in group]

                    new_jobs = db.filter_new_jobs(all_jobs)
                    for job in new_jobs:
                        print(f"Enviando vaga: {job['title']}")
                        messenger.send("job", job)

                    db.save(new_jobs)

                    wait_time = random.randint(300, 3600)
                    next_run = time.strftime(
                        "%H:%M:%S", time.localtime(time.time() + wait_time)
                    )
                    msg = (
                        f"⏱️ Próxima execução em {wait_time // 60} minutos ({next_run})"
                    )
                    print(f"\n{msg}")
                    messenger.send("info", {"title": msg})
                    time.sleep(wait_time)

                except KeyboardInterrupt:
                    print("\nInterrompido pelo usuário")
                    break
                except Exception as e:
                    error_msg = f"Erro durante a execução: {e}"
                    print(f"\nError: {error_msg}")
                    messenger.send("error", {"title": error_msg})
                    print("⏳ Reiniciando após 5 minutos...")
                    time.sleep(300)

        finally:
            if browser:
                browser.close()
            if db:
                db.close()


def config(playwright) -> tuple[Messenger, Searcher, Job_database, Browser]:
    telegram_config = {
        "token_id": os.getenv("TELEGRAM_API_KEY"),
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
    }

    db = Job_database()
    browser = Browser(
        playwright=playwright,
        headless=True,
        slow_mo=random.randint(500, 2000),
    )

    linkedin = Linkedin(browser)
    authenticator = Authenticator([linkedin])
    authenticator.auth()

    messenger = Messenger([Telegram_bot(telegram_config)])
    searcher = Searcher([linkedin])

    return messenger, searcher, db, browser


def random_job_title():
    terms = ["Java", "Java Developer", "Desenvolvedor Java", "Java Backend"]
    return random.choice(terms)


def random_location():
    terms = ["Brasil", "Brazil", "Rio de Janeiro",
             "Remoto", "Rio de Janeiro (Remoto)"]
    return random.choice(terms)


def random_seniority(seniority_map):
    levels = ["junior", "pleno", "senior"]
    selected = random.sample(levels, random.randint(1, 2))
    return [seniority_map["junior"]]


if __name__ == "__main__":
    main()
