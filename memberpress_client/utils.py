import json
import logging
import datetime
import pytz
from unittest.mock import MagicMock
from dateutil.parser import parse, ParserError
from unittest.mock import MagicMock
from requests import Response

# django stuff
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import get_user_model

# open edx stuff
from opaque_keys.edx.keys import CourseKey
from common.lib.xmodule.xmodule.modulestore.django import modulestore
from lms.djangoapps.courseware.date_summary import VerifiedUpgradeDeadlineDate
from common.djangoapps.student.models import get_user_by_username_or_email
from openedx.core.djangoapps.user_api.errors import UserNotFound

# our  stuff
from memberpress_client.models import EcommerceConfiguration, EcommerceEOPWhitelist
from memberpress_client.utils import is_faculty, masked_dict

UTC = pytz.UTC
logger = logging.getLogger(__name__)
User = get_user_model()


def is_faculty(user):
    if user.is_staff or user.is_superuser:
        return True
    return False


def objects_key_by(iter, key):
    index = {}
    for obj in iter:
        value = getattr(obj, key)
        index[value] = obj
    return index


def parse_date_string(date_string, raise_exception=False):
    try:
        return parse(date_string)
    except (TypeError, ParserError):
        if not raise_exception:
            return
        raise


def masked_dict(obj) -> dict:
    """
    To mask sensitive key / value in log entries.
    masks the value of specified key.

    obj: a dict or a string representation of a dict, or None

    example:
        2022-10-07 20:03:01,455 INFO member_press.client.Client.register_user() request: path=/api/user/v1/account/registration/, data={
            "name": "__Pat_SelfReg-07",
            "username": "__Pat_SelfReg-07",
            "email": "pat.mcguire+Pat_SelfReg-07@cabinetoffice.gov.uk",
            "password": "*** -- REDACTED -- ***",
            "terms_of_service": true
        }

    """

    def redact(key: str, obj):
        if key in obj:
            obj[key] = "*** -- REDACTED -- ***"
        return obj

    obj = obj or {}
    obj = dict(obj)
    for key in settings.MEMBERPRESS_SENSITIVE_KEYS:
        obj = redact(key, obj)
    return obj


class MPJSONEncoder(json.JSONEncoder):
    """
    a custom encoder class.
    - smooth out bumps mostly related to test data.
    - ensure text returned is utf-8 encoded.
    - velvety smooth error handling, understanding that we mostly use
      this class for generating log data.
    """

    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        if isinstance(obj, MagicMock):
            return ""
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:
            # obj probably is not json serializable.
            return ""


class MPJSONEncoder(json.JSONEncoder):
    """
    a custom encoder class.
    - smooth out bumps mostly related to test data.
    - ensure text returned is utf-8 encoded.
    - velvety smooth error handling, understanding that we mostly use
      this class for generating log data.
    """

    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        if isinstance(obj, MagicMock):
            return ""
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:
            # obj probably is not json serializable.
            return ""


def get_user(username):
    try:
        return User.objects.get(username=username)
    except UserNotFound:
        pass


def paywall_should_render(request, context):
    """
    A series of boolean tests to determine whether the paywall html
    should be rendered an injected into the current page.

    Args:
        request: the current http request
        context: the mako context object

    Returns:
        [boolean]: True if the Mako template should fully render all html.
    """

    ## this code is moot if the user is not yet authenticated.
    try:
        user = get_user_by_username_or_email(request.user)
    except Exception:
        return False

    if not user.is_authenticated:
        logger("paywall_should_render() - Not authenticated, returning False.")
        return False

    if is_faculty(user):
        logger("paywall_should_render() - Faculty user - never block!, returning False.")
        return False

    if is_eop_student(request):
        logger("paywall_should_render() - User is an EOP student, returning False.")
        return False

    course = get_course(request, context)
    if course is None:
        logger("paywall_should_render() - Not a course, returning False.")
        return False

    course_id = get_course_id(request, context)
    if not is_ecommerce_enabled(request, context):
        logger(
            "paywall_should_render() - Student has already paid for course enrollment {email} / course_id {course_id}, or Ecommerce is not enabled for this course section. returning False.".format(
                course_id=course_id, email=user.email
            )
        )
        return False

    logger("paywall_should_render() - returning True for course_id {course_id}".format(course_id=course_id))
    return True


def paywall_should_raise(request, context):
    """[summary]

    Args:
        request: the current http request
        context: the mako context object

    Returns:
        [boolean]: True if the user has exceeded the payment deadline date
        for the course in which the current page is being rendered.
    """
    payment_deadline_date = get_course_deadline_date(request, context)
    course_id = get_course_id(request, context)
    user = get_user_by_username_or_email(request.user)

    if course_id is None:
        logger("paywall_should_raise() - course_id is None. Returning False.")
        return False

    if payment_deadline_date is None:
        logger(
            "paywall_should_raise() - payment_deadline_date is None {course_id}. Returning False.".format(
                course_id=course_id
            )
        )
        return False

    now = UTC.localize(datetime.datetime.now())
    if now <= payment_deadline_date:
        logger(
            "paywall_should_raise() - Payment deadline is in the future, returning False. {course_id}!".format(
                course_id=course_id
            )
        )
        return False

    logger(
        "paywall_should_raise() - Ecommerce paywall being raised on user {username} in course {course_id}!".format(
            username=user.email, course_id=course_id
        )
    )
    return True


