import itertools
import os
import random
import time
from datetime import datetime, timedelta
import zoneinfo

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from authenticator import Authenticator
from browser import Browser
from db import Job_database
from linkedin import Linkedin
from logger import logger
from messenger import Messenger
from searcher import Searcher
from telegram_bot import Telegram_bot


def main():
    load_dotenv()

    db = None
    browser = None

    job_titles = [
        "Java",
        "Java Developer",
        "Desenvolvedor Java",
        "Java Backend",
        "Python",
        "Python Backend",
        "PHP",
        "PHP Backend",
    ]
    locations = [
        "Brasil",
        "Brazil",
        "Rio de Janeiro",
        "Remoto",
        "Rio de Janeiro (Remoto)",
    ]
    seniority_levels = ["junior"]

    combinations = list(itertools.product(job_titles, locations, seniority_levels))
    sp_tz = zoneinfo.ZoneInfo("America/Sao_Paulo")

    with sync_playwright() as p:
        try:
            messenger, searcher, db, browser = config(p)

            while True:
                random.shuffle(combinations)

                for job_title, location, seniority in combinations:
                    try:
                        posted_time = random.randint(24, 36)

                        terms = {
                            "title": job_title,
                            "location": location,
                            "seniority": [seniority],
                            "posted_time": posted_time,
                        }

                        message = (
                            "Buscando vagas com os termos:\n"
                            f"- *Título:* `{terms['title']}`\n"
                            f"- *Local:* `{terms['location']}`\n"
                            f"- *Senioridade:* `{seniority}`\n"
                            f"- *Postado nas últimas:* `{terms['posted_time']}h`"
                        )

                        logger.info(f"\n{message}")
                        messenger.send("info", {"title": message})

                        all_jobs = searcher.search(terms)
                        all_jobs = [job for group in all_jobs for job in group]

                        new_jobs = db.filter_new_jobs(all_jobs)
                        for job in new_jobs:
                            logger.info(f"Enviando vaga: {job['title']}")
                            messenger.send("job", job)

                        db.save(new_jobs)

                        wait_time = random.randint(300, 3600)
                        next_run_dt = datetime.now(sp_tz) + timedelta(seconds=wait_time)
                        next_run = next_run_dt.strftime("%H:%M:%S")
                        msg = f"⏱️ Próxima execução em {wait_time // 60} minutos ({next_run} - horário SP)"
                        logger.info(f"\n{msg}")
                        messenger.send("info", {"title": msg})
                        time.sleep(wait_time)

                    except Exception as e:
                        error_msg = f"Erro durante a execução: {e}"
                        logger.error(f"\nError: {error_msg}")
                        messenger.send("error", {"title": error_msg})
                        logger.info("⏳ Reiniciando após 5 minutos...")
                        time.sleep(300)

        except KeyboardInterrupt:
            logger.info("\nInterrompido pelo usuário. Encerrando...")
        finally:
            if browser:
                browser.close()
            if db:
                db.close()
            logger.info("Recursos liberados. Programa encerrado.")


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


if __name__ == "__main__":
    main()
