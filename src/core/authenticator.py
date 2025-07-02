from src.platforms.base import Platform
from src.utils.exceptions import InvalidCookieException
from src.utils.logger import logger


class Authenticator:
    def __init__(self, platforms: list[Platform]) -> None:
        self.platforms = platforms

    def auth(self):
        for platform in self.platforms:
            try:
                platform.login()
            except InvalidCookieException as e:
                logger.error(f"Authentication failed for {type(platform).__name__}: {e}")
                raise e
