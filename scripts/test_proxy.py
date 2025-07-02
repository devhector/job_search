import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.utils.proxy import Proxy


def test():
    load_dotenv()

    proxy_api_url = os.getenv("PROXY_API_URL")
    proxy = Proxy(proxy_api_url)

    try:
        print(proxy.random_proxy())
    except Exception as e:
        print(f"ERROR: {e}")


test()
