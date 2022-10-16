"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - plugin constants
"""

# django stuff
from django.conf import settings

MEMBERPRESS_EVENTS = (
    ("after-cc-expires-reminder", "after-cc-expires-reminder"),
    ("after-member-signup-reminder", "after-member-signup-reminder"),
    ("after-signup-abandoned-reminder", "after-signup-abandoned-reminder"),
    ("after-sub-expires-reminder", "after-sub-expires-reminder"),
    ("before-cc-expires-reminder", "before-cc-expires-reminder"),
    ("before-sub-expires-reminder", "before-sub-expires-reminder"),
    ("before-sub-renews-reminder", "before-sub-renews-reminder"),
    ("before-sub-trial-ends", "before-sub-trial-ends"),
    ("login", "login"),
    ("member-account-updated", "member-account-updated"),
    ("member-added", "member-added"),
    ("member-deleted", "member-deleted"),
    ("member-signup-completed", "member-signup-completed"),
    ("mpca-course-completed", "mpca-course-completed"),
    ("mpca-course-started", "mpca-course-started"),
    ("mpca-lesson-completed", "mpca-lesson-completed"),
    ("mpca-lesson-started", "mpca-lesson-started"),
    ("mpca-quiz-attempt-completed", "mpca-quiz-attempt-completed"),
    ("non-recurring-transaction-completed", "non-recurring-transaction-completed"),
    ("non-recurring-transaction-expired", "non-recurring-transaction-expired"),
    ("offline-payment-complete", "offline-payment-complete"),
    ("offline-payment-pending", "offline-payment-pending"),
    ("offline-payment-refunded", "offline-payment-refunded"),
    ("recurring-transaction-completed", "recurring-transaction-completed"),
    ("recurring-transaction-expired", "recurring-transaction-expired"),
    ("recurring-transaction-failed", "recurring-transaction-failed"),
    ("renewal-transaction-completed", "renewal-transaction-completed"),
    ("sub-account-added", "sub-account-added"),
    ("sub-account-removed", "sub-account-removed"),
    ("subscription-created", "subscription-created"),
    ("subscription-downgraded-to-one-time", "subscription-downgraded-to-one-time"),
    ("subscription-downgraded-to-recurring", "subscription-downgraded-to-recurring"),
    ("subscription-downgraded", "subscription-downgraded"),
    ("subscription-expired", "subscription-expired"),
    ("subscription-paused", "subscription-paused"),
    ("subscription-resumed", "subscription-resumed"),
    ("subscription-stopped", "subscription-stopped"),
    ("subscription-upgraded-to-one-time", "subscription-upgraded-to-one-time"),
    ("subscription-upgraded-to-recurring", "subscription-upgraded-to-recurring"),
    ("subscription-upgraded", "subscription-upgraded"),
    ("transaction-completed", "transaction-completed"),
    ("transaction-expired", "transaction-expired"),
    ("transaction-failed", "transaction-failed"),
    ("transaction-refunded", "transaction-refunded"),
    ("unidentified-event", "unidentified-event"),
)


MEMBERPRESS_OPERATION_PREFIX = "memberpress_api_operation_"
OPERATION_GET_MEMBER = MEMBERPRESS_OPERATION_PREFIX + "get_member"


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
    MEMBERPRESS_API_BASE = settings.MEMBERPRESS_API_BASE_URL + "wp-json/mp/v1/"
    MEMBERPRESS_API_ME_PATH = MEMBERPRESS_API_BASE + "me/"

    # -------------------------------------------------------------------------
    # curl "https://set-me-please.com/wp-json/mp/v1/members?search=mcdaniel" -H "MEMBERPRESS-API-KEY: set-me-please"
    # -------------------------------------------------------------------------
    def MEMBERPRESS_API_MEMBER_PATH(username):
        return MemberPressAPI_Endpoints.MEMBERPRESS_API_BASE + "members?search=" + username


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

COMPLETE_MEMBERSHIP_DICT = [
    "id",
    "title",
    "content",
    "excerpt",
    "date",
    "status",
    "author",
    "date_gmt",
    "modified",
    "modified_gmt",
    "group",
    "price",
    "period",
    "period_type",
    "signup_button_text",
    "limit_cycles",
    "limit_cycles_num",
    "limit_cycles_action",
    "limit_cycles_expires_after",
    "limit_cycles_expires_type",
    "trial",
    "trial_days",
    "trial_amount",
    "trial_once",
    "group_order",
    "is_highlighted",
    "plan_code",
    "pricing_title",
    "pricing_show_price",
    "pricing_display",
    "custom_price",
    "pricing_heading_txt",
    "pricing_footer_txt",
    "pricing_button_txt",
    "pricing_button_position",
    "pricing_benefits",
    "register_price_action",
    "register_price",
    "thank_you_page_enabled",
    "thank_you_page_type",
    "thank_you_message",
    "thank_you_page_id",
    "custom_login_urls_enabled",
    "custom_login_urls_default",
    "custom_login_urls",
    "expire_type",
    "expire_after",
    "expire_unit",
    "expire_fixed",
    "tax_exempt",
    "tax_class",
    "allow_renewal",
    "access_url",
    "disable_address_fields",
    "simultaneous_subscriptions",
    "use_custom_template",
    "custom_template",
    "customize_payment_methods",
    "custom_payment_methods",
    "customize_profile_fields",
    "custom_profile_fields",
    "cannot_purchase_message",
]
