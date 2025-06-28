from platform import Platform


class Authenticator:
    def __init__(self, platforms: list[Platform]) -> None:
        self.platforms = platforms

    def auth(self):
        for platform in self.platforms:
            platform.login()
