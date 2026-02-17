from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
GRAPH_VERSION = os.getenv("FACEBOOK_GRAPH_VERSION", "v19.0")
