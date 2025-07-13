from src.utils.logger import logger
from src.core.orchestrator import JobSearchOrchestrator
import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    load_dotenv()

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

    orchestrator = JobSearchOrchestrator(
        job_titles, locations, seniority_levels)
    try:
        orchestrator.run()
    except KeyboardInterrupt:
        logger.info("\nInterrompido pelo usuário. Encerrando...")
        orchestrator.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
