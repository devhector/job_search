from src.core.message import Message
from src.notifiers.base import Notifier


class Messenger:
    def __init__(self, notifiers: list[Notifier]) -> None:
        self.notifiers = notifiers

    def send(self, message: Message) -> None:
        for notifier in self.notifiers:
            notifier.notify(message)
