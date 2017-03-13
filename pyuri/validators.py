import six


class ExitValidation(Exception):
    """Raised by Validators to signal that current value is valid and no further validation is needed"""


class _Validator(object):
    def __init__(self, accept_none=True):
        self._accept_none = accept_none

    def __call__(self, value):
        if value is None:
            if self._accept_none:
                raise ExitValidation
            raise ValueError('None not valid for {}'.format(self.__class__.__name__))


class StringValidator(_Validator):
    """Accepts any string type"""

    def __call__(self, value):
        super(StringValidator, self).__call__(value)

        if isinstance(value, six.string_types):
            return value
        else:
            raise TypeError('Expected string type, got {}'.format(type(value)))


class PortValidator(_Validator):
    """Accepts int (or something that can be cast) within the accepted port range"""

    def __init__(self, low_port=0, high_port=65536, **kwargs):
        self._low_port = low_port
        self._high_port = high_port
        super(PortValidator, self).__init__(**kwargs)

    def __call__(self, value):
        super(PortValidator, self).__call__(value)

        value = int(value)

        if not self._low_port <= value <= self._high_port:
            raise ValueError('{} not within {}-{}'.format(value, self._low_port, self._high_port))

        return value
