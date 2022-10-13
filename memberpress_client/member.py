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
    _is_validated_member = False

    def __init__(self, request) -> None:
        super().__init__()
        self.request = request

    def init(self):
        self._request = None
        self._member = None
        self._user = None
        self._is_validated_member = False

    def validate_response_object(self) -> None:
        if not self.member:
            logger.error("member property is not set for username {username}".format(username=self.user.username))
            self._is_validated_member = False

        if type(self.member) != dict:
            logger.error(
                "was expecting member object of type dict but received an object of type {t}".format(
                    t=type(self.member)
                )
            )
            self._is_validated_member = False

        if self.username != self.request.user.username:
            logger.error(
                "internal error: openedx username {req_username} does not match the username returned by memberpress REST api member response object: {res_username}".format(
                    req_username=self.request.user.username, res_username=self.username
                )
            )
            self._is_validated_member = False
        self._is_validated_member = True

    def validate_dict_keys(self) -> None:
        def list_diff(self, list_1: list, list_2: list) -> list:
            diff = list(set(list_2) - set(list_1))
            return ",".join(diff)

        if self.is_complete_member_dict:
            logger.info("validated member response object for username {username}.".format(username=self.user.username))
            return

        if not self.is_minimum_member_dict:
            missing = list_diff(MINIMUM_MEMBER_DICT, self.member.keys())
            logger.warning(
                "member response object for username {username} is missing the following required keys: {missing}".format(
                    username=self.user.username, missing=missing
                )
            )

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        if type(value) == requests.request:
            self.init()
            self._request = value
            if self.validate_response_object():
                self.validate_dict_keys()
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
            logger.warning("Cannot read id for username {username}".format(username=self.username))
            return None

    @property
    def email(self) -> str:
        email_str = self.member.get("email", "")
        if validators.email(email_str):
            return email_str
        logger.warning("invalid email address for username {username}".format(username=self.username))
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
        return _url if validators.url(_url) else None

    @property
    def message(self) -> str:
        return self.member.get("message", "")

    @property
    def registered_at(self) -> datetime:
        date_str = self.member.get("registered_at", "")
        try:
            return datetime.strptime(date_str, "%m/%d/%y %H:%M:%S")
        except Exception:
            logger.warning("Cannot read registered_at for username {username}".format(username=self.username))
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
        """
        the number of historical financial transactions (ie Stripe, PayPal, etc.)
        that exist for this member.
        """
        try:
            return int(self.member.get("active_txn_count", ""))
        except Exception:
            logger.warning("Cannot read active_txn_count for username {username}".format(username=self.username))
            return 0

    @property
    def expired_txn_count(self) -> int:
        """
        the number of historical financial transactions (ie Stripe, PayPal, etc.)
        that exist for this member with an expiration date in the past.
        """
        try:
            return int(self.member.get("expired_txn_count", ""))
        except Exception:
            logger.warning("Cannot read expired_txn_count for username {username}".format(username=self.username))
            return 0

    @property
    def trial_txn_count(self) -> int:
        """
        the number of free trials that exist for this member.
        """
        try:
            return int(self.member.get("trial_txn_count", ""))
        except Exception:
            logger.warning("Cannot read trial_txn_count for username {username}".format(username=self.username))
            return 0

    @property
    def login_count(self) -> int:
        """
        the number of times that this member has logged in to the
        Wordpress site hosting the memberpress REST API plugin.
        """
        try:
            return int(self.member.get("login_count", ""))
        except Exception:
            logger.warning("Cannot read login_count for username {username}".format(username=self.username))
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
        return self._is_validated_member

    @property
    def active_memberships(self) -> list:
        return self.member.get("active_memberships", []) if self.is_validated_member else []

    @property
    def recent_subscriptions(self) -> list:
        return self.member.get("recent_subscriptions", []) if self.is_validated_member else []

    @property
    def recent_transactions(self) -> list:
        return self.member.get("recent_transactions", []) if self.is_validated_member else []

    @property
    def first_transaction(self) -> list:
        return self.member.get("first_txn", {}) if self.is_validated_member else {}

    @property
    def glatest_transaction(self) -> list:
        return self.member.get("latest_txn", {}) if self.is_validated_member else {}

    @property
    def first_txn(self) -> dict:
        return self.member.get("first_txn", {}) if self.is_validated_member else {}

    @property
    def latest_txn(self) -> dict:
        return self.member.get("latest_txn", {}) if self.is_validated_member else {}

    @property
    def address(self) -> dict:
        return self.member.get("address", {}) if self.is_validated_member else {}

    @property
    def profile(self) -> dict:
        return self.member.get("profile", {}) if self.is_validated_member else {}

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
