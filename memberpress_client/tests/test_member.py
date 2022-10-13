# python stuff
import os
import io
import unittest
import json
from datetime import datetime
from requests import request

# bootstrap the test environment
from memberpress_client.settings import test as test_settings
from django.conf import settings

settings.configure(default_settings=test_settings)

# our testing code starts here
# -----------------------------------------------------------------------------
from memberpress_client.member import Member  # noqa: E402
from memberpress_client.transaction import Transaction  # noqa: E402


# setup test data
HERE = os.path.abspath(os.path.dirname(__file__))


def load_test_member(test_file):
    with io.open(os.path.join(HERE, "data", test_file), "rt", encoding="utf8") as f:
        return f.read()


valid_member_response = json.loads(load_test_member("valid-member.json"), strict=False)


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
        self.assertEqual(member.is_complete_dict, False)
        self.assertEqual(member.is_minimum_member_dict, False)
        self.assertEqual(member.is_validated_member, False)
        self.assertEqual(member.active_memberships, None)
        self.assertEqual(member.recent_subscriptions, None)
        self.assertEqual(member.recent_transactions, None)
        self.assertEqual(member.first_transaction, None)
        self.assertEqual(member.latest_transaction, None)
        self.assertEqual(member.address, {})
        self.assertEqual(member.profile, {})

        # advanced class properties - business rule support
        self.assertEqual(member.is_active_subscription, False)
        self.assertEqual(member.is_trial_subscription, False)

    def test_member_1(self):

        member = Member(request=None, response=valid_member_response)
        registered_at = datetime.strptime("2022-10-07 22:21:58", "%Y-%m-%d %H:%M:%S")

        # class properties
        self.assertEqual(member.request, None)
        self.assertEqual(member.is_offline, True)
        self.assertEqual(type(member.member), dict)
        self.assertEqual(member.id, 8)
        self.assertEqual(member.email, "jon.spurling@crstrategypartners.com")
        self.assertEqual(member.username, "JonSpurling81")
        self.assertEqual(member.nicename, "jonspurling81")
        self.assertEqual(member.url, None)
        self.assertEqual(member.message, "")
        self.assertEqual(member.registered_at, registered_at)
        self.assertEqual(member.first_name, "Jon")
        self.assertEqual(member.last_name, "Spurling")
        self.assertEqual(member.display_name, "Jon Spurling")
        self.assertEqual(member.active_txn_count, 1)
        self.assertEqual(member.expired_txn_count, 0)
        self.assertEqual(member.trial_txn_count, 1)
        self.assertEqual(member.login_count, 1)

        # dict structural integrity
        self.assertEqual(member.is_complete_dict, True)
        self.assertEqual(member.is_minimum_member_dict, True)
        self.assertEqual(member.is_validated_member, True)

        self.assertEqual(type(member.active_memberships), list)
        self.assertEqual(type(member.recent_subscriptions), list)
        self.assertEqual(type(member.recent_transactions), list)
        self.assertEqual(type(member.first_transaction), Transaction)
        self.assertEqual(type(member.latest_transaction), Transaction)

        self.assertEqual(len(member.active_memberships), 1)
        self.assertEqual(len(member.recent_subscriptions), 1)
        self.assertEqual(len(member.recent_transactions), 1)

        # advanced class properties - business rule support
        self.assertEqual(member.is_active_subscription, True)
        self.assertEqual(member.is_trial_subscription, True)


if __name__ == "__main__":
    unittest.main()
