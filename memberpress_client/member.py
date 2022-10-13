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

    def __init__(self, request) -> None:
        super().__init__()
        self.request = request

    def init(self):
        self._request = None
        self._member = None
        self._user = None

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        if type(value) == requests.request:
            self.init()
            self._request = value
        else:
            raise TypeError("Was expecting value of type request but received object of type {t}".format(t=type(value)))

    @property
    def member(self) -> dict:
        if not self._member:
            path = MemberPressAPI_Endpoints.MEMBERPRESS_API_ME_PATH
            self._member = self.get(path=path, operation=MemberPressAPI_Operations.GET_MEMBER) or {}
        return self._member

    @property
    def user(self) -> User:
        if not self._user:
            self._user = self.request.user
        return self._user

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
    def active_txn_count(self) -> int:
        try:
            return int(self.member.get("active_txn_count", ""))
        except Exception:
            return 0

    @property
    def expired_txn_count(self) -> int:
        try:
            return int(self.member.get("expired_txn_count", ""))
        except Exception:
            return 0

    @property
    def trial_txn_count(self) -> int:
        try:
            return int(self.member.get("trial_txn_count", ""))
        except Exception:
            return 0

    @property
    def login_count(self) -> int:
        try:
            return int(self.member.get("login_count", ""))
        except Exception:
            return 0

    """
    ---------------------------------------------------------------------------
                                Computed properties
    ---------------------------------------------------------------------------
    """

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

    @property
    def active_memberships(self) -> list:
        return self.member["active_memberships"] if self.is_validated_member else []

    @property
    def recent_subscriptions(self) -> list:
        return self.member["recent_subscriptions"] if self.is_validated_member else []

    @property
    def recent_transactions(self) -> list:
        return self.member["recent_transactions"] if self.is_validated_member else []

    @property
    def first_transaction(self) -> list:
        return self.member["first_txn"] if self.is_validated_member else {}

    @property
    def glatest_transaction(self) -> list:
        return self.member["latest_txn"] if self.is_validated_member else {}

    @property
    def first_txn(self) -> dict:
        return self.member["first_txn"] if self.is_validated_member else {}

    @property
    def latest_txn(self) -> dict:
        return self.member["latest_txn"] if self.is_validated_member else {}

    @property
    def address(self) -> dict:
        return self.member["address"] if self.is_validated_member else {}

    @property
    def profile(self) -> dict:
        return self.member["profile"] if self.is_validated_member else {}

    @property
    def is_active_subscription(self) -> bool:
        if not self.is_validated_member:
            return False

        for subscription in self.recent_subscriptions:
            if subscription.get("status", "") == "active":
                return True

        return False

    @property
    def is_trial_subscription(self) -> bool:
        if not self.is_validated_member:
            return False

        for membership in self.active_memberships:
            # FIX NOTE: I DON'T WORK YET.
            membership["date_gmt"] + membership["trial_days"]
            return True

        return False
