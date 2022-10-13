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

COMPLETE_SUBSCRIPTION_DICT = [
    "coupon",
    "membership",
    "member",
    "id",
    "subscr_id",
    "gateway",
    "price",
    "period",
    "period_type",
    "limit_cycles",
    "limit_cycles_num",
    "limit_cycles_action",
    "limit_cycles_expires_after",
    "limit_cycles_expires_type",
    "prorated_trial",
    "trial",
    "trial_days",
    "trial_amount",
    "trial_tax_amount",
    "trial_total",
    "status",
    "created_at",
    "total",
    "tax_rate",
    "tax_amount",
    "tax_desc",
    "tax_class",
    "cc_last4",
    "cc_exp_month",
    "cc_exp_year",
    "token",
    "tax_compound",
    "tax_shipping",
    "response",
]

COMPLETE_TRANSACTION_DICT = [
    "membership",
    "member",
    "coupon",
    "subscription",
    "id",
    "amount",
    "total",
    "tax_amount",
    "tax_rate",
    "tax_desc",
    "tax_class",
    "trans_num",
    "status",
    "txn_type",
    "gateway",
    "prorated",
    "created_at",
    "expires_at",
    "corporate_account_id",
    "parent_transaction_id",
    "tax_compound",
    "tax_shipping",
    "response",
]


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
