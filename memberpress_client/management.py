"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Open edX - membership management.
This is currently the only real consumer of MPClient
"""

from member import Member


def is_active_subscription(request):
    member = Member(request=request)
    return member.is_active_subscription
