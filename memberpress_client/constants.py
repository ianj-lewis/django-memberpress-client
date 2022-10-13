from django.conf import settings

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
    MEMBERPRESS_API_BASE = settings.MEMBERPRESS_API_BASE_URL + "/wp-json/mp/v1/"
    MEMBERPRESS_API_ME_PATH = MEMBERPRESS_API_BASE + "me/"
