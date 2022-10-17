# python stuff
import os
import io
import unittest
import json
from datetime import datetime

# our testing code starts here
# -----------------------------------------------------------------------------
from memberpress_client.constants import MemberpressEvents
from memberpress_client.events import get_event, MEMBERPRESS_EVENT_CLASSES

# setup test data
HERE = os.path.abspath(os.path.dirname(__file__))


def load_json(test_file):
    test_file = test_file + ".json"
    with io.open(os.path.join(HERE, "data", "events", test_file), "rt", encoding="utf8") as f:
        return json.loads(f.read(), strict=False)


class TestMember(unittest.TestCase):
    def test_1_valid_dicts(self):
        def validate(event_str: str):
            # load a json dict from a test file
            data_dict = load_json(event_str)

            # instantiate the object
            event = get_event(data_dict)

            # tests
            self.assertEqual(event.is_valid, True)
            self.assertEqual(event.event, event_str)
            self.assertEqual(type(event), MEMBERPRESS_EVENT_CLASSES[event_str])

        validate(MemberpressEvents.AFTER_CC_EXPIRES_REMINDER)
        validate(MemberpressEvents.AFTER_CC_EXPIRES_REMINDER)
        validate(MemberpressEvents.AFTER_MEMBER_SIGNUP_REMINDER)
        validate(MemberpressEvents.AFTER_SIGNUP_ABANDONED_REMINDER)
        validate(MemberpressEvents.AFTER_SUB_EXPIRES_REMINDER)
        validate(MemberpressEvents.BEFORE_CC_EXPIRES_REMINDER)
        validate(MemberpressEvents.BEFORE_SUB_EXPIRES_REMINDER)
        validate(MemberpressEvents.BEFORE_SUB_RENEWS_REMINDER)
        validate(MemberpressEvents.BEFORE_SUB_TRIAL_ENDS)
        validate(MemberpressEvents.LOGIN)
        validate(MemberpressEvents.MEMBER_ACCOUNT_UPDATED)
        validate(MemberpressEvents.MEMBER_ADDED)
        validate(MemberpressEvents.MEMBER_DELETED)
        validate(MemberpressEvents.MEMBER_SIGNUP_COMPLETED)
        validate(MemberpressEvents.MPCA_COURSE_COMPLETED)
        validate(MemberpressEvents.MPCA_COURSE_STARTED)
        validate(MemberpressEvents.MPCA_LESSON_COMPLETED)
        validate(MemberpressEvents.MPCA_LESSON_STARTED)
        validate(MemberpressEvents.MPCA_QUIZ_ATTEMPT_COMPLETED)
        validate(MemberpressEvents.NON_RECURRING_TRANSACTION_COMPLETED)
        validate(MemberpressEvents.NON_RECURRING_TRANSACTION_EXPIRED)
        validate(MemberpressEvents.OFFLINE_PAYMENT_COMPLETE)
        validate(MemberpressEvents.OFFLINE_PAYMENT_PENDING)
        validate(MemberpressEvents.OFFLINE_PAYMENT_REFUNDED)
        validate(MemberpressEvents.RECURRING_TRANSACTION_COMPLETED)
        validate(MemberpressEvents.RECURRING_TRANSACTION_EXPIRED)
        validate(MemberpressEvents.RECURRING_TRANSACTION_FAILED)
        validate(MemberpressEvents.RENEWAL_TRANSACTION_COMPLETED)
        validate(MemberpressEvents.SUB_ACCOUNT_ADDED)
        validate(MemberpressEvents.SUB_ACCOUNT_REMOVED)
        validate(MemberpressEvents.SUBSCRIPTION_CREATED)
        validate(MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME)
        validate(MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_RECURRING)
        validate(MemberpressEvents.SUBSCRIPTION_DOWNGRADED)
        validate(MemberpressEvents.SUBSCRIPTION_EXPIRED)
        validate(MemberpressEvents.SUBSCRIPTION_PAUSED)
        validate(MemberpressEvents.SUBSCRIPTION_RESUMED)
        validate(MemberpressEvents.SUBSCRIPTION_STOPPED)
        validate(MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_ONE_TIME)
        validate(MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_RECURRING)
        validate(MemberpressEvents.SUBSCRIPTION_UPGRADED)
        validate(MemberpressEvents.TRANSACTION_COMPLETED)
        validate(MemberpressEvents.TRANSACTION_EXPIRED)
        validate(MemberpressEvents.TRANSACTION_FAILED)
        validate(MemberpressEvents.TRANSACTION_REFUNDED)

    def test_2_valid_login_event(self):
        event_str = MemberpressEvents.LOGIN
        data_dict = load_json(event_str)
        event = get_event(data_dict)

        # tests
        self.assertEqual(event.is_valid, True)
        self.assertEqual(event.event, event_str)
        self.assertEqual(type(event), MEMBERPRESS_EVENT_CLASSES[event_str])

        self.assertEqual(event.id, 6)
        self.assertEqual(event.email, "lpm0073@gmail.com")
        self.assertEqual(event.username, "mcdaniel")
        self.assertEqual(event.nicename, "mcdaniel")
        self.assertEqual(event.url, "https://lawrencemcdaniel.com")
        self.assertEqual(event.message, "")
        self.assertEqual(event.registered_at, datetime.strptime("2022-10-04 00:46:37", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(event.first_name, "Lawrence")
        self.assertEqual(event.last_name, "McDaniel")
        self.assertEqual(event.active_memberships, [])
        self.assertEqual(event.active_txn_count, 0)
        self.assertEqual(event.expired_txn_count, 0)
        self.assertEqual(event.trial_txn_count, 0)
        self.assertEqual(event.sub_count, None)
        self.assertEqual(event.login_count, 25)
        self.assertEqual(type(event.address), dict)
        self.assertEqual(len(event.address.keys()), 6)
        self.assertEqual(type(event.profile), dict)
        self.assertEqual(event.profile, {})
        self.assertEqual(event.recent_transactions, [])
        self.assertEqual(event.recent_subscriptions, [])
