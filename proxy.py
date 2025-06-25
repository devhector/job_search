import requests
import pandas as pd
from io import StringIO


class Proxy:
    def __init__(self, proxy_api_url) -> None:
        self.proxy_api_url = proxy_api_url

    def random_proxy(self) -> str:
        csv_content = self.get_proxies()

        df = pd.read_csv(
            StringIO(csv_content),
            engine="python",
            quotechar='"',
            true_values=["true"],
            false_values=["false"],
            na_values=["", " ", "NA", "N/A", "null"],
        )

        required_cols = ["alive", "protocol", "proxy"]
        if not all(col in df.columns for col in required_cols):
            missing = [col for col in required_cols if col not in df.columns]
            raise ValueError(f"Missing required columns: {missing}")

        valid_proxies = df[
            (df["alive"])
            & (df["protocol"].str.lower() == "http")
            & (df["proxy"].notna())
        ]

        if valid_proxies.empty:
            print("\n[DEBUG] Unique values on 'alive':", df["alive"].unique())
            print(
                "[DEBUG] protocols:",
                df["protocol"].str.lower().value_counts(),
            )
            print(f"[DEBUG] Proxies alives: {len(df[df['alive']])}")
            raise ValueError("No suitable proxy found")

        return valid_proxies.sample(n=1)["proxy"].iloc[0]

    def get_proxies(self):
        response = requests.get(
            self.proxy_api_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15
        )

        if response.status_code != 200:
            raise ConnectionError(
                f"Failed search proxies (Status {response.status_code}): {response.text[:200]}"
            )

        return response.text
