from .api import mp_client
from .utils import get_user

client = mp_client()


def is_active_subscription(request):
    return client.is_active_subscription(request=request)
