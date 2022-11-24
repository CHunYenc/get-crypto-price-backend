import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CACHE_REDIS_URL = REDIS_URL

class developmentConfig(Config):
    ENV = "development"
    DEBUG = True

class productionConfig(Config):
    ENV = "production"
    DEBUG = False

class testConfig(Config):
    ENV = "test"
    TESTING = True
    REDIS_HOST = None
    REDIS_PORT = 6379
    CELERY_BROKER_URL = None
    CELERY_RESULT_BACKEND = None
    CACHE_REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


config = {
    "development": developmentConfig,
    "production": productionConfig,
    "test": testConfig,
}
