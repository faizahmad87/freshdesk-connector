import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    FRESHDESK_DOMAIN = os.environ["FRESHDESK_DOMAIN"]
    FRESHDESK_API_KEY = os.environ["FRESHDESK_API_KEY"]

    BASE_URL = f"https://{FRESHDESK_DOMAIN}.freshdesk.com/api/v2"

    REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))
