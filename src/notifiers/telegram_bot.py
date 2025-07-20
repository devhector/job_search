from src.core.message import Message
from src.notifiers.base import Notifier
from src.utils.logger import logger


class Telegram_bot(Notifier):
    def __init__(self, config: dict) -> None:
        self.token_id = config["token_id"]
        self.chat_id = config["chat_id"]
        self.BASE_URL = f"https://api.telegram.org/bot{self.token_id}"

    def notify(self, message: Message, retries=5, delay=5) -> None:
        payload = {
            "chat_id": self.chat_id,
            "text": self._prettify(message),
            "parse_mode": "Markdown",
        }
        for i in range(retries):
            try:
                response = requests.post(f"{self.BASE_URL}/sendMessage", data=payload)
                response.raise_for_status()
                return
            except requests.exceptions.RequestException as e:
                if i < retries - 1:
                    logger.warning(
                        f"Failed to send notification (attempt {i + 1}/{retries}). Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    logger.error(
                        f"Failed to send notification after {retries} attempts: {e}"
                    )

    def _prettify(self, message: Message) -> str:
        if message["type"] == "job":
            return (
                f"📌 *{message['title']}*\n"
                f"🏢 {message['company']}\n"
                f"📍 {message['location']}\n"
                f"🔗 [Ver vaga]({message['link']})\n"
                "-----------------------------"
            )
        elif message["type"] == "info":
            return f"ℹ️ {message['title']}"
        elif message["type"] == "error":
            return f"❌ {message['title']}"
        else:
            return f"🔔 {message.get('title', 'Mensagem recebida')}"


import time

import requests
