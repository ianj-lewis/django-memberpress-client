"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Open edX - plugin constants
"""

# django stuff
from django.conf import settings

MEMBERPRESS_OPERATION_PREFIX = "memberpress_api_operation_"
OPERATION_GET_MEMBER = MEMBERPRESS_OPERATION_PREFIX + "get_member"
COMPLETE_MEMBER_DICT = [
    "id",
    "email",
    "username",
    "nicename",
    "url",
    "message",
    "registered_at",
    "first_name",
    "last_name",
    "display_name",
    "active_memberships",
    "active_txn_count",
    "expired_txn_count",
    "trial_txn_count",
    "sub_count",
    "login_count",
    "first_txn",
    "latest_txn",
    "address",
    "profile",
    "recent_transactions",
    "recent_subscriptions",
]
MINIMUM_MEMBER_DICT = ["username", "recent_transactions", "recent_subscriptions", "active_memberships"]


class MemberPressAPI_Operations:
    __slots__ = ()
    GET_MEMBER = OPERATION_GET_MEMBER


class MemberPressAPI_Endpoints:
    """
    written by: mcdaniel
    date:       oct-2022
    Codify the data models of the api endpoints and data dicts
    referenced by MemberPress REST API
    """

    # -------------------------------------------------------------------------
    # api end points originating from https://stepwisemath.ai/wp-json/mp/v1/
    # -------------------------------------------------------------------------
    MEMBERPRESS_API_BASE = settings.MEMBERPRESS_API_BASE_URL + "/wp-json/mp/v1/"
    MEMBERPRESS_API_ME_PATH = MEMBERPRESS_API_BASE + "me/"
