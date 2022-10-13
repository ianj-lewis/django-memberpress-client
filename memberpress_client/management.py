"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Open edX - membership management.
This is currently the only real consumer of MPClient
"""

# our stuff
from client import mp_client

client = mp_client()


def is_active_subscription(request):
    """
    returns True if the current user has an active subscription, False otherwise.

    active:
    means that the user has subscribed either to a trial
    subscription that has not yet expired, or, the user has a paid
    subscription that has not yet expired.
    """
    return client.is_active_subscription(request=request)
