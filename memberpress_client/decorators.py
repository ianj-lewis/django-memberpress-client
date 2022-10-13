# Python imports
import json
import functools
import logging

from requests.exceptions import HTTPError

# imports from this project
from .utils import MPJSONEncoder, masked_dict

# module initializations
logger = logging.getLogger(__name__)




def request_manager(method):
    """
    Decorate a method to
    - retry on 401 http exceptions. Will attempt to refresh the token in this case, and try again.
    - catch and kill 429 exceptions.
    - catch and kill 415 exceptions.
    """

    def wrapper(*args, **kwargs):
        cls = args[0]
        operation = ""

        try:
            return method(*args, **kwargs)
        except HTTPError as e:
            # mcdaniel aug-2022:
            # look for an operation description if it exists
            if "operation" in kwargs.keys():
                operation = " " + kwargs["operation"]

            """
            mcdaniel oct-2022
            catch and kill exceptions of the following form:

                requests.exceptions.HTTPError: 415 Client Error: Unsupported Media Type for url: https://staging.global-communications-academy.com/gcsi/user/api/v1/preferences/florin
                2022-10-08 07:30:37,663 INFO member_press.client.Client.set_language() request: path=/gcsi/user/api/v1/preferences/florin, data={
                    "Authorization": "*** -- REDACTED -- ***",
                    "Content-Type": "application/merge-patch+json"
                }

            """
            if e.response.status_code == 415:
                logger.info(
                    "member_press.decorators.request_manager() -{operation} http request by method {method}() returned error 415: {err}".format(
                        operation=operation, method=method.__name__, err=e
                    )
                )
                return

            # mcdaniel jul-2022:
            # paring this down to only handle 401 errors bc everthing else
            # was getting tried twice, and failing twice.
            if e.response.status_code == 401:
                logger.info(
                    "member_press.decorators.request_manager() -{operation} http request by method {method}() returned error 401. Requesting a new session token.".format(
                        operation=operation, method=method.__name__
                    )
                )
                cls.token = cls.get_token()

                # mcdaniel jul-2022:
                # if the kwargs dict contains a value for `headers` then set this to None
                # so that, if needed, the calling method will reinitialize the header "Authorization" key
                # with the new session token.
                if "headers" in kwargs.keys():
                    kwargs["headers"] = None

                logger.info(
                    "member_press.decorators.request_manager() -{operation} a new session token has been issued. Re-attempting method {method}.".format(
                        operation=operation, method=method.__name__
                    )
                )
                return method(*args, **kwargs)
            # mcdaniel jul-2022 anything other than an http 401 error should be treated as an unhandled exception
            # however, we should add meta data about the request to the stack trace.
            #
            # mcdaniel: dump the request headers and body using MPJSONEncoder so that sensitive data is masked.
            request_body = json.dumps(e.response.content, cls=MPJSONEncoder, indent=4) if e.response is not None else ""
            request_headers = (
                json.dumps(masked_dict(dict(e.response.request.headers)), cls=MPJSONEncoder, indent=4)
                if e.response is not None and e.response.request is not None
                else ""
            )
            raise Exception(
                "member_press.decorators.request_manager(){operation} an unhandled exception '{error_message}', was returned by {method}(): {verb} {url}, headers={headers}, body={body}".format(
                    operation=operation,
                    method=method.__name__,
                    verb=e.response.request.method,
                    url=e.response.request.url,
                    headers=request_headers,
                    body=request_body,
                    error_message=str(e),
                )
            ) from e

    return wrapper


def app_logger(func):
    """
    Decorate a function to add an entry to the app log with the function name,
    its positional arguments, and keyword pairs presented as a formatted dict.

    sample output:
        2022-10-07 19:45:26,869 INFO app_logger: registration.views.EmailVerificationView().get() ["<WSGIRequest: GET '/verify-email/MjY1/bcxw75-69581da3ea4f0cefad2f0f2205354117/'>"] keyword args: {
            "uid": "MjY1",
            "token": "*** -- REDACTED -- ***"
        }
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        name_of_def = func.__name__
        logged_args = args
        kwargs_dict_repr = ""

        # try initializing variables assuming that we were called by a class method
        try:
            cls = args[0].__class__
            name_of_class = cls.__name__ + "()."
            name_of_module = cls.__module__
            # slice off the 'self' positional argument
            logged_args = args[1:]
        except Exception:
            # We weren't called by a class method. Fall back to initializing variables for
            # a standard module function.
            name_of_class = ""
            name_of_module = func.__module__

        positional_args = [repr(a) for a in logged_args]

        if len(kwargs.keys()) > 0:
            kwargs_dict_repr = "keyword args: "
            kwargs_dict_repr += json.dumps(masked_dict(kwargs), cls=MPJSONEncoder, indent=4)

        logger.info(
            "app_logger: {name_of_module}.{name_of_class}{name_of_def}() {args} {kwargs}".format(
                name_of_module=name_of_module,
                name_of_class=name_of_class,
                name_of_def=name_of_def,
                args=positional_args if len(positional_args) > 0 else "",
                kwargs=kwargs_dict_repr,
            )
        )
        return func(*args, **kwargs)

    return wrapper
