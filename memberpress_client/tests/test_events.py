# python stuff
from email.policy import strict
import os
import io
import unittest
import json
from datetime import datetime
from requests import request


# our testing code starts here
# -----------------------------------------------------------------------------
from memberpress_client.member import Member  # noqa: E402
from memberpress_client.constants import MemberpressEvents
from memberpress_client.event import get_event

# setup test data
HERE = os.path.abspath(os.path.dirname(__file__))


def load_json_file(test_file):
    test_file = test_file + ".json"
    with io.open(os.path.join(HERE, "data", test_file), "rt", encoding="utf8") as f:
        return json.loads(f.read(), strict=False)


# test data
# -----------------------------------------------------------------------------


class TestMember(unittest.TestCase):

    PATH = "./data/events/"

    def test_1_valid_dicts(self):
        def validate(data_dict: dict):
            event = get_event(data_dict)
            self.assertEqual(event.is_valid, True)

        validate(load_json_file(self.PATH + MemberpressEvents.AFTER_CC_EXPIRES_REMINDER))
        validate(load_json_file(self.PATH + MemberpressEvents.AFTER_CC_EXPIRES_REMINDER))
        validate(load_json_file(self.PATH + MemberpressEvents.AFTER_MEMBER_SIGNUP_REMINDER))
        validate(load_json_file(self.PATH + MemberpressEvents.AFTER_SIGNUP_ABANDONED_REMINDER))
        validate(load_json_file(self.PATH + MemberpressEvents.AFTER_SUB_EXPIRES_REMINDER))
        validate(load_json_file(self.PATH + MemberpressEvents.BEFORE_CC_EXPIRES_REMINDER))
        validate(load_json_file(self.PATH + MemberpressEvents.BEFORE_SUB_EXPIRES_REMINDER))
        validate(load_json_file(self.PATH + MemberpressEvents.BEFORE_SUB_RENEWS_REMINDER))
        validate(load_json_file(self.PATH + MemberpressEvents.BEFORE_SUB_TRIAL_ENDS))
        validate(load_json_file(self.PATH + MemberpressEvents.LOGIN))
        validate(load_json_file(self.PATH + MemberpressEvents.MEMBER_ACCOUNT_UPDATED))
        validate(load_json_file(self.PATH + MemberpressEvents.MEMBER_ADDED))
        validate(load_json_file(self.PATH + MemberpressEvents.MEMBER_DELETED))
        validate(load_json_file(self.PATH + MemberpressEvents.MEMBER_SIGNUP_COMPLETED))
        validate(load_json_file(self.PATH + MemberpressEvents.MPCA_COURSE_COMPLETED))
        validate(load_json_file(self.PATH + MemberpressEvents.MPCA_COURSE_STARTED))
        validate(load_json_file(self.PATH + MemberpressEvents.MPCA_LESSON_COMPLETED))
        validate(load_json_file(self.PATH + MemberpressEvents.MPCA_LESSON_STARTED))
        validate(load_json_file(self.PATH + MemberpressEvents.MPCA_QUIZ_ATTEMPT_COMPLETED))
        validate(load_json_file(self.PATH + MemberpressEvents.NON_RECURRING_TRANSACTION_COMPLETED))
        validate(load_json_file(self.PATH + MemberpressEvents.NON_RECURRING_TRANSACTION_EXPIRED))
        validate(load_json_file(self.PATH + MemberpressEvents.OFFLINE_PAYMENT_COMPLETE))
        validate(load_json_file(self.PATH + MemberpressEvents.OFFLINE_PAYMENT_PENDING))
        validate(load_json_file(self.PATH + MemberpressEvents.OFFLINE_PAYMENT_REFUNDED))
        validate(load_json_file(self.PATH + MemberpressEvents.RECURRING_TRANSACTION_COMPLETED))
        validate(load_json_file(self.PATH + MemberpressEvents.RECURRING_TRANSACTION_EXPIRED))
        validate(load_json_file(self.PATH + MemberpressEvents.RECURRING_TRANSACTION_FAILED))
        validate(load_json_file(self.PATH + MemberpressEvents.RENEWAL_TRANSACTION_COMPLETED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUB_ACCOUNT_ADDED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUB_ACCOUNT_REMOVED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_CREATED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_RECURRING))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_DOWNGRADED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_EXPIRED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_PAUSED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_RESUMED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_STOPPED))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_ONE_TIME))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_RECURRING))
        validate(load_json_file(self.PATH + MemberpressEvents.SUBSCRIPTION_UPGRADED))
        validate(load_json_file(self.PATH + MemberpressEvents.TRANSACTION_COMPLETED))
        validate(load_json_file(self.PATH + MemberpressEvents.TRANSACTION_EXPIRED))
        validate(load_json_file(self.PATH + MemberpressEvents.TRANSACTION_FAILED))
        validate(load_json_file(self.PATH + MemberpressEvents.TRANSACTION_REFUNDED))
        validate(load_json_file(self.PATH + MemberpressEvents.UNIDENTIFIED_EVENT))
