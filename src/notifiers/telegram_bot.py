import time
import requests
from src.utils.logger import logger
from src.notifiers.base import Notifier


class Telegram_bot(Notifier):
    def __init__(self, config: dict) -> None:
        self.token_id = config["token_id"]
        self.chat_id = config["chat_id"]
        self.BASE_URL = f"https://api.telegram.org/bot{self.token_id}"

    def notify(self, type_: str, message: dict, retries=5, delay=5) -> None:
        payload = {
            "chat_id": self.chat_id,
            "text": self._prettify(type_, message),
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

    def _prettify(self, type_: str, message: dict) -> str:
        if type_ == "job":
            return (
                f"📌 *{message['title']}*\n"
                f"🏢 {message['company']}\n"
                f"📍 {message['location']}\n"
                f"🔗 [Ver vaga]({message['link']})\n"
                "-----------------------------"
            )
        elif type_ == "info":
            return f"ℹ️ {message['title']}"
        elif type_ == "error":
            return f"❌ {message['title']}"
        else:
            return f"🔔 {message.get('title', 'Mensagem recebida')}"
