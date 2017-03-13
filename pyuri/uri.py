import os
import re

try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs

from .validators import *

with open(os.path.join(os.path.dirname(__file__), 'uri.regex')) as f:
    pattern = f.read()

URI_REGEX = re.compile(pattern, flags=re.VERBOSE)


class URI(object):
    """Data structure abstracting out work needed to parse and build URIs"""

    __modified = False
    __uri = None
    __validators = {
        'scheme': [StringValidator()],
        'username': [StringValidator()],
        'password': [StringValidator()],
        'host': [StringValidator(False)],
        'port': [PortValidator()],
        'path': [StringValidator()],
        'query': [StringValidator()],
        'fragment': [StringValidator()]
    }

    def __init__(
            self,
            uri=None,
            scheme=None,
            username=None,
            password=None,
            host=None,
            port=None,
            path=None,
            query=None,
            fragment=None
    ):
        args = locals()
        args.pop('self')

        if all([args[key] is None for key in args]):
            raise ValueError('Must provide either uri argument, or individual arguments to build URI (at minimum host)')

        if uri is not None and any([args[key] is not None for key in self.__validators]):
            raise ValueError('Cannot provide uri argument alongside any individual parameters')

        if uri is None:
            self.scheme = scheme
            self.username = username
            self.password = password
            self.host = host
            self.port = port
            self.path = path
            self.query = query
            self.fragment = fragment

        else:
            self.uri = uri

    def __str__(self):
        return self.uri

    def __repr__(self):
        return '{0.__class__.__name__}("{0.uri}")'.format(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.uri == self.uri

    def __setattr__(self, key, value):
        if key in self.__validators:
            self.__modified = True

            for validator in self.__validators[key]:
                try:
                    value = validator(value)
                except ExitValidation:
                    break
                except Exception as error:
                    raise ValueError('Unable to set `{}` = `{}`: {}'.format(key, value, error))

        return super(URI, self).__setattr__(key, value)

    @property
    def uri(self):
        """Cache to prevent recalculating URI unless necessary"""
        if self.__modified:
            self.__uri = self.__parse_uri()

        return self.__uri

    @uri.setter
    def uri(self, value):
        """Attempt to validate URI and split into individual values"""
        if value == self.__uri:
            return

        match = URI_REGEX.match(value)
        if match is None:
            raise ValueError('Unable to match URI from `{}`'.format(value))

        for key, value in match.groupdict().items():
            setattr(self, key, value)

    def __parse_uri(self):
        """Parse complete URI from all values"""
        if self.scheme:
            scheme = '{}://'.format(self.scheme)
        else:
            scheme = ''

        credentials = self.username or ''
        password = self.password or ''

        if credentials and password:
            credentials = self.username + ':' + self.password
        if credentials:
            credentials += '@'

        if self.port:
            location = '{}:{}'.format(self.host, self.port)
        else:
            location = self.host

        path = self.path or ''

        if self.query:
            query = '?' + self.query
        else:
            query = ''

        if self.fragment:
            fragment = '#' + self.fragment
        else:
            fragment = ''

        return scheme + credentials + location + path + query + fragment

    def query_dict(self):
        """Return dictionary of query parameters and their respective values"""
        return parse_qs(self.query)
