"""
base class
"""
import logging

logger = logging.getLogger(__name__)


class Memberpress:
    _json = None  # the dict passed in the body of the webhook request object
    _is_valid = False  # set in validate()
    _locked = False
    qc_keys = []  # set in __init__() of the child object. the data dict keys to validate

    def init(self):
        self._locked = False
        self._json = None

    def validate(self):
        if self.json is not None and type(self.json) != dict:
            self._is_valid = False
            return

        # validate more stuff here

        # if everything passed then return True
        self._is_valid = True

    def is_valid_dict(self, response, qc_keys) -> bool:
        if not type(response) == dict:
            logger.warning(
                "is_valid_dict() was expecting a dict but received an object of type: {type}".format(
                    type=type(response)
                )
            )
            return False
        return all(key in response for key in qc_keys)

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

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
    def locked(self):
        return self._locked

    @property
    def ready(self):
        return True if not self.locked and self.json and len(self.json) > 0 else False
