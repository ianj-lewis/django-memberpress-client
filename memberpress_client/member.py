# Python stuff
import validators
import logging
import json
from datetime import datetime
import requests

# Django stuff
from django.contrib.auth import get_user_model

# our stuff
from client import MemberpressAPIClient
from utils import MPJSONEncoder, masked_dict
from constants import MemberPressAPI_Endpoints, MemberPressAPI_Operations, COMPLETE_MEMBER_DICT, MINIMUM_MEMBER_DICT
from decorators import app_logger

logger = logging.getLogger(__name__)
User = get_user_model()


class Member(MemberpressAPIClient):
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
        self.request = request

    def init(self):
        self._request = None
        self._member = None
        self._user = None
        self._active_memberships = None
        self._recent_subscriptions = None
        self._recent_transactions = None

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        self.init()
        self._request = value

    @property
    def member(self) -> dict:
        if not self._member:
            self._member = self.get_member()
        return self._member

    @property
    def user(self) -> User:
        if not self._user:
            self._user = self.request.user

    @property
    def active_memberships(self) -> list:
        if not self._active_memberships:
            self._active_memberships = self.get_active_memberships(self.request)
        return self._active_memberships

    @property
    def recent_subscriptions(self) -> list:
        if not self._recent_subscriptions:
            self._recent_subscriptions = self.get_recent_subscriptions(self.request)
        return self._recent_subscriptions

    @property
    def recent_transactions(self) -> list:
        if not self._recent_transactions:
            self._recent_transactions = self.get_recent_transactions(request=self.request)
        return self._recent_transactions

    @property
    def id(self) -> int:
        try:
            return int(self.member.get("id", ""))
        except ValueError:
            return None

    @property
    def email(self) -> str:
        email_str = self.member.get("email", "")
        if validators.email(email_str):
            return email_str
        return None

    @property
    def username(self) -> str:
        return self.member.get("username", "")

    @property
    def nicename(self) -> str:
        return self.member.get("nicename", "")

    @property
    def url(self) -> str:
        _url = self.member.get("url", "")
        return _url if validators.url(_url) else ""

    @property
    def message(self) -> str:
        return self.member.get("message", "")

    @property
    def registered_at(self) -> datetime:
        date_str = self.member.get("registered_at", "")
        try:
            return datetime.strptime(date_str, "%m/%d/%y %H:%M:%S")
        except Exception:
            return None

    @property
    def first_name(self) -> str:
        return self.member.get("first_name", "")

    @property
    def last_name(self) -> str:
        return self.member.get("last_name", "")

    @property
    def display_name(self) -> str:
        return self.member.get("display_name", "")

    @property
    def is_complete_member_dict(self) -> bool:
        """
        validate that response is a json dict containing at least
        the keys in qc_keys. These are the dict keys returned by the
        MemberPress REST api "/me" endpoint for a subscribed user.
        """
        qc_keys = COMPLETE_MEMBER_DICT
        return self.is_valid_dict(self.member, qc_keys)

    @property
    def is_minimum_member_dict(self) -> bool:
        """
        validate that response is a json dict containing at least
        the minimum required keys in qc_keys. These are the dict keys
        containing information about the identity of the member and
        the status of the member's subscription.
        """
        qc_keys = MINIMUM_MEMBER_DICT
        return self.is_valid_dict(self.member, qc_keys)

    @app_logger
    def get_member(self) -> requests.Response:
        """
        Return a Memberpress REST api json object describing the authenticated user.
        Invoke the REST API only once for the lifecycle of this instance.
        """
        path = MemberPressAPI_Endpoints.MEMBERPRESS_API_ME_PATH
        return self.get(path=path, operation=MemberPressAPI_Operations.GET_MEMBER) or {}

    @property
    def is_validated_member(self) -> bool:
        if not self.is_minimum_member_dict:
            logger.warning(
                "get_member() returned an invalid json response {response}".format(
                    response=json.dumps(masked_dict(self.member), cls=MPJSONEncoder, indent=4)
                )
            )
            return False

        if not self.member:
            logger.warning("member property is not set for username {username}".format(username=self.user.username))
            return False

        if self.username != self.request.user.username:
            logger.warning(
                "internal error: requested username {req_username} but received {res_username}".format(
                    req_username=self.request.user.username, res_username=self.username
                )
            )
            return False

        return True

    def get_active_memberships(self, request) -> list:
        return self.member["active_memberships"] if self.is_validated_member else []

    def get_recent_subscriptions(self, request) -> list:
        return self.member["recent_subscriptions"] if self.is_validated_member else []

    def get_recent_transactions(self, request) -> list:
        return self.member["recent_transactions"] if self.is_validated_member else []

    def get_first_transaction(self, request) -> list:
        return self.member["first_txn"] if self.is_validated_member else {}

    def get_latest_transaction(self, request) -> list:
        return self.member["latest_txn"] if self.is_validated_member else {}

    @app_logger
    def is_active_subscription(self, request) -> bool:
        member = self.is_validated_member(request=request)
        if not member:
            return False

        recent_subscriptions = self.get_recent_subscriptions(request=request)
        for subscription in recent_subscriptions:
            if subscription.get("status", "") == "active":
                return True

        return False

    @app_logger
    def is_trial_subscription(self, request) -> bool:
        member = self.is_validated_member(request=request)
        if not member:
            return False

        memberships = self.get_active_memberships(request=request)
        for membership in memberships:
            membership["date_gmt"] + membership["trial_days"]
            return True

        return False
