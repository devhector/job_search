class Platform:
    def login(self) -> None:
        raise NotImplementedError("Method not implemented")

    def search_jobs(self, title, location, seniority, posted_time=24):
        raise NotImplementedError("Method not implemented")
