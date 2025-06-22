import requests
import pandas as pd


class Proxy:
    def __init__(self, proxy_api_url) -> None:
        self.proxy_api_url = proxy_api_url

    def random_proxy(self):
        csv = self.get_proxies()
        df = pd.read_csv(csv)

        random_line = self.get_random_line(df)

        return random_line["proxy"]

    def get_proxies(self):
        response = requests.get(self.proxy_api_url)

        if response.status_code == 200:
            return response.text
        else:
            raise ValueError(
                f"Cannot get the proxies, status code: {response.status_code}"
            )

    def get_random_line(self, dataframe):
        max_attempts = 100
        attempts = 0

        while attempts < max_attempts:
            random_line = dataframe.sample(n=1)
            if (
                random_line["alive"].iloc[0] == "true"
                and random_line["protocol"].iloc[0] == "http"
            ):
                return random_line
            attempts += 1
        raise ValueError("No suitable proxy found after maximum attempts")
