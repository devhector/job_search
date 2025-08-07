import time
import random
import urllib.parse

from src.platforms.base import Platform
from src.utils.logger import logger


class Nerdin(Platform):
    def __init__(self, browser):
        self.BASE_URL = "https://www.nerdin.com.br"
        self.COOKIE_PATH = ".config/cookies/nerdin.json"
        self.browser = browser

    def search_jobs(self, title, location, seniority, posted_time=24):
        seniority_map = {"junior": "3", "pleno": "2", "senior": "1"}

        seniority_ids = [
            seniority_map[level.lower()]
            for level in seniority
            if level.lower() in seniority_map
        ]

        if not seniority_ids:
            raise Exception(f"Nenhuma senioridade válida encontrada em: {seniority}")

        params = {
            "PalavraChave": title,
            "CodigoCidade": "0",  # 0 = Todas as cidades
            "CodigoCargo": "15,2,8,6,4",  # Cargos mais comuns para dev
            "CodigoNivel": ",".join(seniority_ids),
            "CodigoVaga": "",
            "CodigoEmpresa": "0",
        }

        search_url = f"{self.BASE_URL}/vagas?{urllib.parse.urlencode(params)}"
        page = self.browser.goto(search_url)
        time.sleep(random.uniform(2.0, 5.0))

        try:
            page.wait_for_selector("#divListaVagas", timeout=15000)
            lista_vagas = page.query_selector("#divListaVagas")
            jobs = lista_vagas.query_selector_all(
                "div.container[style*='border-color:#A9CCE3']"
            )
        except Exception as e:
            logger.error("Lista de vagas não pode ser carregada.")
            raise e

        return self._jobs_parser(jobs)

    def _jobs_parser(self, jobs):
        jobs_data = []
        for job in jobs:
            try:
                title_el = job.query_selector("span[style*='font-size:18px'] b")
                title = title_el.inner_text().strip() if title_el else ""

                if title.startswith("•"):
                    title = title[1:].strip()

                company_el = job.query_selector(
                    "a[href*='empresa?CodigoEmpresa'] button"
                )
                company = company_el.inner_text().strip() if company_el else ""

                location_el = job.query_selector("a[href*='CodigoCidade'] button")
                location = location_el.inner_text().strip() if location_el else ""

                link_el = job.query_selector("a[href^='vaga/']")
                link = ""
                if link_el:
                    href = link_el.get_attribute("href")
                    link = f"{self.BASE_URL}/{href}" if href else ""

                if title and link:
                    jobs_data.append(
                        {
                            "title": title,
                            "company": company,
                            "location": location,
                            "link": link,
                            "type": "job",
                        }
                    )

            except Exception as e:
                logger.error(f"Erro ao processar vaga: {e}")
                continue

        return jobs_data
