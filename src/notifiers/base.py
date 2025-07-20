from src.core.message import Message


class Notifier:
    def notify(self, message: Message) -> None:
        raise NotImplementedError("Method not implemented")
