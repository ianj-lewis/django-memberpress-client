# bootstrap the test environment
from memberpress_client.settings import local
from django.conf import settings

settings.configure(default_settings=local)
