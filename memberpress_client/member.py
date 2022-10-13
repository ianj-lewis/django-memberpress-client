# Python stuff
import validators
import logging
import inspect
import json
from datetime import datetime
import urllib3
from urllib.parse import urljoin
import requests

# Django stuff
from django.conf import settings
from django.core.cache import cache

# our stuff
from client import APIClientBaseClass
from utils import MPJSONEncoder, masked_dict, log_trace
from constants import MemberPressAPI_Endpoints, MemberPressAPI_Operations, COMPLETE_MEMBER_DICT, MINIMUM_MEMBER_DICT
from decorators import app_logger

logger = logging.getLogger(__name__)


class Member(APIClientBaseClass):
    """
    memberpress REST API client
    """

    _request = None

    _member = None
    _user = None
    _active_memberships = None
    _recent_subscriptions = None
    _recent_transactions = None

    def __init__(self, request) -> None:
        super().__init__()
        self._request = request

    @property
    def request(self):
        return self._request

    @property
    def member(self):
        if not self._member:
            self._member = self.get_member(username=self._user.username)
        return self._member

    @property
    def user(self):
        if not self._user:
            self._user = self.request.user

    @property
    def active_memberships(self):
        if not self._active_memberships:
            self._active_memberships = self.get_active_memberships(self.request)
        return self._active_memberships

    @property
    def recent_subscriptions(self):
        if not self._recent_subscriptions:
            self._recent_subscriptions = self.get_recent_subscriptions(self.request)
        return self._recent_subscriptions

    @property
    def recent_transactions(self):
        if not self._recent_transactions:
            self._recent_transactions = self.get_recent_transactions(request=self.request)
        return self._recent_transactions

    @property
    def id(self):
        try:
            return int(self.member.get("id", ""))
        except ValueError:
            return None

    @property
    def email(self):
        return self.member.get("email", "")

    @property
    def username(self):
        return self.member.get("username", "")

    @property
    def nicename(self):
        return self.member.get("nicename", "")

    @property
    def url(self):
        _url = self.member.get("url", "")
        return _url if validators.url(_url) else ""

    @property
    def message(self):
        return self.member.get("message", "")

    @property
    def registered_at(self):
        date_str = self.member.get("registered_at", "")
        try:
            return datetime.strptime(date_str, "%m/%d/%y %H:%M:%S")
        except Exception:
            return None

    @property
    def first_name(self):
        return self.member.get("first_name", "")

    @property
    def last_name(self):
        return self.member.get("last_name", "")

    @property
    def display_name(self):
        return self.member.get("display_name", "")

    def is_complete_member_dict(self, response: json) -> bool:
        """
        validate that response is a json dict containing at least
        the keys in qc_keys. These are the dict keys returned by the
        MemberPress REST api "/me" endpoint for a subscribed user.
        """
        qc_keys = COMPLETE_MEMBER_DICT
        return self.is_valid_dict(response, qc_keys)

    def is_minimum_member_dict(self, response: json) -> bool:
        """
        validate that response is a json dict containing at least
        the minimum required keys in qc_keys. These are the dict keys
        containing information about the identity of the member and
        the status of the member's subscription.
        """
        qc_keys = MINIMUM_MEMBER_DICT
        return self.is_valid_dict(response, qc_keys)

    @app_logger
    def get_member(self, username) -> requests.Response:
        """
        Return a Memberpress REST api json object describing the authenticated user.
        """
        cache_key = f"get_member:{username}"
        log_trace(caller=inspect.currentframe().f_code.co_name, path=cache_key, data={})
        response = cache.get(cache_key)
        if response is None:
            path = MemberPressAPI_Endpoints.MEMBERPRESS_API_ME_PATH
            response = self.get(path=path, operation=MemberPressAPI_Operations.GET_MEMBER)
            response = response or {}
        cache.set(cache_key, response, settings.MEMBERPRESS_CACHE_EXPIRATION)
        return response

    @app_logger
    def get_member_and_validate(self, request) -> bool:
        req_username = request.user.username
        if not req_username or req_username == "":
            logger.warning("received request with an invalid username {username}".format(username=req_username))
            return False

        member = self.get_member(req_username)
        if not self.is_minimum_member_dict(member):
            logger.warning(
                "get_member() returned an invalid json response {response}".format(
                    response=json.dumps(masked_dict(member), cls=MPJSONEncoder, indent=4)
                )
            )
            return False

        if not member:
            logger.warning("get_member() returned None for username {username}".format(username=req_username))
            return False

        res_username = member.get("username", "MISSING")
        if res_username != req_username:
            logger.warning(
                "internal error: requested username {req_username} but received {res_username}".format(
                    req_username=req_username, res_username=res_username
                )
            )
            return False

        return member

    @app_logger
    def get_active_memberships(self, request) -> list:
        member = self.get_member_and_validate(request=request)
        if not member:
            return []
        return member["active_memberships"]

    @app_logger
    def get_recent_subscriptions(self, request) -> list:
        member = self.get_member_and_validate(request=request)
        if not member:
            return []
        return member["recent_subscriptions"]

    @app_logger
    def get_recent_transactions(self, request) -> list:
        member = self.get_member_and_validate(request=request)
        if not member:
            return []
        return member["recent_transactions"]

    @app_logger
    def get_first_transaction(self, request) -> list:
        member = self.get_member_and_validate(request=request)
        if not member:
            return {}
        return member["first_txn"]

    @app_logger
    def get_latest_transaction(self, request) -> list:
        member = self.get_member_and_validate(request=request)
        if not member:
            return {}
        return member["latest_txn"]

    @app_logger
    def is_active_subscription(self, request) -> bool:
        member = self.get_member_and_validate(request=request)
        if not member:
            return False

        recent_subscriptions = self.get_recent_subscriptions(request=request)
        for subscription in recent_subscriptions:
            if subscription.get("status", "") == "active":
                return True

        return False

    @app_logger
    def is_trial_subscription(self, request) -> bool:
        member = self.get_member_and_validate(request=request)
        if not member:
            return False

        memberships = self.get_active_memberships(request=request)
        for membership in memberships:
            membership["date_gmt"] + membership["trial_days"]
            return True

        return False
