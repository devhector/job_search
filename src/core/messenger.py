from src.notifiers.base import Notifier


class Messenger:
    def __init__(self, notifiers: list[Notifier]) -> None:
        self.notifiers = notifiers

    def send(self, type_: str, message: dict) -> None:
        for notifier in self.notifiers:
            notifier.notify(type_, message)
