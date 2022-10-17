import logging

from memberpress_client.constants import (
    COMPLETE_TRANSACTION_DICT,
    COMPLETE_MEMBER_DICT,
    MemberpressEvents,
    MemberpressEventsTypes,
)
from memberpress_client.member import Member
from memberpress_client.membership import Membership
from memberpress_client.transaction import Transaction
from memberpress_client.subscription import Subscription

logger = logging.getLogger(__name__)


class MemberpressEvent:
    """
    Event base class
    """

    _json = None
    _event = None
    _event_type = None
    _data = None
    _member = None
    _membership = None
    _transaction = None
    _subscription = None
    _is_valid = False

    qc_keys = []
    has_member = False
    has_membership = False
    has_transaction = False
    has_subscription = False

    def __init__(self, data: dict) -> None:
        self.init()
        self.json = data
        pass

    def init(self):
        self._json = None
        self._event = None
        self._event_type = None
        self._data = None
        self._member = None
        self._membership = None
        self._transaction = None
        self._subscription = None

    def validate(self):
        if self.event != self.json.get("event", "missing event"):
            self._is_valid = False
            logger.warning("received a dict with no 'event' key.")
            return

        if self.event_type != self.json.get("type", "missing event type"):
            self._is_valid = False
            logger.warning("received a dict with no 'type' key.")
            return

        base_keys = ["event", "type", "data"]
        if not self.is_valid_dict(self.json, qc_keys=base_keys):
            self._is_valid = False
            logger.warning("received a dict with no 'data' key.")
            return

        if not self.is_valid_dict(self.json, qc_keys=self.qc_keys):
            self._is_valid = False
            return

        self.has_member = MemberpressEventsTypes.MEMBER in self.qc_keys
        self.has_membership = MemberpressEventsTypes.MEMBERSHIP in self.qc_keys
        self.has_transaction = MemberpressEventsTypes.TRANSACTION in self.qc_keys
        self.has_subscription = MemberpressEventsTypes.SUBSCRIPTION in self.qc_keys

    def is_valid_dict(self, response, qc_keys) -> bool:
        if not type(response) == dict:
            logger.warning(
                "is_valid_dict() was expecting a dict but received an object of type: {type}".format(
                    type=type(response)
                )
            )
            return False
        return all(key in response for key in qc_keys)

    @property
    def json(self):
        return self._json or {}

    @json.setter
    def json(self, value):
        if type(value) == dict or value is None:
            self.init()
            self._json = value
        else:
            logger.warning("was expecting a value of type dict but receive type {t}".format(t=type(value)))

    @property
    def is_valid(self):
        return self._is_valid

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        if type(value) == str or value is None:
            self._event = value
        else:
            logger.warning("was expecting a value of type str but received type {t}".format(t=type(value)))

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        if type(value) == str or value is None:
            self._event_type = value
        else:
            logger.warning("was expecting a value of type str but received type {t}".format(t=type(value)))

    @property
    def data(self):
        return self.json.get("data", {})

    @property
    def membership(self):
        if self.has_membership and not self._membership:
            membership_dict = self.data.get(MemberpressEventsTypes.MEMBERSHIP, {})
            self._membership = Membership(membership=membership_dict)
        return self._membership

    @property
    def member(self):
        if self.has_member and not self._member:
            if self.event_type == MemberpressEventsTypes.MEMBER:
                member_dict = (
                    self.data
                    if self.event_type == MemberpressEventsTypes.MEMBER
                    else self.data.get(MemberpressEventsTypes.MEMBER, {})
                )
            self._member = Member(response=member_dict)
        return self._member

    @property
    def transaction(self):
        if self.has_transaction and not self._transaction:
            transaction_dict = self.data
            self._transaction = Transaction(transaction=transaction_dict)
        return self._transaction

    @property
    def subscription(self):
        if self.has_subscription and not self._subscription:
            subscription_dict = self.data.get(MemberpressEventsTypes.SUBSCRIPTION, {})
            self._subscription = Subscription(subscription=subscription_dict)
        return self._subscription


class MEAfterCCExpiresReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.AFTER_CC_EXPIRES_REMINDER
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEAfterMemberSignupReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.AFTER_MEMBER_SIGNUP_REMINDER
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEAfterSignupAbandonedReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.AFTER_SIGNUP_ABANDONED_REMINDER
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEAfterSubExpiresReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.AFTER_SUB_EXPIRES_REMINDER
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEBeforeCCExpiresReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.BEFORE_CC_EXPIRES_REMINDER
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEBeforeSubExpiresReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.BEFORE_SUB_EXPIRES_REMINDER
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEBeforeSubRenewsReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.BEFORE_SUB_RENEWS_REMINDER
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEBeforeSubTrialEnds(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.BEFORE_SUB_TRIAL_ENDS
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MELogin(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.LOGIN
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMemberAccountUpdated(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MEMBER_ACCOUNT_UPDATED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMemberAdded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MEMBER_ADDED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMemberDeleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MEMBER_DELETED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMemberSignupCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MEMBER_SIGNUP_COMPLETED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMPCACourseCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_COURSE_COMPLETED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMPCACourseStarted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_COURSE_STARTED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMPCALessonCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_LESSON_COMPLETED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMPCALessonStarted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_LESSON_STARTED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MEMPCALQuizAttemptCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_QUIZ_ATTEMPT_COMPLETED
        self.event_type = MemberpressEventsTypes.MEMBER
        self.qc_keys = [] + COMPLETE_MEMBER_DICT
        self.validate()


class MENonRecurringTransactionCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.NON_RECURRING_TRANSACTION_COMPLETED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MENonRecurringTransactionExpired(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.NON_RECURRING_TRANSACTION_EXPIRED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEOfflinePaymentComplete(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.OFFLINE_PAYMENT_COMPLETE
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEOfflinePaymentPending(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.OFFLINE_PAYMENT_PENDING
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEOfflinePaymentRefunded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.OFFLINE_PAYMENT_REFUNDED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MERecurringTransactionCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.RECURRING_TRANSACTION_COMPLETED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MERecurringTransactionExpired(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.RECURRING_TRANSACTION_EXPIRED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MERecurringTransactionFailed(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.RECURRING_TRANSACTION_FAILED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MERenewalTransactionCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.RENEWAL_TRANSACTION_COMPLETED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubAccountAdded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUB_ACCOUNT_ADDED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubAccountRemoved(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUB_ACCOUNT_REMOVED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionCreated(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_CREATED
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionDowngradedToOneTime(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionDowngradedToRecurring(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_RECURRING
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionDowngraded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_DOWNGRADED
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionExpired(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_EXPIRED
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionPaused(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_PAUSED
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionResumed(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_RESUMED
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionStopped(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_STOPPED
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionUpgradedToOneTime(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_ONE_TIME
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionUpgradedToRecurring(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_RECURRING
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionUpgraded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_UPGRADED
        self.event_type = MemberpressEventsTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventsTypes.MEMBERSHIP, MemberpressEventsTypes.MEMBER] + COMPLETE_TRANSACTION_DICT
        self.validate()


class METransactionCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.TRANSACTION_COMPLETED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class METransactionExpired(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.TRANSACTION_EXPIRED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class METransactionFailed(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.TRANSACTION_FAILED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class METransactionRefunded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.TRANSACTION_REFUNDED
        self.event_type = MemberpressEventsTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventsTypes.MEMBERSHIP,
            MemberpressEventsTypes.MEMBER,
            MemberpressEventsTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEUnidentifiedEvent(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.UNIDENTIFIED_EVENT
        self.event_type = ""
        self.qc_keys = []
        self.validate()


MEMBERPRESS_EVENT_CLASSES = {
    MemberpressEvents.AFTER_CC_EXPIRES_REMINDER: MEAfterCCExpiresReminder,
    MemberpressEvents.AFTER_MEMBER_SIGNUP_REMINDER: MEAfterMemberSignupReminder,
    MemberpressEvents.AFTER_SIGNUP_ABANDONED_REMINDER: MEAfterSignupAbandonedReminder,
    MemberpressEvents.AFTER_SUB_EXPIRES_REMINDER: MEAfterSubExpiresReminder,
    MemberpressEvents.BEFORE_CC_EXPIRES_REMINDER: MEBeforeCCExpiresReminder,
    MemberpressEvents.BEFORE_SUB_EXPIRES_REMINDER: MEBeforeSubExpiresReminder,
    MemberpressEvents.BEFORE_SUB_RENEWS_REMINDER: MEBeforeSubRenewsReminder,
    MemberpressEvents.BEFORE_SUB_TRIAL_ENDS: MEBeforeSubTrialEnds,
    MemberpressEvents.LOGIN: MELogin,
    MemberpressEvents.MEMBER_ACCOUNT_UPDATED: MEMemberAccountUpdated,
    MemberpressEvents.MEMBER_ADDED: MEMemberAdded,
    MemberpressEvents.MEMBER_DELETED: MEMemberDeleted,
    MemberpressEvents.MEMBER_SIGNUP_COMPLETED: MEMemberSignupCompleted,
    MemberpressEvents.MPCA_COURSE_COMPLETED: MEMPCACourseCompleted,
    MemberpressEvents.MPCA_COURSE_STARTED: MEMPCACourseStarted,
    MemberpressEvents.MPCA_LESSON_COMPLETED: MEMPCALessonCompleted,
    MemberpressEvents.MPCA_LESSON_STARTED: MEMPCALessonStarted,
    MemberpressEvents.MPCA_QUIZ_ATTEMPT_COMPLETED: MEMPCALQuizAttemptCompleted,
    MemberpressEvents.NON_RECURRING_TRANSACTION_COMPLETED: MENonRecurringTransactionCompleted,
    MemberpressEvents.NON_RECURRING_TRANSACTION_EXPIRED: MENonRecurringTransactionExpired,
    MemberpressEvents.OFFLINE_PAYMENT_COMPLETE: MEOfflinePaymentComplete,
    MemberpressEvents.OFFLINE_PAYMENT_PENDING: MEOfflinePaymentPending,
    MemberpressEvents.OFFLINE_PAYMENT_REFUNDED: MEOfflinePaymentRefunded,
    MemberpressEvents.RECURRING_TRANSACTION_COMPLETED: MERecurringTransactionCompleted,
    MemberpressEvents.RECURRING_TRANSACTION_EXPIRED: MERecurringTransactionExpired,
    MemberpressEvents.RECURRING_TRANSACTION_FAILED: MERecurringTransactionFailed,
    MemberpressEvents.RENEWAL_TRANSACTION_COMPLETED: MERenewalTransactionCompleted,
    MemberpressEvents.SUB_ACCOUNT_ADDED: MESubAccountAdded,
    MemberpressEvents.SUB_ACCOUNT_REMOVED: MESubAccountRemoved,
    MemberpressEvents.SUBSCRIPTION_CREATED: MESubscriptionCreated,
    MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME: MESubscriptionDowngradedToOneTime,
    MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_RECURRING: MESubscriptionDowngradedToRecurring,
    MemberpressEvents.SUBSCRIPTION_DOWNGRADED: MESubscriptionDowngraded,
    MemberpressEvents.SUBSCRIPTION_EXPIRED: MESubscriptionExpired,
    MemberpressEvents.SUBSCRIPTION_PAUSED: MESubscriptionPaused,
    MemberpressEvents.SUBSCRIPTION_RESUMED: MESubscriptionResumed,
    MemberpressEvents.SUBSCRIPTION_STOPPED: MESubscriptionStopped,
    MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_ONE_TIME: MESubscriptionUpgradedToOneTime,
    MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_RECURRING: MESubscriptionUpgradedToRecurring,
    MemberpressEvents.SUBSCRIPTION_UPGRADED: MESubscriptionUpgraded,
    MemberpressEvents.TRANSACTION_COMPLETED: METransactionCompleted,
    MemberpressEvents.TRANSACTION_EXPIRED: METransactionExpired,
    MemberpressEvents.TRANSACTION_FAILED: METransactionFailed,
    MemberpressEvents.TRANSACTION_REFUNDED: METransactionRefunded,
    MemberpressEvents.UNIDENTIFIED_EVENT: MEUnidentifiedEvent,
}


def get_event(data: dict) -> object:
    """
    introspect a data dict received by a webhook, determine the event type
    and return an instance the corresponding class.
    """
    event = data.get("event", None)
    if event:
        cls = MEMBERPRESS_EVENT_CLASSES[event]
        return cls(data)
