import os
import random
import sys

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from authenticator import Authenticator
from browser import Browser
from linkedin import Linkedin
from logger import logger


def main():
    """Manually logs into platforms to create/update session cookies."""
    load_dotenv()

    # Path to the cookie file
    cookie_path = "cookies/linkedin.json"

    # Remove existing cookie file to ensure a fresh login
    if os.path.exists(cookie_path):
        logger.info(f"Removing existing cookie file at {cookie_path} to force new login.")
        os.remove(cookie_path)

    browser = None
    with sync_playwright() as p:
        try:
            logger.info("Starting browser in interactive mode for manual login...")
            browser = Browser(
                playwright=p,
                headless=False,  # Must be False for user interaction
                slow_mo=random.randint(50, 200),
            )

            linkedin = Linkedin(browser)
            authenticator = Authenticator([linkedin])

            logger.info("Please log in to LinkedIn in the browser window...")
            authenticator.auth()

            logger.info("Login successful! Cookie file has been created.")

        except Exception as e:
            logger.error(f"An error occurred during the manual login process: {e}")
            sys.exit(1)
        finally:
            if browser:
                browser.close()
            logger.info("Browser closed. Process finished.")


if __name__ == "__main__":
    main()
