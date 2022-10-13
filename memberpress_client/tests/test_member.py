# bootstrap the test environment
from memberpress_client.settings.test import (
    MEMBERPRESS_API_KEY,
    MEMBERPRESS_API_KEY_NAME,
    MEMBERPRESS_API_BASE_URL,
    MEMBERPRESS_CACHE_EXPIRATION,
    MEMBERPRESS_SENSITIVE_KEYS,
)

from django.conf import settings

settings.configure(
    MEMBERPRESS_API_KEY=MEMBERPRESS_API_KEY,
    MEMBERPRESS_API_KEY_NAME=MEMBERPRESS_API_KEY_NAME,
    MEMBERPRESS_API_BASE_URL=MEMBERPRESS_API_BASE_URL,
    MEMBERPRESS_CACHE_EXPIRATION=MEMBERPRESS_CACHE_EXPIRATION,
    MEMBERPRESS_SENSITIVE_KEYS=MEMBERPRESS_SENSITIVE_KEYS,
)


# python stuff
import os  # noqa: E402
import io  # noqa: E402
import unittest  # noqa: E402
import json  # noqa: E402
from requests import request   # noqa: E402

# our stuff
from memberpress_client.member import Member  # noqa: E402


HERE = os.path.abspath(os.path.dirname(__file__))


def load_test_member():
    with io.open(os.path.join(HERE, "data", "mb-member.json"), "rt", encoding="utf8") as f:
        return f.read()


member_response = json.loads(load_test_member(), strict=False)


class TestMember(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_none_member_1(self):

        member = Member(request=None, response=None)  # noqa: F841

    def test_none_member_2(self):

        member = Member(request=None, response=None)
        # class properties
        self.assertEqual(member.request, None)
        self.assertEqual(member.is_offline, True)
        self.assertEqual(member.member, {})
        self.assertEqual(member.user, None)
        self.assertEqual(member.id, None)
        self.assertEqual(member.email, None)
        self.assertEqual(member.username, None)
        self.assertEqual(member.nicename, None)
        self.assertEqual(member.url, None)
        self.assertEqual(member.message, None)
        self.assertEqual(member.registered_at, None)
        self.assertEqual(member.first_name, None)
        self.assertEqual(member.last_name, None)
        self.assertEqual(member.display_name, None)
        self.assertEqual(member.active_txn_count, 0)
        self.assertEqual(member.expired_txn_count, 0)
        self.assertEqual(member.trial_txn_count, 0)
        self.assertEqual(member.login_count, 0)

        # dict structural integrity
        self.assertEqual(member.is_complete_member_dict, False)
        self.assertEqual(member.is_minimum_member_dict, False)
        self.assertEqual(member.is_validated_member, False)
        self.assertEqual(member.active_memberships, [])
        self.assertEqual(member.recent_subscriptions, [])
        self.assertEqual(member.recent_transactions, [])
        self.assertEqual(member.first_transaction, {})
        self.assertEqual(member.latest_transaction, {})
        self.assertEqual(member.address, {})
        self.assertEqual(member.profile, {})

        # advanced class properties - business rule support
        self.assertEqual(member.is_active_subscription, False)
        self.assertEqual(member.is_trial_subscription, False)


if __name__ == "__main__":
    unittest.main()
