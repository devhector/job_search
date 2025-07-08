from src.utils.logger import logger
from src.utils.exceptions import InvalidCookieException
from src.utils.db import Job_database
from src.utils.browser import Browser
from src.platforms.linkedin import Linkedin
from src.notifiers.telegram_bot import Telegram_bot
from src.core.searcher import Searcher
from src.core.messenger import Messenger
from src.core.authenticator import Authenticator
from playwright.sync_api import Playwright
import itertools
import os
import random
import sys
import time
from datetime import datetime, timedelta
import zoneinfo

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class JobSearchOrchestrator:
    """
    Orquestra o processo de busca de vagas, incluindo configuração,
    execução do ciclo de busca e tratamento de exceções.
    """

    def __init__(self, job_titles, locations, seniority_levels):
        self.job_titles = job_titles
        self.locations = locations
        self.seniority_levels = seniority_levels
        self.combinations = list(
            itertools.product(self.job_titles, self.locations, self.seniority_levels)
        )
        self.sp_tz = zoneinfo.ZoneInfo("America/Sao_Paulo")
        self.db = None
        self.browser = None
        self.messenger = None
        self.searcher = None

    def _setup_services(self, playwright: Playwright):
        """Configura e inicializa todos os serviços necessários."""
        logger.info("Configurando serviços...")
        telegram_config = {
            "token_id": os.getenv("TELEGRAM_API_KEY"),
            "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        }
        self.messenger = Messenger([Telegram_bot(telegram_config)])

        self.db = Job_database(
            # db_path=os.getenv("DB_PATH")
        )
        self.browser = Browser(
            playwright=playwright,
            headless=True,
            slow_mo=random.randint(500, 2000),
        )

        linkedin = Linkedin(self.browser)
        authenticator = Authenticator([linkedin])
        authenticator.auth()  # Pode levantar InvalidCookieException

        self.searcher = Searcher([linkedin])
        logger.info("Serviços configurados com sucesso.")

    def _shutdown(self):
        """Encerra os recursos de forma segura."""
        if self.browser:
            self.browser.close()
        if self.db:
            self.db.close()
        logger.info("Recursos liberados.")

    def _perform_search_iteration(self, job_title, location, seniority):
        """Executa uma única iteração do ciclo de busca de vagas."""
        try:
            self.db.delete_expired_jobs()
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
            self.messenger.send("info", {"title": message})

            all_jobs = self.searcher.search(terms)
            all_jobs = [job for group in all_jobs for job in group]

            new_jobs = self.db.filter_new_jobs(all_jobs)
            for job in new_jobs:
                logger.info(f"Enviando vaga: {job['title']}")
                self.messenger.send("job", job)

            self.db.save(new_jobs)

            wait_time = random.randint(300, 3600)
            next_run_dt = datetime.now(self.sp_tz) + timedelta(seconds=wait_time)
            next_run = next_run_dt.strftime("%H:%M:%S")
            msg = f"⏱️ Próxima execução em {wait_time // 60} minutos ({next_run} - horário SP)"
            logger.info(f"\n{msg}")
            self.messenger.send("info", {"title": msg})
            time.sleep(wait_time)

        except Exception as e:
            error_msg = f"Erro durante a execução: {e}"
            logger.error(f"\nError: {error_msg}")
            if self.messenger:
                self.messenger.send("error", {"title": error_msg})
            time.sleep(300)

    def run(self):
        """Inicia o loop infinito de busca de vagas."""
        while True:
            try:
                with sync_playwright() as p:
                    self._setup_services(p)

                    # Loop principal de busca
                    while True:
                        random.shuffle(self.combinations)
                        for job_title, location, seniority in self.combinations:
                            self._perform_search_iteration(
                                job_title, location, seniority
                            )

            except InvalidCookieException as e:
                platform = e.platform_name or "Unknown"
                error_msg = f"O cookie de autenticação do {platform} expirou!"
                logger.error(error_msg)
                # O messenger pode não ter sido inicializado, então criamos um temporário
                # se necessário, mas tentamos usar o existente primeiro.
                if not self.messenger:
                    self.messenger = Messenger(
                        [
                            Telegram_bot(
                                {
                                    "token_id": os.getenv("TELEGRAM_API_KEY"),
                                    "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
                                }
                            )
                        ]
                    )
                self.messenger.send("error", {"title": error_msg})

                logger.info(
                    "Aguardando 6 horas para tentar novamente a autenticação..."
                )
                time.sleep(21600)

            finally:
                self._shutdown()
