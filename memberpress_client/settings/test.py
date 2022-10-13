import os
from dotenv import load_dotenv

load_dotenv()

MEMBERPRESS_API_KEY = os.getenv("MEMBERPRESS_API_KEY")
MEMBERPRESS_API_KEY_NAME = "MEMBERPRESS-API-KEY"
MEMBERPRESS_API_BASE_URL = "https://stepwisemath.ai/"
MEMBERPRESS_CACHE_EXPIRATION = 300
MEMBERPRESS_SENSITIVE_KEYS = [
    "password",
    "token",
    "client_id",
    "client_secret",
    "Authorization",
    "secret",
]
DEBUG = True
LOGGING_CONFIG = None
LOGGING = None
FORCE_SCRIPT_NAME = None
INSTALLED_APPS = []
ALLOWED_HOSTS = []
EMAIL_BACKEND = None
USE_I18N = False
