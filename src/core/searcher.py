from src.platforms.base import Platform


class Searcher:
    def __init__(self, platforms: list[Platform]) -> None:
        self.platforms = platforms

    def search(self, terms: dict) -> list[dict]:
        jobs = []
        for platform in self.platforms:
            jobs.append(
                platform.search_jobs(
                    terms["title"],
                    terms["location"],
                    terms["seniority"],
                    terms["posted_time"],
                )
            )
        return jobs
