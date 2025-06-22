from telegram import Bot


class Telegram_bot:
    def __init__(self, token_id, chat_id) -> None:
        self.bot = Bot(token=token_id)
        self.chat_id = chat_id

    def send(self, message) -> None:
        self.bot.send_message(text=message, chat_id=self.chat_id)
