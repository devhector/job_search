import sqlite3
import hashlib


class Job_database:
    def __init__(self, db_path: str = "job.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE,
                title TEXT,
                company TEXT,
                location TEXT,
                link TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def delete_expired_jobs(self) -> None:
        self.conn.execute("DELETE FROM jobs WHERE created_at <= datetime('now', '-24 hours')")
        self.conn.commit()

    def filter_new_jobs(self, jobs: list[dict]) -> list[dict]:
        cursor = self.conn.cursor()

        new_jobs = []
        for job in jobs:
            job["job_id"] = self._generate_job_id(job)
            cursor.execute(
                "SELECT 1 FROM jobs WHERE job_id = ?", (job["job_id"],))
            if cursor.fetchone() is None:
                new_jobs.append(job)
        return new_jobs

    def _generate_job_id(self, job: dict) -> str:
        unique_str = f"{job['title'], job['company'], job['location']}"
        return hashlib.sha256(unique_str.encode()).hexdigest()

    def save(self, jobs: list[dict]) -> None:
        cursor = self.conn.cursor()

        for job in jobs:
            cursor.execute(
                """
                INSERT OR IGNORE INTO jobs (job_id, title, company, location, link) VALUES (?, ?, ?, ?, ?)
            """,
                (
                    job["job_id"],
                    job["title"],
                    job["company"],
                    job["location"],
                    job["link"],
                ),
            )
        self.conn.commit()

    def close(self):
        self.conn.close()
