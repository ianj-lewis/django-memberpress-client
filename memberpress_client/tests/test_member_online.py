# python stuff
import os
import io
import unittest
import json
from datetime import datetime
from requests import request

# our testing code starts here
# -----------------------------------------------------------------------------
from memberpress_client.member import Member  # noqa: E402
from memberpress_client.transaction import Transaction  # noqa: E402
from memberpress_client.subscription import Subscription  # noqa: E402
from memberpress_client.membership import Membership  # noqa: E402

# setup test data
HERE = os.path.abspath(os.path.dirname(__file__))


def load_test_member(test_file):
    with io.open(os.path.join(HERE, "data", test_file), "rt", encoding="utf8") as f:
        return f.read()


# test data
# -----------------------------------------------------------------------------
valid_member_response = json.loads(load_test_member("valid-member.json"), strict=False)
invalid_member_missing_subscriptions = json.loads(
    load_test_member("invalid-member-missing-subscriptions.json"), strict=False
)
invalid_member_no_trx = json.loads(load_test_member("invalid-member-no-trx.json"), strict=False)


class TestMember(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_online_1(self):

        member = Member(username="jon")
        registered_at = datetime.strptime("2022-10-07 22:21:58", "%Y-%m-%d %H:%M:%S")

        # class properties
        self.assertEqual(member.request, None)
        self.assertEqual(member.is_offline, True)
        self.assertEqual(type(member.member), dict)
        self.assertEqual(member.id, 10)
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
        self.assertEqual(member.is_trial_subscription, False)


if __name__ == "__main__":
    unittest.main()
