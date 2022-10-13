"""
Common Pluggable Django App settings
"""


def plugin_settings(settings):
    """
    Injects local settings into django settings
    """

    # MemberPress REST API client
    # -------------------------------------------------------------------------
    MEMBERPRESS_API_KEY = "set-me-please"                           # noqa: F841
    MEMBERPRESS_API_BASE_URL = "https://set-me-please.com/"         # noqa: F841
    MEMBERPRESS_CACHE_EXPIRATION = 300                              # noqa: F841
    MEMBERPRESS_SENSITIVE_KEYS = ["password", "token", "client_id", "client_secret", "Authorization", "secret"]  # noqa: F841
