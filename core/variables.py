import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
DB_NAME = os.getenv("DB_NAME", "default")
DB_USER = os.getenv("DB_USER", "default")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default")
DB_HOST = os.getenv("DB_HOST", "default")
DB_PORT = int(os.getenv("DB_PORT", "default"))