def is_eop_student(request):
    """Looks for a record in EcommerceEOPWhitelist with the email address
    of the current user.

    Args:
        request: the current http request

    Returns:
        [boolean]: True if the current user's email address is saved
        to the EOP Whitelist table.
    """
    try:
        user = get_user_by_username_or_email(request.user)
        usr = EcommerceEOPWhitelist.objects.filter(user_email=user.email).first()
        if usr is not None:
            return True
    except ObjectDoesNotExist:
        pass

    return False


def is_ecommerce_enabled(request, context):
    """
    Args:
        request: the current http request

    Args:
        request: the current http request
        context: the mako context object

    Returns:
        [boolean]: True if Oscar e-commerce is running and this course
        has been configured for e-commerce.
    """
    block = get_verified_upgrade_deadline_block(request, context)
    if block is None:
        logger("is_ecommerce_enabled() - get_verified_upgrade_deadline_block is None. returning False")
        return False

    return block.is_enabled


def get_verified_upgrade_deadline_block(request, context):
    """Retrieve the content block containing the
    Verified Upgrade meta information.

    Args:
        request: the current http request
        context: the mako context object

    Returns:
        [type]: [description]
    """

    course = get_course(request, context)
    user = get_user_by_username_or_email(request.user)
    return VerifiedUpgradeDeadlineDate(course, user)


def get_course_id(request, context):
    """
    Extract the course_id from the current request, if one exists.

    Args:
        request: the current http request
        context: the mako context object

    Returns:
        [string]: string representation of the course_id, or None
    """
    try:
        """
        this is a hacky way to test for a course object that MIGHT be
        included in the page context for whatever page called this template.

        attempt to grap the course_id slug, if it exists.
        logger('get_course_id() context: {context}, course_key: {course_key}'.format(
           context=context.keys(),
           course_key=context['course_key']
        ))
        """
        course_id = str(context["course_key"])
        # course_key = CourseKey.from_string(course_id)
        return course_id
    except Exception:
        pass

    return None


def get_course(request, context):
    """retrieve the course object from the current request

    Args:
        request (http request): current request from the current  user
        context: the mako context object

    Returns:
        [course]: a ModuleStore course object
    """
    try:
        course_id = get_course_id(request, context)
        course_key = CourseKey.from_string(course_id)
        course = modulestore().get_course(course_key)
        return course
    except Exception:
        pass

    return None


def get_course_deadline_date(request, context):
    """
    retrieve the payment deadline date for the course.

    Args:
        course (CourseKey): the Opaque Key for the course which the current page
        is related.

    Returns:
        [DateTimeField]: the payment deadline date for the CourseKey
    """

    try:
        course_id = get_course_id(request, context)
        configuration = EcommerceConfiguration.objects.filter(course_id=course_id).first()
        if configuration is not None:
            return configuration.payment_deadline_date
    except Exception:
        return None

    return None


def logger(msg):
    logger.info(msg)


def enrollement_counts(enrollments) -> dict:
    """
    Return a dict report of all enrollement counts
    given a list of enrollements from the API
    """
    report = {"total": 0, "honor": 0, "audit": 0}
    for enrollment in enrollments:
        report.setdefault(enrollment["mode"], 0)
        if enrollment.get("is_active"):
            report[enrollment["mode"]] += 1
            report["total"] += 1
    return report


def log_trace(caller: str, path: str, data: dict) -> None:
    """
    add an application log entry for higher level defs that call the edxapp api.
    """
    logger.info(
        "member_press.client.Client.{caller}() request: path={path}, data={data}".format(
            caller=caller, path=path, data=json.dumps(masked_dict(data), cls=MPJSONEncoder, indent=4)
        )
    )


def log_pretrip(caller: str, url: str, data: dict, operation: str = "") -> None:
    """
    add an application log entry immediately prior to calling the edxapp api.
    """
    logger.info(
        "member_press.client.Client.{caller}() {operation}, request: url={url}, data={data}".format(
            operation=operation,
            caller=caller,
            url=url,
            data=json.dumps(masked_dict(data), cls=MPJSONEncoder, indent=4),
        )
    )


def log_postrip(caller: str, path: str, response: Response, operation: str = "") -> None:
    """
    log the api response immediately after calling the edxapp api.
    """
    status_code = response.status_code if response is not None else 599
    log_message = "member_press.client.Client.{caller}() {operation}, response status_code={response_status_code}, path={path}".format(
        operation=operation, caller=caller, path=path, response_status_code=status_code
    )
    if 200 <= status_code <= 399:
        logger.info(log_message)
    else:
        try:
            response_content = (
                json.dumps(response.content, cls=MPJSONEncoder, indent=4)
                if response is not None
                else "No response object."
            )
            log_message += ", response_content={response_content}".format(response_content=response_content)
        except TypeError:
            # TypeError: cannot convert dictionary update sequence element #0 to a sequence
            # This happens occasionally. Appears to be a malformed dict in the response body.
            pass

        logger.error(log_message)
