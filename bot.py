import requests


class Telegram_bot:
    def __init__(self, token_id, chat_id) -> None:
        self.token_id = token_id
        self.chat_id = chat_id
        self.BASE_URL = f"https://api.telegram.org/bot{token_id}"

    def send(self, message) -> None:
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(f"{self.BASE_URL}/sendMessage", data=payload)
        response.raise_for_status()
