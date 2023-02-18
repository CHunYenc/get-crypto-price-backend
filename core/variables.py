import environ
import os

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create .env file on /get-crypto-price-backend/.env
# See https://django-environ.readthedocs.io/en/latest/quickstart.html
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Used django-environ package loading environment variables
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
DATABASE = env.db()
CACHE = env.cache()
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
