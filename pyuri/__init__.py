"""Python URI Handling"""

from pkg_resources import get_distribution, DistributionNotFound

from .uri import URI

__all__ = ['URI']

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = '0.0.0-dev'

