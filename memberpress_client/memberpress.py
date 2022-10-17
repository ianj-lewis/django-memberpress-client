"""
base class
"""
import logging

logger = logging.getLogger(__name__)


class Memberpress:
    _json = None  # the dict passed in the body of the webhook request object
    _is_valid = False  # set in validate()
    _locked = False
    _qc_keys = []  # set in __init__() of the child object. the data dict keys to validate

    def init(self):
        self._locked = False
        self._json = None
        self._qc_keys = []
        logger.info("initialized {t}".format(t=type(self)))

    def validate(self):
        if not self.json:
            self._is_valid = False
            return

        if not self.qc_keys:
            self._is_valid = False
            return

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
    def qc_keys(self):
        return self._qc_keys

    @qc_keys.setter
    def qc_keys(self, value):
        if type(value) == list:
            self._qc_keys = list(set(value))
        else:
            logger.warning("qc_keys.setter received an invalid value: {v}".format(v=value))

    @property
    def json(self) -> dict:
        return self._json or {}

    @json.setter
    def json(self, value):
        if type(value) == dict or value is None:
            self.init()
            self._json = value
        else:
            logger.warning("was expecting a value of type dict but receive type {t}".format(t=type(value)))

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def locked(self) -> bool:
        return self._locked

    @property
    def ready(self) -> bool:
        return True if not self.locked and self.json and len(self.json) > 0 else False
